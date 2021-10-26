from django.db import models

#biblioteca nativa Python
from decimal import Decimal
#bibliotecas Django
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
#bibliotecas h2o
import h2o
from h2o.automl import H2OAutoML
#biblioteca pandas
import pandas as pd

#Modelo que representa a tabela no banco de dados para que o registro dos dados de processamento seja persistido
# dados dos modelos que são criados
class ModeloMachineLearningProcessado(models.Model):
    model_id = models.TextField('Identificador do modelo', null=True)
    #conjunto de metricas de performance
    auc = models.DecimalField('aux', max_digits=10, decimal_places=6, null=True)
    logloss = models.DecimalField('logloss', max_digits=10, decimal_places=6, null=True)
    aucpr = models.DecimalField('aucpr', max_digits=10, decimal_places=6, null=True)
    mean_per_class_error = models.DecimalField('mean_per_class_error', max_digits=10, decimal_places=6, null=True)
    rmse = models.DecimalField('rmse', max_digits=10, decimal_places=6, null=True)
    mse = models.DecimalField('mse', max_digits=10, decimal_places=6, null=True)
    #binario do modelo para a previsão : saber onde o modelo ta
    binario_modelo = models.FileField('Binário do modelo ML', upload_to='binario_modelo_ml', null=True)


#Modelo que representa a tabela no banco de dados para o processo
class ProcessamentoModeloMachineLearning(models.Model):
    data = models.DateTimeField('Data e hora do processamento', auto_now_add=True)
    dados_csv = models.FileField('Arquivo CSV', upload_to='arquivos_csv') # sugestao de melhoria: aceitar outros formatos de arquivo xml,json,db
    #campo de resultado
    classe = models.CharField('Classe', max_length=30) # classe usuario informa
    variaveis_independentes = models.TextField('Variáveis independentes', null=True) # programa define os campos que não são a classe
    tempo_maximo = models.PositiveIntegerField('Tempo máximo em segundos', 
                                               validators=[MinValueValidator(settings.TEMPO_MINIMO_PROCESSAMENTO), 
                                                           MaxValueValidator(settings.TEMPO_MAXIMO_PROCESSAMENTO)],)
    modelos_processados = models.ManyToManyField('ia.ModeloMachineLearningProcessado')
    
    class Meta:
        ordering = ['-data']

    def processar(self):
        """
        Método que processa o Auto Machine Learning e guarda os resultados do melhor modelo ranqueado
        nos atributos do modelo da ORM Django ProcessamentoModeloMachineLearning
        """
        h2o.init()
        # Importa dados do CSV que foi gravado no atributo dados_csv do modelo da ORM
        imp = pd.read_csv(self.dados_csv, sep=";")

        # Identifica dinamicamente as colunas do arquivo CSV
        colunas = imp.columns.tolist()

        # Seleciona as variáveis independentes de forma excludente, considerando a classe
        variaveis_independentes = [coluna for coluna in colunas if coluna != self.classe]
        self.variaveis_independentes = ','.join(variaveis_independentes)
        self.save()

        # Divide em treino e teste
        imp = h2o.H2OFrame(imp)
        treino, teste = imp.split_frame(ratios=[.7])

        # Transforma a variável dependente em fator
        treino[self.classe] = treino[self.classe].asfactor()
        teste[self.classe] = teste[self.classe].asfactor()

        # Auto ML
        # Busca o modelo valor gravado no atributo tempo_maximo segundos, podemos em vez disso definir max_models
        modelo_automl = H2OAutoML(max_runtime_secs=self.tempo_maximo, sort_metric='AUC') # melhoria: informar metrica dinamicamente (pesquisar outras metricas)
        modelo_automl.train(y=self.classe, training_frame=treino)

        # Ranking dos melhores AutoML
        ranking = modelo_automl.leaderboard
        ranking = ranking.as_data_frame()

        # Salva os resultados dos modelos rankeados associados ao processamento
        for i in range(0, len(ranking)-1):
            
            modelo_processado = ModeloMachineLearningProcessado.objects.create(
                model_id=ranking['model_id'].iloc[i] ,
                auc= ranking['auc'].iloc[i].astype(Decimal),
                logloss= ranking['logloss'].iloc[i].astype(Decimal),
                aucpr= ranking['aucpr'].iloc[i].astype(Decimal),
                mean_per_class_error=ranking['mean_per_class_error'].iloc[i].astype(Decimal) ,
                rmse=  ranking['rmse'].iloc[i].astype(Decimal),
                mse= ranking['mse'].iloc[i].astype(Decimal),
            )
            modelo = h2o.get_model(modelo_processado.model_id)
            modelo_processado.binario_modelo.name = h2o.save_model(modelo, path="%s/modelo" % settings.MEDIA_ROOT, force=True)
            modelo_processado.save()
            self.modelos_processados.add(modelo_processado)