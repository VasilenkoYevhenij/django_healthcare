from datetime import date, timedelta

from core.celery import app


from .models import Schedule


@app.task
def reset_schedule():
    today = date.today()
    bad_date = str(today - timedelta(days=5))
    Schedule.objects.filter(date__lte=bad_date).delete()
