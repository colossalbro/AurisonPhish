from django.core.management.base import BaseCommand
from management.models import *


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from decouple import config 
from pytz import timezone as ptimezone  #so that it doesn't clash with django's timezone (django.utils.timezone)
from .tasks import *



#note (to self): Django-apscheduler felt less flexible after reading docs, so I opted to work directly with apscheduler, especially
#since i'm not doing anything 'much' scheduling :). 
#The caveat is I have to remeber to run this from the commandline :(
#command - python manage.py scheduler


class Command(BaseCommand):
    help = 'Start Apscheduler for periodic tasks'


    def handle(self, *args, **kwargs):
        scheduler = self.createScheduler()

        scheduler.add_job(deleteXlsx, 'interval', minutes=5)
        scheduler.add_job(sendEmail, 'interval', minutes=1)
        scheduler.add_job(sendAnalytics, 'interval', minutes=30)

        scheduler.start()
        
        try:
            self.stdout.write(self.style.SUCCESS('APScheduler started successfully.'))
            self.stdout.write(self.style.SUCCESS('Press Ctrl+C to exit'))
            while True:
                pass  #keep the thread alive.

        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()




    def createScheduler(self):
        gmt = ptimezone('GMT')

        jobstores = {
            'default': SQLAlchemyJobStore( url=config('DATABASE_URL') ) #Not even sure if this is necessary :|
        }

        executors = {
            'default': ThreadPoolExecutor(5)    #Don't need much.
        }

        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }

        return BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=gmt
        )