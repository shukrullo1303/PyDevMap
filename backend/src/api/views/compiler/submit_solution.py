from src.api.views.base import *
from src.api.views.compiler.run_code import run_code
from src.api.views.compiler.ai_analysis import flexible_compare
from src.core.models.compiler.submission import POINTS_MAP


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_solution(request, task_id=None):
    if task_id is None:
        task_id = request.data.get('task_id')

    if not task_id:
        return Response({'error': 'task_id talab qilinadi'}, status=400)

    try:
        task = TaskModel.objects.get(id=task_id)
    except TaskModel.DoesNotExist:
        return Response({'error': 'Task topilmadi'}, status=404)

    user_code = request.data.get('code', '')
    if not user_code.strip():
        return Response({'error': "Kod bo'sh bo'lishi mumkin emas"}, status=400)

    run_status, output = run_code(user_code, task.test_code)

    # Natijani kutilgan bilan solishtirish
    is_correct = False
    points_earned = 0
    if run_status == 'Success':
        if task.test_code and 'unittest' in task.test_code:
            # unittest testlari o'tsa returncode=0 → Success = to'g'ri
            is_correct = True
        elif task.expected_output:
            is_correct = flexible_compare(task.expected_output, output)

    # Ball berish — faqat birinchi to'g'ri yechimda
    user = request.user if request.user.is_authenticated else None
    if is_correct and user:
        already_solved = SubmissionModel.objects.filter(
            task=task, user=user, is_correct=True
        ).exists()
        if not already_solved:
            points_earned = POINTS_MAP.get(task.difficulty, 10)

    SubmissionModel.objects.create(
        task=task,
        user=user,
        code=user_code,
        status=run_status,
        result=output,
        is_correct=is_correct,
        points_earned=points_earned,
    )

    return Response({
        'status': run_status,
        'output': output,
        'task_id': task.id,
        'is_correct': is_correct,
        'points_earned': points_earned,
    })
