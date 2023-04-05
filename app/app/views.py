

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

class HomeViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"
    # permission_classes = [IsAuthenticated]
    def get(self, request):

        return Response({})

class AboutViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "about.html"

    def get(self, request):

        return Response({})