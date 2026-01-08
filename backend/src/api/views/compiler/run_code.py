from src.api.views.base import *
import subprocess
import tempfile
import os
from django.http import JsonResponse

def run_code(user_code, test_code):
    # Foydalanuvchi kodi va testlarni birlashtiramiz
    full_code = f"{user_code}\n\n{test_code}"
    
    # Vaqtinchalik fayl yaratamiz
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        tmp.write(full_code.encode('utf-8'))
        tmp_path = tmp.name

    try:
        # Docker konteynerida kodni ishga tushiramiz
        # --rm: ish bitgach konteynerni o'chiradi
        # -v: faylni konteynerga bog'laydi
        # memory: operativ xotirani cheklaydi
        result = subprocess.run([
            "docker", "run", "--rm",
            "-v", f"{tmp_path}:/app/solution.py",
            "--memory", "128m", 
            "python-sandbox", "python", "/app/solution.py"
        ], capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            return "Success", result.stdout
        else:
            return "Fail", result.stderr

    except subprocess.TimeoutExpired:
        return "Timeout", "Kod juda uzoq vaqt ishladi!"
    finally:
        os.remove(tmp_path)