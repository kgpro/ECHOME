import os
from django.apps import AppConfig
from .scheduler import scheduler, initialize_scheduler
from ECHOME.BLOCK_CHAIN import ChainContract
from ECHOME.IPFS import FilebaseIPFS
from .utility_functions import utility_functions

contract = ChainContract()  # contract object
utility_client = utility_functions()
ipfsClient = FilebaseIPFS()  # filebase object

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WORKER'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # make sure scheduler run in main
            initialize_scheduler()
            print("Scheduler initialized")

            if not scheduler.running:  # check if scheduler is running

                '''
                all jobs should be added here
                '''
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
