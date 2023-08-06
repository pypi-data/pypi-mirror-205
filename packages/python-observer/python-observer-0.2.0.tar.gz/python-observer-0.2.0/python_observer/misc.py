import subprocess
import sys
from pathlib import Path


def get_python_version():
    return (
        subprocess.check_output(f"{sys.executable} --version", shell=True)
        .strip()
        .decode("utf-8")
    )


def run_file(command):
    cmd = [sys.executable, *command]

    return subprocess.run(cmd)


def resolve_path(path):
    return Path(path).resolve()


def file_exists(file_path):
    return Path(file_path).is_file()
