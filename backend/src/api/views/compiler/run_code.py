from src.api.views.base import *
import subprocess
import tempfile
import os
import re
import sys

# Xavfli modul va funksiyalar ro'yxati
BANNED_IMPORTS = [
    'os', 'sys', 'subprocess', 'shutil', 'pathlib',
    'socket', 'http', 'urllib', 'requests', 'httpx',
    'ftplib', 'smtplib', 'telnetlib',
    'ctypes', 'cffi', 'mmap',
    'pickle', 'shelve', 'marshal',
    'importlib', '__import__', 'builtins',
    'multiprocessing', 'threading', 'concurrent',
    'signal', 'resource', 'platform',
    'glob', 'fnmatch', 'fileinput',
    'tempfile', 'io',
]

BANNED_PATTERNS = [
    r'__import__\s*\(',
    r'open\s*\(',          # fayl o'qish/yozish
    r'exec\s*\(',
    r'eval\s*\(',
    r'compile\s*\(',
    r'getattr\s*\(',
    r'setattr\s*\(',
    r'delattr\s*\(',
    r'vars\s*\(',
    r'globals\s*\(',
    r'locals\s*\(',
    r'dir\s*\(',
]


def _is_safe(code: str) -> tuple[bool, str]:
    """
    Foydalanuvchi kodini xavfsizlik nuqtaidan tekshiradi.
    Qaytaradi: (xavfsiz_mi, xato_xabari)
    """
    lines = code.splitlines()
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # import os, import sys, from os import ...
        for banned in BANNED_IMPORTS:
            if re.search(rf'\bimport\s+{re.escape(banned)}\b', stripped):
                return False, f"Xavfli modul: '{banned}' ({i}-qator)"
            if re.search(rf'\bfrom\s+{re.escape(banned)}\b', stripped):
                return False, f"Xavfli modul: '{banned}' ({i}-qator)"

        # Xavfli funksiyalar
        for pattern in BANNED_PATTERNS:
            if re.search(pattern, stripped):
                fn = pattern.replace(r'\s*\(', '()').replace(r'\b', '')
                return False, f"Taqiqlangan funksiya: {fn} ({i}-qator)"

    return True, ''


def run_code(user_code: str, test_code: str):
    """
    Foydalanuvchi kodini xavfsiz ishga tushiradi.
    Docker mavjud bo'lsa — sandbox ichida, bo'lmasa — tekshirilgan direct mode.
    """
    # Xavfsizlik tekshiruvi (faqat direct mode uchun ham amal qiladi)
    safe, reason = _is_safe(user_code)
    if not safe:
        return "Fail", f"Xavfsizlik xatosi: {reason}"

    full_code = f"{user_code}\n\n{test_code}"

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write(full_code)
        tmp_path = tmp.name

    def _run_direct():
        return subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, 'PYTHONPATH': ''},  # env ni tozalab berish
        )

    try:
        use_direct = False
        try:
            result = subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{tmp_path}:/app/solution.py",
                "--memory", "128m",
                "--network", "none",          # tarmoqni o'chirish
                "--read-only",                # fayl tizimini read-only
                "python-sandbox", "python", "/app/solution.py"
            ], capture_output=True, text=True, timeout=5)

            if result.returncode != 0 and any(k in result.stderr.lower() for k in (
                'docker', 'daemon', 'cannot connect', 'pipe', 'failed to connect'
            )):
                use_direct = True
        except (FileNotFoundError, OSError):
            use_direct = True

        if use_direct:
            result = _run_direct()

        if result.returncode == 0:
            # unittest stderr ga yozadi, stdout bo'sh bo'lishi mumkin
            output = result.stdout if result.stdout.strip() else result.stderr
            return "Success", output
        else:
            return "Fail", result.stderr

    except subprocess.TimeoutExpired:
        return "Timeout", "Kod juda uzoq vaqt ishladi (5 soniya limit)!"
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
