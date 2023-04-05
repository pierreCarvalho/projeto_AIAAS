from django.shortcuts import render
from .forms import UsuarioRegisterForm

from .models import Usuario
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

# Create your views here.
class UsuarioRegisterView(CreateView):
    model = Usuario
    form_class = UsuarioRegisterForm
    template_name = "usuario/usuario_register_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(UsuarioRegisterView, self).form_valid(form)

    def get_success_url(self):

        return reverse("usuario_register_success")


class UsuarioRegisterSuccessView(TemplateView):
    template_name = "usuario/usuario_register_success.html"
