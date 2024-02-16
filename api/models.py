from django.db import models
from datetime import date
from dnsdadweb.models import AppCredentials
from enum import Enum

class Status(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    MANUAL = 'manual'
    CLOSED = 'closed'

class Domain(models.Model):
    application = models.ForeignKey(AppCredentials, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    provider = models.CharField(max_length=250)
    connection_time = models.DateField(default=date.today)
    completion_time = models.DateField(default=None, null=True)
    status = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in Status], default=Status.PENDING.value)
    is_active = models.BooleanField(default=True)
    created = models.DateField(default=date.today)
    updated = models.DateField(default=date.today)
    deleted = models.DateField(default=None, null=True)

    def __str__(self):
        return self.name