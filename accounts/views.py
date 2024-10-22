from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import ResetPasswordRequestToken
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from threading import Thread
from utils import send_async_email
from .serializers import *

# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({'status': 'success', 'message': 'Users retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            email_subject = 'Alert Group Direct Debit: User Created'
            email_boby = f"""Dear {data['first_name']} {data['last_name']},\n
            You have been created successfully on the ALERT GROUP Direct Debit platform. Your default password is {data['password']}.\n\n
            Kindly click forget password to change the default password.\n\n
            Regards,\n
            Alert Group Direct Debit\n
            https://ndd.dap-alertgroup.com.ng"""
            # Asynchronously handle send mail
            Thread(target=send_async_email, args=(email_subject, email_boby, [data['email']])).start()
            return Response({'status': 'success', 'message': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except (ValidationError, IntegrityError) as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserRetrUpdtDelView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Exception, ObjectDoesNotExist):
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response({'status': 'success', 'message': 'User details retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except ObjectDoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except (Exception, ValidationError) as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response({'status': 'success', 'message': 'User updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Exception, ObjectDoesNotExist):
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response({'status': 'success', 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                return Response({'status': 'error', 'message': 'Email and password is required!'}, status=status.HTTP_400_BAD_REQUEST)
            response = super().post(request, *args, **kwargs)
            return Response({'status': 'success', 'message': 'User logged in successfully', 'data': response.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'error', 'message': 'Incorrect email or password'}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            token = RefreshToken(data['refresh'])
            token.blacklist()
            return Response({'status': 'success', 'message': 'User logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({'status': 'error', 'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, ValidationError) as e:
            return Response({'status': 'error', 'message': 'refresh: '+str(e.detail['refresh']).split("'")[1]}, status=status.HTTP_400_BAD_REQUEST)
        

class PasswordResetView(ResetPasswordRequestToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            if not email:
                return Response({'status': 'error', 'message': 'Email field is required!'}, status=status.HTTP_400_BAD_REQUEST)
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                token = ResetPasswordToken.objects.get(user__email=email)
                email_subject = 'Alert Group Direct Debit: Password Reset Request'
                email_body = f"""Dear {token.user}\n,
                You have requested a password reset. Use the following token to reset your password:\n
                Token: {token.key}\n\n
                PS: Please ignore if you did not initiate this process.\n\n
                Regards,\n
                Alert Group Direct Debit"""
                # Asynchronously handle send mail
                Thread(target=send_async_email, args=(email_subject, email_body, [token.user.email])).start()
                return Response({'status': 'success', 'message': 'Password reset email has been sent!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Error generating reset token'}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, ValidationError) as e:
            return Response({'status': 'error', 'message': 'Invalid email or email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        

class PasswordConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordConfirmSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            token = ResetPasswordToken.objects.select_related('user').get(key=data['token'])
            user = token.user
            user.set_password(data['password'])
            user.save()
            token.delete()
            return Response({'status': 'success', 'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except ResetPasswordToken.DoesNotExist:
            return Response({'status': 'error', 'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, ValidationError) as e:
            return Response({'status': 'error', 'message': 'password: '+str(e.detail['password']).split("'")[1]}, status=status.HTTP_400_BAD_REQUEST)
        
