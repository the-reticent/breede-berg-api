from rest_framework import viewsets
from .models import VegetationSurvey
from .serializers import VegetationSurveySerializer

class VegetationSurveyViewSet(viewsets.ModelViewSet):
    queryset = VegetationSurvey.objects.all()
    serializer_class = VegetationSurveySerializer