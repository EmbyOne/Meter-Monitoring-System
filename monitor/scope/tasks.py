from datetime import timedelta
from .models import Meter
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


#This handles deleting database entries after a set amount of time, works in the background
@register_job(scheduler, 'interval', seconds=3600, id='epicID', replace_existing=True)
def delete_data():
    for record in Meter.objects.all():
        time_elapsed = timezone.now() - record.time
        if time_elapsed >= timedelta(hours=24):
            record.delete()
            print('deleters')
        else:
            print('keepers')
    #print('done')

register_events(scheduler)