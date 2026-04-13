from django.shortcuts import render

def field_capture(request):
    return render(request, 'field/capture.html')
