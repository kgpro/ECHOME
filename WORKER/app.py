import os
import threading
from django.apps import AppConfig
from django.db.utils import OperationalError

# Import scheduler-related utilities that do NOT require Django models
from .scheduler import scheduler, initialize_scheduler
from ECHOME.BLOCK_CHAIN import ChainContract
from ECHOME.IPFS import FilebaseIPFS
from .utility_functions import utility_functions

# Initialize external clients (safe at module level)
contract = ChainContract()
utility_client = utility_functions()
ipfsClient = FilebaseIPFS()


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WORKER'

    def ready(self):
        """
        Starts APScheduler safely in a separate thread.
        Lazy-import tasks to avoid AppRegistryNotReady errors.
        """

        def start_scheduler():
            from django.db import connections
            try:
                # Ensure DB connection is alive
                connections['default'].ensure_connection()

                # Lazy import tasks AFTER Django apps are fully loaded
                from .tasks import send_notification

                # Initialize the scheduler
                initialize_scheduler()

                # Add job only if scheduler isn't already running
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
                # DB might not be ready yet; retry after 10 seconds
                print("DB not ready yet. Retrying in 10s...")
                threading.Timer(10, start_scheduler).start()

        # Run only in the main Gunicorn process to avoid duplicate threads
        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=start_scheduler, daemon=True).start()
