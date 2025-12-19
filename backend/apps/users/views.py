from rest_framework import status, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import Http404

from .permissions import IsAdminRole
from .serializers import UserSerializer
from ..courses.permissions import IsMentor

User = get_user_model()


# --- Authentication Views ---

class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            fn = request.data.get('first_name')
            ln = request.data.get('last_name')
            mail = request.data.get('email')

            if not username or not password or not mail or not fn or not ln:
                return Response({
                    'detail': 'All details are required',
                }, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=fn,
                last_name=ln,
                email=mail
            )

            token = RefreshToken.for_user(user)
            return Response({
                'data': {
                    'access': str(token.access_token),
                    'refresh': str(token),
                    'user': UserSerializer(user).data,
                },
                'detail': 'User registered successfully',
            }, status=status.HTTP_200_OK)

        except IntegrityError:
            return Response({
                'detail': 'User with this username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'detail': f'Registration Failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = RefreshToken.for_user(user)

        role_name = "Student"
        if user.role == User.Role.MENTOR: role_name = "Mentor"
        elif user.role == User.Role.ADMIN: role_name = "Admin"

        return Response({
            "data": {
                "access": str(token.access_token),
                "refresh": str(token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role,
                    "role_name": role_name,
                },
            },
            "detail": "User logged in successfully",
        }, status=status.HTTP_200_OK)




class UserViewSet(mixins.ListModelMixin,  # Enables GET /api/users/
                  mixins.DestroyModelMixin,  # Enables DELETE /api/users/:id/
                  viewsets.GenericViewSet):  # Base class
    """
    A unified ViewSet for User Management (Admin Only).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def list(self, request, *args, **kwargs):
        try:
            # super().list() handles pagination and serialization automatically
            response = super().list(request, *args, **kwargs)

            return Response({
                'data': response.data,
                'detail': 'Users fetched successfully',
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'detail': f'Failed to fetch users: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # Raises 404 automatically if not found
            self.perform_destroy(instance)

            return Response({
                'detail': 'User deleted successfully'
            }, status=status.HTTP_200_OK)

        except Http404:
            return Response({
                'detail': 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'detail': f'Failed to delete user: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Custom Action: PUT /api/users/:pk/approve-mentor/
    @action(detail=True, methods=['put'], url_path='approve-mentor')
    def approve_mentor(self, request, pk):
        try:
            user = self.get_object()

            if user.role == User.Role.ADMIN:
                return Response({
                    'detail': 'Cannot change the role of an Admin user.'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif user.role == User.Role.MENTOR:
                return Response({
                    'detail': 'User is already a mentor.'
                }, status=status.HTTP_400_BAD_REQUEST)

            user.role = User.Role.MENTOR
            user.save()

            return Response({
                'detail': f'User {user.username} has been approved as mentor',
            }, status=status.HTTP_200_OK)

        except Http404:
            return Response({
                'detail': f'User does not exist',
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'detail': f'Failed to approve as mentor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MentorStudentListView(APIView):
    """
    Mentor-only API to fetch all students.
    """
    permission_classes = [IsAuthenticated, IsMentor]

    def get(self, request):
        try:
            students = User.objects.filter(role=User.Role.STUDENT)

            serializer = UserSerializer(students, many=True)

            return Response({
                "data": serializer.data,
                "detail": "Students fetched successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "detail": f"Failed to fetch students: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)