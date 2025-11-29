#!/usr/bin/env python3
import os
import getpass
import subprocess
from pathlib import Path


def detect_project_root():
    # Directory where script is executed
    return Path(__file__).resolve().parent


def detect_venv():
    # Check VIRTUAL_ENV variable (if executed inside venv)
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        return Path(venv)

    # Fallback: auto-detect ".venv" or "venv" folder
    project = detect_project_root()
    for name in [".venv", "venv"]:
        candidate = project / name
        if candidate.exists():
            return candidate

    raise RuntimeError("Could not detect virtual environment folder!")


def create_supervisor_config(project_path, venv_path, user):
    gunicorn_cmd = f"{venv_path}/bin/gunicorn"
    celery_cmd   = f"{venv_path}/bin/celery"

    config = f"""
[program:gunicorn_dynamic]
directory={project_path}
command={gunicorn_cmd} ECHOME.wsgi:application --bind 0.0.0.0:8000 --workers 3
user={user}
autostart=true
autorestart=true
stdout_logfile=/var/log/gunicorn_dynamic.log
stderr_logfile=/var/log/gunicorn_dynamic_error.log
stopasgroup=true
killasgroup=true

[program:celery_workerbeat_dynamic]
directory={project_path}
command={celery_cmd} -A ECHOME worker -B --loglevel=info
user={user}
autostart=true
autorestart=true
stdout_logfile=/var/log/celery_workerbeat_dynamic.log
stderr_logfile=/var/log/celery_workerbeat_dynamic_error.log
stopasgroup=true
killasgroup=true
"""
    return config


def write_supervisor_conf(config):
    conf_path = "/etc/supervisor/conf.d/echome_dynamic.conf"
    with open(conf_path, "w") as f:
        f.write(config)
    print(f"[+] Supervisor config created at: {conf_path}")
    return conf_path


def reload_supervisor():
    print("[+] Reloading supervisor...")
    subprocess.run(["sudo", "supervisorctl", "reread"])
    subprocess.run(["sudo", "supervisorctl", "update"])


def main():
    print("[*] Auto-detecting system setup...")

    project_path = detect_project_root()
    print(f"[+] Project path detected: {project_path}")

    venv_path = detect_venv()
    print(f"[+] Virtualenv path detected: {venv_path}")

    user = getpass.getuser()
    print(f"[+] Running as user: {user}")

    config_text = create_supervisor_config(project_path, venv_path, user)

    conf_file = write_supervisor_conf(config_text)

    reload_supervisor()

    print("\n[✔] Setup complete!")
    print("[✔] Run these commands if services aren't started automatically:")
    print("    sudo supervisorctl start gunicorn_dynamic")
    print("    sudo supervisorctl start celery_workerbeat_dynamic")


if __name__ == "__main__":
    main()
