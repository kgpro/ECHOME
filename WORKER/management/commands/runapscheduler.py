from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from WORKER.tasks import send_notification, cleanup_old_logs

class Command(BaseCommand):
    help = 'Run APScheduler in blocking mode'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(send_notification, 'interval', minutes=1, id='send_notification')
        scheduler.add_job(cleanup_old_logs, 'interval', days=1, id='cleanup_old_logs')

        self.stdout.write(self.style.SUCCESS("Starting APScheduler..."))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
