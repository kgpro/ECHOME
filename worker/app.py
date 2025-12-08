# import os
# from django.apps import AppConfig
# from .scheduler import scheduler, initialize_scheduler
# from ECHOME.BLOCK_CHAIN import ChainContract
# from ECHOME.IPFS import FilebaseIPFS
# from .utility_functions import utility_functions
#
# contract = ChainContract()  # contract object
# utility_client = utility_functions()
# ipfsClient = FilebaseIPFS()  # filebase object
#
# class MyAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'worker'
#
#     def ready(self):
#         import threading, time
#         from .tasks import send_notification
#
#         def start_scheduler():
#             time.sleep(10)  # give Django & DB time to start
#             try:
#                 initialize_scheduler()
#                 if not scheduler.running:
#                     scheduler.add_job(
#                         send_notification,
#                         'interval',
#                         minutes=1,
#                         id='send_notification',
#                         replace_existing=True
#                     )
#                     scheduler.start()
#                     print("✅ Scheduler started successfully")
#             except Exception as e:
#                 print(f"Scheduler failed to start: {e}")
#
#         if os.environ.get('RUN_MAIN') == 'true':
#             threading.Thread(target=start_scheduler, daemon=True).start()
