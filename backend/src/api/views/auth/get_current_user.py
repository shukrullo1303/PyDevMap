from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([JWTAuthentication]) # Bu qator JWT ni majburiy qiladi
@permission_classes([IsAuthenticated])       # Bu qator login qilmaganlarni haydaydi
def get_current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_authenticated': user.is_authenticated,
    })