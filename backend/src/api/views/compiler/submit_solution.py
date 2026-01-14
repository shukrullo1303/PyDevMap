from src.api.views.base import *
from src.api.views.compiler.run_code import run_code

def submit_solution(request, task_id):
    if request.method == "POST":
        task = TaskModel.objects.get(id=task_id)
        user_code = request.POST.get('code')
        
        status, output = run_code(user_code, task.test_code)
        
        SubmissionModel.objects.create(
            task=task,
            code=user_code,
            status=status,
            result=output
        )
        
        return JsonResponse({"status": status, "output": output})