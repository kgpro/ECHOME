from django.db.utils import OperationalError
from django.core.management import call_command

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WORKER'

    def ready(self):
        import threading
        from .scheduler import scheduler, initialize_scheduler
        from .tasks import send_notification

        def start_scheduler():
            from django.db import connections
            try:
                # Check if APScheduler tables exist
                connections['default'].ensure_connection()
                call_command('migrate', interactive=False)  # optional: run migrations automatically
                initialize_scheduler()
                if not scheduler.running:
                    scheduler.add_job(
                        send_notification,
                        'interval',
                        minutes=1,
                        id='send_notification',
                        max_instances=4,
                        replace_existing=True
                    )
                    scheduler.start()
                    print("✅ Scheduler started after migrations")
            except OperationalError:
                # DB not ready yet; retry in 10 seconds
                print("DB not ready yet. Retrying in 10s...")
                threading.Timer(10, start_scheduler).start()

        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=start_scheduler, daemon=True).start()
