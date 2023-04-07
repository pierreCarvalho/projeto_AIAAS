from rest_framework import serializers

from usuario.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "first_name",
            "last_name",
            "cpf",
            "email",
            "tipo",
            "rg",
            "data_nascimento",
        ]
