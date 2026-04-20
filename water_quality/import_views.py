from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .importers import import_water_quality_excel
from organisations.plans.permissions import ExcelImportPermission

class WaterQualityImportView(APIView):
    permission_classes = [IsAuthenticated, ExcelImportPermission]
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided. Send an Excel file with key "file"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']

        if not file.name.endswith(('.xlsx', '.xls')):
            return Response(
                {'error': 'Invalid file type. Please upload an .xlsx or .xls file'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = import_water_quality_excel(file)

        return Response({
            'message': f"Import complete. {results['created']} readings created.",
            'created': results['created'],
            'errors': results['errors'],
            'error_count': len(results['errors'])
        }, status=status.HTTP_201_CREATED if results['created'] > 0 else status.HTTP_400_BAD_REQUEST)