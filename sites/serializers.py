from rest_framework import serializers
from .models import MonitoringSite

class MonitoringSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringSite
        fields = '__all__'
        read_only_fields = ['organisation']