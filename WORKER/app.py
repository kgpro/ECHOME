import os
import threading
from django.apps import AppConfig                
from django.db.utils import OperationalError
from django.core.management import call_command

from .scheduler import scheduler, initialize_scheduler
from .tasks import send_notification
from ECHOME.BLOCK_CHAIN import ChainContract
from ECHOME.IPFS import FilebaseIPFS
from .utility_functions import utility_functions

# Initialize your clients here
contract = ChainContract()
utility_client = utility_functions()
ipfsClient = FilebaseIPFS()


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WORKER'

    def ready(self):
        """
        Starts APScheduler safely after database is ready.
        Runs in a separate thread so it does not block Gunicorn.
        Retries automatically if DB is not ready yet.
        """

        def start_scheduler():
            from django.db import connections
            try:
                # Ensure DB connection is alive
                connections['default'].ensure_connection()

                # Optional: run migrations automatically on deploy
                call_command('migrate', interactive=False)

                # Initialize scheduler
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
                    print("✅ APScheduler started successfully after DB ready")
            except OperationalError:
                print("DB not ready yet. Retrying in 10s...")
                threading.Timer(10, start_scheduler).start()

        # Only start once in main process (avoid multiple threads on Gunicorn reloads)
        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=start_scheduler, daemon=True).start()
