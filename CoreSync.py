#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import venv

# ---------------- CONFIG ---------------- #

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, "venv")
REQUIREMENTS_FILE = os.path.join(PROJECT_DIR, "requirements.txt")

# Change this if your entry file is different:
MAIN_SCRIPT = os.path.join(PROJECT_DIR, "main.py")

# ---------------- CORE ---------------- #

def run(cmd):
    print(f"[+] {cmd}")
    subprocess.check_call(cmd, shell=True)

def create_venv():
    if not os.path.exists(VENV_DIR):
        print("[+] Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)

def pip_path():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")

def python_path():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")

def install_dependencies():
    pip = pip_path()

    run(f'"{pip}" install --upgrade pip')

    if os.path.exists(REQUIREMENTS_FILE):
        run(f'"{pip}" install -r "{REQUIREMENTS_FILE}"')
    else:
        print("[!] No requirements.txt found — skipping dependency install.")

def run_project():
    py = python_path()

    if not os.path.exists(MAIN_SCRIPT):
        print(f"[!] Entry file not found: {MAIN_SCRIPT}")
        sys.exit(1)

    print("[+] Running project...")
    subprocess.call(f'"{py}" "{MAIN_SCRIPT}"', shell=True)

# ---------------- MAIN ---------------- #

def main():
    print(f"[+] OS: {platform.system()}")

    create_venv()
    install_dependencies()
    run_project()

if __name__ == "__main__":
    main()
