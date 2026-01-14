from django.urls import path 
from src.api.views.compiler import *


urlpatterns = [
    path("run_code", run_code, name='run-code'),
    path('submit_solution', submit_solution, name="submit-solution"),
    path("compile_code/", compile_code_view, name="compile-code")
]