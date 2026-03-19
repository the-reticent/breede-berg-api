from rest_framework import viewsets
from .models import MonitoringSite
from .serializers import MonitoringSiteSerializer

class MonitoringSiteViewSet(viewsets.ModelViewSet):
    queryset = MonitoringSite.objects.all()
    serializer_class = MonitoringSiteSerializer
    
