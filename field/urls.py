from django.urls import path
from .views import field_capture

urlpatterns = [
    path('', field_capture, name='field-capture'),
]