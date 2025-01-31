from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from api.models import CustomUser  # Import CustomUser model
from nlmmm import chatbot  # Assuming chatbot logic is in nlmmm.py
import os
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)  # Since username holds the email
            if check_password(password, user.password):  # Check hashed password
                token = RefreshToken.for_user(user)
                return Response({
                    'access': str(token.access_token),
                    'refresh': str(token)
                })
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    def post(self, request):
        # Get username (email) and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username or password are missing
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email is valid
        if not self.is_valid_email(username):
            return Response({"error": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username (email) already exists in the database
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new user
            user = CustomUser.objects.create_user(username=username, password=password)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle any unexpected errors (e.g., database issues)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def is_valid_email(self, email):
        # Check if email is valid (basic validation)
        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


class QueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query')

        if not query:
            return Response({"error": "Query is missing."}, status=status.HTTP_400_BAD_REQUEST)

        response = chatbot(query)
        return Response({"response": response})


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"error": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            return Response({'access': str(token.access_token)})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Query by username (which is the email)
            user = CustomUser.objects.get(username=email)
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construct password reset link
            site_url = os.getenv("SITE_URL")  # Get the base URL from the environment variable
            reset_link = f"http://localhost:4200/reset-password/{uid}/{token}/"
            
            # Send email with password reset link
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                os.getenv("EMAIL_USER"),
                [email],
                fail_silently=False,
            )
            
            return Response({"message": "Password reset link sent to email."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def get(self, request, uidb64, token):
        # Check if the token is valid
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)  # Retrieve the user using the decoded uid
            
            if default_token_generator.check_token(user, token):
                # Token is valid, proceed with rendering the reset password form or returning a success message
                return Response({"message": "Token is valid, you can reset your password."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except (CustomUser.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, uidb64, token):
        # Handle POST request for resetting the password (already implemented)
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Decode uid and get user object
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)  # Use CustomUser as the model
            
            # Check if the token is valid
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except (CustomUser.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'index.html')
