from rest_framework import viewsets
from .models import WildlifeSighting
from .serializers import WildlifeSightingSerializer

class WildlifeSightingViewSet(viewsets.ModelViewSet):
    queryset = WildlifeSighting.objects.all()
    serializer_class = WildlifeSightingSerializer