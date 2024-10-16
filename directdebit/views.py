from rest_framework import views, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, permissions
import requests
from .serializers import *
from utils import base_url, headers, format_date


class CreateMandateView(generics.CreateAPIView):
    serializer_class = CreateMandateSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            data['startDate'] = format_date(data.get('startDate'))
            data['endDate'] = format_date(data.get('endDate'))
            # Handle file upload
            file = data.pop('mandateImageFile', None)
            if not file:
                return Response({'status': 'error', 'message': 'File field is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Prepare payload for file upload
            file_upload = [('mandateImageFile', (file.name, file, file.content_type))]
            url = f"{base_url}ndd/v2/api/MandateRequest/CreateMandateDirectDebit"
            response = requests.post(url, headers=headers, data=data, files=file_upload)
            if response.status_code == 201:
                return Response({'status': 'success', 'message': 'Mandate created successfully', 'data': response.json()}, status=status.HTTP_201_CREATED)
            else:
                error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BalanceEnquiryView(generics.GenericAPIView):
    serializer_class = CreateMandateSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            data['startDate'] = format_date(data.get('startDate'))
            data['endDate'] = format_date(data.get('endDate'))
            # Handle file upload
            file = data.pop('mandateImageFile', None)
            if not file:
                return Response({'status': 'error', 'message': 'File field is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Prepare payload for file upload
            file_upload = [('mandateImageFile', (file.name, file, file.content_type))]
            url = f"{base_url}ndd/v2/api/MandateRequest/CreateMandateBalanceEnquiry"
            response = requests.post(url, headers=headers, data=data, files=file_upload)
            if response.status_code == 201:
                return Response({'status': 'success', 'message': 'Mandate created successfully', 'data': response.json()}, status=status.HTTP_201_CREATED)
            else:
                error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class MandateStatusView(generics.GenericAPIView):
    serializer_class = MandateStatusSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        try:
            serializer.is_valid(raise_exception=True)
            mandate_code = serializer.validated_data['mandate_code']
            url = f"{base_url}ndd/v2/api/MandateRequest/MandateStatus?MandateCode={mandate_code}"
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                return Response({'status': 'success', 'message': 'Mandate status fetched successfully', 'data': response.json()}, status=status.HTTP_200_OK)
            else:
                error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateEMandateView(generics.CreateAPIView):
    serializer_class = EMandateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            data['startDate'] = format_date(data.get('startDate'))
            data['endDate'] = format_date(data.get('endDate'))
            url = f"{base_url}ndd/v2/api/MandateRequest/CreateEmandate"
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                return Response({'status': 'success', 'message': 'E-Mandate created successfully', 'data': response.json()['data']}, status=status.HTTP_201_CREATED)
            else:
                error_message = response.json()['errors'] if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FetchMandateView(generics.GenericAPIView):
    serializer_class = FetchMandateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, page, pageSize, *args, **kwargs):
        # page = 1
        # pageSize = 20
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            url = f"{base_url}ndd/v2/api/MandateRequest/FetchMandate?page={page}&pageSize={pageSize}"
            print(url)
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return Response({'status': 'success', 'message': 'Fetched mandate successfully', 'data': response.json()}, status=status.HTTP_200_OK)
            else:
                error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateMandateStatusView(generics.CreateAPIView):
    serializer_class = UpdateMandateStatus
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            url = f"{base_url}ndd/v2/api/MandateRequest/UpdateMandateStatus"
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return Response({'status': 'success', 'message': 'Mandate status updated successfully', 'data': response.json()['data']}, status=status.HTTP_201_CREATED)
            else:
                error_message = response.json()['errors'] if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetProductView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id, *args, **kwargs):
        url = f"{base_url}ndd/v2/api/Biller/GetProduct/{id}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response({'status': 'success', 'message': 'Fetched product successfully', 'data': response.json()}, status=status.HTTP_200_OK)
            else:
                error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                return Response({'status': 'error', 'message': error_message}, status=response.status_code)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

