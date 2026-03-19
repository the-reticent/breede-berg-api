from rest_framework import serializers
from .models import VegetationSurvey

class VegetationSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = VegetationSurvey
        fields = '__all__'