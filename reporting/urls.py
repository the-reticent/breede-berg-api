from django.urls import path
from .views import FunderReportView

urlpatterns = [
    path('funder-report/', FunderReportView.as_view(), name='funder-report'),
]