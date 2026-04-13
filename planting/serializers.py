from rest_framework import serializers
from .models import PlantingEvent, SurvivalCheck


class SurvivalCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurvivalCheck
        fields = '__all__'
        read_only_fields = ['survival_rate']


class PlantingEventSerializer(serializers.ModelSerializer):
    survival_checks = SurvivalCheckSerializer(many=True, read_only=True)
    latest_survival_rate = serializers.SerializerMethodField()
    days_since_planting = serializers.SerializerMethodField()

    class Meta:
        model = PlantingEvent
        fields = '__all__'

    def get_latest_survival_rate(self, obj):
        latest = obj.survival_checks.first()
        if latest:
            return float(latest.survival_rate)
        return None

    def get_days_since_planting(self, obj):
        from django.utils import timezone
        delta = timezone.now().date() - obj.planting_date
        return delta.days