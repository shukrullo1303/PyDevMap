from src.api.views.base import *
from src.api.views.compiler.run_code import run_code


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def compile_code_view(request):
    user_code = request.data.get('user_code', '')
    test_code = request.data.get('test_code', '') # Odatda bazadan olinadi

    status, output = run_code(user_code, test_code)
    
    return Response({
        "status": status,
        "output": output
    })