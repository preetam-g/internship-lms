from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404

from .permissions import IsAdminRole
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password']
        )
        return Response({
            'detail': 'User registered',
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if not user:
            return Response({
                'detail': 'Invalid username or password',
            }, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(user)
        return Response({
            'data': {
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            },
            'detail': 'User logged in',
        }, status=status.HTTP_200_OK)


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        """
        GET /api/users
        Retrieve a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response({
            'data': serializer.data,
            'detail': 'Users fetched successfully',
        }, status=status.HTTP_200_OK)


class ApproveMentorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def put(self, request, id):
        """
        PUT /api/users/:id/approve-mentor
        Approve a user by setting is_approved to True and updating role to Mentor.
        """
        # 1. Use get_object_or_404 to handle the "User does not exist" error automatically
        user = get_object_or_404(User, pk=id)
        # 2. Update the role
        user.role = User.Role.MENTOR
        user.save()

        return Response({
            'detail': f'User {user.username} has been approved as mentor',
        }, status=status.HTTP_200_OK)