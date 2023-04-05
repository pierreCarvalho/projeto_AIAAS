from django.urls import path

from . import views


urlpatterns = [
    path(
        "treinar-modelo",
        views.ProcessamentoModeloMachineLearningView.as_view(),
        name="treinar_modelo",
    ),
    path("prever", views.PrevisaoView.as_view(), name="prever"),
    path("prever-form", views.PreverViewSet.as_view(), name="prever-form"),
    path(
        "treinar-modelo-form",
        views.TreinarViewSet.as_view(),
        name="treinar-modelo-form",
    ),
    
]
