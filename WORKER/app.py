import os
from django.apps import AppConfig
from .scheduler import scheduler, initialize_scheduler
from ECHOME.BLOCK_CHAIN import ChainContract
from ECHOME.IPFS import FilebaseIPFS
from .utility_functions import utility_functions

contract = ChainContract()
utility_client = utility_functions()
ipfsClient = FilebaseIPFS()

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WORKER'

    def ready(self):
        # Prevent multiple scheduler starts when Django autoreloads or Gunicorn forks
        if os.environ.get('RUN_MAIN') != 'true' and not scheduler.running:
            initialize_scheduler()
            print("APScheduler initialized inside Gunicorn process")

            from .tasks import send_notification
            scheduler.add_job(
                send_notification,
                'interval',
                minutes=1,
                id='send_notification',
                max_instances=4,
                replace_existing=True
            )
            scheduler.start()
