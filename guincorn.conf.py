def on_starting(server):
    import os, django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ECHOME.settings')
    django.setup()
    from WORKER.scheduler import start_scheduler
    print("🔥 APScheduler launched before Gunicorn workers...")
    start_scheduler()
