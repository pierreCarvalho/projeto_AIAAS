from django.shortcuts import get_object_or_404, redirect
from requests import Response
from usuario.api.serializers import UsuarioSerializer
from usuario.models import Usuario
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class UsuarioList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "usuario_list.html"

    def get(self, request):
        queryset = Usuario.objects.all()
        return Response({"usuarios": queryset})


class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile_detail.html"

    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = UsuarioSerializer(usuario)
        return Response({"serializer": serializer, "usuario": usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "usuario": usuario})
        serializer.save()
        return redirect("usuario-list")
