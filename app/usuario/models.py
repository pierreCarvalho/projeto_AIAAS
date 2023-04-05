# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User

from utils.gerador_hash import gerar_hash

# from django.core.validators import MaxValueValidator, MinValueValidator
# from utils.gerador_hash import gerar_hash


class Usuario(User):
    # 1 campo da tupla fica no banco de dados
    # 2 campo da tupla eh mostrado para o usuario
    TIPOS = (("ADMINISTRADOR", "Administrador"), ("NORMAL", "Normal"))

    USERNAME_FIELD = "email"

    tipo = models.CharField(
        ("Tipo do usuário"), max_length=15, choices=TIPOS, default="NORMAL"
    )
    data_nascimento = models.DateField(
        ("Data de Nascimento"), blank=True, null=True, help_text="dd/mm/aaaa"
    )
    cpf = models.CharField(
        ("CPF"),
        max_length=14,
        help_text="Atenção: SOMENTE OS NÚMEROS",
        blank=True,
        null=True,
    )
    rg = models.CharField(
        ("RG"),
        max_length=10,
        help_text="Atenção: SOMENTE OS NÚMEROS",
        blank=True,
        null=True,
    )

    slug = models.SlugField("Hash", max_length=200, null=True, blank=True)

    class Meta:
        ordering = ["first_name"]
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")

    def __str__(self):
        return "%s %s- %s " % (self.first_name, self.last_name, self.tipo)

    def get_short_name(self):
        try:
            return self.first_name[0:10].strip()
        except:
            return None

    def get_full_name(self):
        try:
            return f"{self.first_name} {self.last_name}"
        except:
            return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        if not self.id:
            self.set_password(self.password)
        super(Usuario, self).save(*args, **kwargs)

    def get_id(self):
        try:
            return self.id
        except:
            return None

    # @property
    # def get_absolute_url(self):
    #     return reverse("usuario_update", args=[str(self.id)])

    # @property
    # def get_delete_url(self):
    #     return reverse("usuario_delete", args=[str(self.id)])

    # @property
    # def get_usuario_register_activate_url(self):
    #     return "%s%s" % (
    #         settings.DOMINIO_URL,
    #         reverse("usuario_register_activate", kwargs={"slug": self.slug}),
    #     )
