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


class UsuarioCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "usuario_create.html"

    def get(self, request):
        serializer = UsuarioSerializer()
        return Response({"serializer": serializer})

    def post(self, request, id):
        # usuario = get_object_or_404(Usuario, pk=id)
        serializer = UsuarioSerializer(data=request.data)
        if not serializer.is_valid():
            usuario = serializer.save()
            return Response({"serializer": serializer, "usuario": usuario})
        serializer.save()
        return redirect("usuario_list")


class UsuarioDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "usuario_detail.html"

    def get(self, request, id):
        usuario = get_object_or_404(Usuario, pk=id)
        serializer = UsuarioSerializer(usuario)
        return Response({"serializer": serializer, "usuario": usuario})

    def post(self, request, id):
        usuario = get_object_or_404(Usuario, pk=id)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "usuario": usuario})
        serializer.save()
        return redirect("usuario_list")


class UsuarioDelete(APIView):
    def get(self, request, id):
        usuario = get_object_or_404(Usuario, pk=id)
        usuario.delete()
        return redirect("usuario_list")
