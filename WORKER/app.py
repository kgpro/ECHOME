import os
import threading
from django.apps import AppConfig
from django.db.utils import OperationalError
from django.core.management import call_command

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WORKER'

    def ready(self):
        from .scheduler import scheduler, initialize_scheduler
        from .tasks import send_notification

        def start_scheduler():
            print("🔹 Scheduler thread starting...")
            from django.db import connections
            try:
                # Ensure DB is ready
                connections['default'].ensure_connection()
                call_command('migrate', interactive=False)  # optional
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
                    print("✅ APScheduler started successfully")
            except OperationalError:
                print("DB not ready yet. Retrying in 10s...")
                threading.Timer(10, start_scheduler).start()
            except Exception as e:
                print(f"❌ Scheduler failed: {e}")

        # Start scheduler only in main thread (works with Gunicorn)
        if threading.current_thread().name == "MainThread":
            threading.Thread(target=start_scheduler, daemon=True).start()
