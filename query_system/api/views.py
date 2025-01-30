from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import render
from api.models import CustomUser  # Import CustomUser model
from django.contrib.auth.hashers import check_password  # For checking hashed passwords
from nlmmm import chatbot  # Assuming you have integrated your chatbot logic from nlmmm.py

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):  # Check hashed password
                # Generate JWT token
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
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = CustomUser.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
class QueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query')

        if not query:
            return Response({"error": "Query is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the chatbot function from nlmmm.py to process the query
        response = chatbot(query)

        return Response({"response": response})
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"error": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token)
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
def home(request):
    return render(request, 'index.html')  # Ensure that 'index.html' exists in your templates directory
