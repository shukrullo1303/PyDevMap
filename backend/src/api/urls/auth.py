from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user profile"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not all([username, email, password]):
            return Response(
                {'detail': 'username, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', get_current_user, name='current_user'),
    path('register/', register_user, name='register'),
]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })
