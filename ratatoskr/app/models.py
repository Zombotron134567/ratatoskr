from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from .calendarutil import create_calendar_for_schedule, update_timeslot_event

# Create your models here.

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    is_locked = models.BooleanField()
    auto_lock_after = models.DateTimeField()
    # These fields are filled automatically
    calendar_id = models.CharField(max_length=1024)
    calendar_meet_data = models.JSONField()
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            (self.calendar_meet_data, self.calendar_id) = create_calendar_for_schedule(self)
        super().save(force_insert, force_update)

class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(to=Schedule, on_delete=models.CASCADE)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    auto_lock_after = models.DateTimeField()
    is_locked = models.BooleanField()
    reservation_limit = models.IntegerField()

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=747)
    time_slot = models.ForeignKey(to=TimeSlot, on_delete=models.CASCADE)
    email = models.EmailField()
    comment = models.CharField(max_length=256)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            update_timeslot_event(self.time_slot)
        super().save(force_insert, force_update)
