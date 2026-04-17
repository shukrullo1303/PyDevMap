from django.urls import path
from src.api.views.compiler import (
    run_code, submit_solution, compile_code_view,
    task_list, task_detail, task_solved_check, analyze_code, leaderboard,
)

urlpatterns = [
    # Task ro'yxati va detail
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:task_id>/', task_detail, name='task-detail'),
    path('tasks/<int:task_id>/solved/', task_solved_check, name='task-solved-check'),

    # Submit va run
    path('submit/<int:task_id>/', submit_solution, name='submit-solution'),
    path('submit/', submit_solution, name='submit-solution-body'),
    path('run_code/', run_code, name='run-code'),
    path('compile_code/', compile_code_view, name='compile-code'),

    # AI tahlil
    path('analyze/', analyze_code, name='analyze-code'),

    # Leaderboard
    path('leaderboard/', leaderboard, name='leaderboard'),
]
