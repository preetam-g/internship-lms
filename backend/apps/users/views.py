
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password']
        )
        return Response({'status':'registered'})

class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        token = RefreshToken.for_user(user)
        return Response({'access': str(token.access_token)})
