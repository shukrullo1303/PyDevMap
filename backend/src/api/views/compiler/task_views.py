"""
Task list/detail views — LeetCode uslubidagi masalalar ro'yxati.
"""
from src.api.views.base import *
from src.api.serializers import TaskSerializer, TaskDetailSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def task_list(request):
    """Barcha tasklar ro'yxati (difficulty bo'yicha filter)."""
    tasks = TaskModel.objects.all()

    difficulty = request.query_params.get('difficulty')
    if difficulty:
        tasks = tasks.filter(difficulty__iexact=difficulty)

    search = request.query_params.get('search')
    if search:
        tasks = tasks.filter(title__icontains=search)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def task_detail(request, task_id):
    """Bitta task. Agar user login qilgan bo'lsa — user_solved ham qaytaradi."""
    try:
        task = TaskModel.objects.get(id=task_id)
    except TaskModel.DoesNotExist:
        return Response({'error': 'Task topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    data = serializer.data

    user_solved = False
    if request.user.is_authenticated:
        user_solved = SubmissionModel.objects.filter(
            task=task, user=request.user, is_correct=True
        ).exists()
    data['user_solved'] = user_solved

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def task_solved_check(request, task_id):
    """Foydalanuvchi bu taskni yechganmi? {solved: true/false}"""
    if not request.user.is_authenticated:
        return Response({'solved': False})
    solved = SubmissionModel.objects.filter(
        task_id=task_id, user=request.user, is_correct=True
    ).exists()
    return Response({'solved': solved})
