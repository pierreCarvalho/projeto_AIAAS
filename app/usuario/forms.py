from django import forms
from .models import Usuario


class UsuarioRegisterForm(forms.ModelForm):
    TIPOS_REGISTER = (
        ("NORMAL", "Normal"),
        ("ADMINISTRADOR", "Administrador"),
    )
    tipo = forms.ChoiceField(label="Tipo", choices=TIPOS_REGISTER)
    nome = forms.CharField(label="Nome")
    email = forms.EmailField(label="Email *", max_length=100)
    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        help_text="Atenção: SOMENTE OS NÚMEROS",
        required=False,
    )
    rg = forms.CharField(
        label="RG",
        max_length=14,
        help_text="Atenção: SOMENTE OS NÚMEROS",
        required=False,
    )
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = [
            "nome",
            "tipo",
            "email",
            "cpf",
            "rg",
            "password",
        ]
