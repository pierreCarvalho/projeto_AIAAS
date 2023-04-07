from django.urls import path

from . import views
from .api import viewsets as vs_usuario

urlpatterns = [
    path("listagem-usuarios", vs_usuario.UsuarioList.as_view(), name="usuario_list"),
    path("create-usuario/", vs_usuario.UsuarioCreate.as_view(), name="usuario_create"),
    path(
        "editar-usuario/<int:id>/",
        vs_usuario.UsuarioDetail.as_view(),
        name="usuario_update",
    ),
    path(
        "remover-usuario/<int:id>/",
        vs_usuario.UsuarioDelete.as_view(),
        name="usuario_delete",
    ),
    path("register", views.UsuarioRegisterView.as_view(), name="usuario_register"),
    path(
        "registersuccess/",
        views.UsuarioRegisterSuccessView.as_view(),
        name="usuario_register",
    ),
]
