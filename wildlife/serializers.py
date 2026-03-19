from rest_framework import serializers
from .models import WildlifeSighting

class WildlifeSightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeSighting
        fields = '__all__'