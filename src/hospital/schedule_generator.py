from datetime import timedelta, datetime

from rest_framework.exceptions import APIException

from .models import Schedule, Visit


def schedule_choose(serializer, doctor):
    """Call function to generate schedule. Depends on choice of periodicity"""
    date = serializer.data['date']
    date_time_obj = datetime.strptime(date, '%d/%m/%y %H:%M:%S')
    time_from = datetime.strptime(serializer.data['time_from'], '%H:%M:%S')
    time_to = datetime.strptime(serializer.data['time_to'], '%H:%M:%S')

    if serializer.validated_data['periodicity'] == 'Every week':
        return every_week_schedule(date_time_obj, time_from, time_to, doctor)
    elif serializer.validated_data['periodicity'] == 'Except weekend':
        return except_weekend_schedule(date_time_obj, time_from, time_to, doctor)
    elif serializer.validated_data['periodicity'] == 'Every day':
        return every_day_schedule(date_time_obj, time_from, time_to, doctor)
    else:
        return one_day_schedule(date_time_obj, time_from, time_to, doctor)


def visits_generator(date, time_from, time_to, user):
    """Generates a bunch of visits, for range of dates"""
    visits = []
    time = time_from
    while time < time_to:
        visits.append(Visit(
            date=date,
            time=time,
            doctor=user
        ))
        time += timedelta(minutes=int(user.visit_duration))
    Visit.objects.bulk_create(visits)


def one_day_schedule(date, time_from, time_to, user):
    """Generates one schedule object for one day"""
    visits_generator(date, time_from, time_to, user)

    return Schedule.objects.create(
        time_from=time_from,
        time_to=time_to,
        date=date,
        doctor=user,
        periodicity='Once'
    )


def every_day_schedule(date, time_from, time_to, user):
    """"Generates schedules for all days in month, starting from chosen date"""
    current_month = date.strftime("%B")
    schedules = []
    while current_month == date.strftime("%B"):
        schedules.append(
            Schedule(
                time_from=time_from,
                time_to=time_to,
                date=date,
                doctor=user,
                periodicity='Every day'
            ))
        visits_generator(date, time_from, time_to, user)
        date += timedelta(days=1)

    return Schedule.objects.bulk_create(schedules)


def every_week_schedule(date, time_from, time_to, user):
    """Generates schedule for certain day of the week for all month, starting from chosen date"""
    current_month = date.strftime("%B")
    schedules = []
    while current_month == date.strftime("%B"):
        schedules.append(
            Schedule(
                time_from=time_from,
                time_to=time_to,
                date=date,
                doctor=user,
                periodicity='Every week'
            ))
        visits_generator(date, time_from, time_to, user)
        date += timedelta(weeks=1)

    return Schedule.objects.bulk_create(schedules)


def except_weekend_schedule(date, time_from, time_to, user):
    """"Generates schedules for all days in month except weekends, starting from chosen date"""
    current_month = date.strftime("%B")
    schedules = []
    if date.isoweekday() > 5:
        raise APIException('')
    while current_month == date.strftime("%B"):
        if date.isoweekday() > 5:
            date += timedelta(days=2)
        schedules.append(
            Schedule(
                time_from=time_from,
                time_to=time_to,
                date=date,
                doctor=user,
                periodicity='Except weekend'
            ))
        visits_generator(date, time_from, time_to, user)
        date += timedelta(days=1)
    return Schedule.objects.bulk_create(schedules)
