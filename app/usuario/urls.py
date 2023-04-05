from django.urls import path

from . import views
from .api import viewsets as vs_usuario

urlpatterns = [
    path("listagem-usuarios", vs_usuario.UsuarioList.as_view(), name="usuario_list"),
    path("register", views.UsuarioRegisterView.as_view(), name="usuario_register"),
    path(
        "registersuccess/",
        views.UsuarioRegisterSuccessView.as_view(),
        name="usuario_register",
    ),
]
