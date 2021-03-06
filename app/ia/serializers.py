from rest_framework import serializers

from .models import ProcessamentoModeloMachineLearning, ModeloMachineLearningProcessado

#informação dos modelos gerados
class ModeloMachineLearningProcessadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloMachineLearningProcessado
        #quais atributos do modelo são usados
        fields = ['model_id', 'auc', 'logloss', 'aucpr', 'mean_per_class_error', 'rmse', 'mse', 'binario_modelo']

#informação do processamento
class ProcessamentoModeloMachineLearningCreateSerializer(serializers.ModelSerializer):
    modelos_processados = ModeloMachineLearningProcessadoSerializer(many=True, read_only=True)

    #melhoria: reescer o create e validar campos
    class Meta:
        model = ProcessamentoModeloMachineLearning
        #dados do processamento
        #modelos_processados é um relacionamento many to many que é lista de objetos de cima
        fields = ['id', 'data', 'dados_csv', 'classe', 'variaveis_independentes', 'tempo_maximo', 'modelos_processados']
        read_only_fields = ['id', 'data', 'variaveis_independentes', 'modelos_processados']

#recebe dado do usuário para prever
class PrevisaoSerializer(serializers.Serializer):
    model_id = serializers.CharField(required=False)
    csv_prever = serializers.FileField(allow_empty_file=False)