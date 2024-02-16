from django.db import models
from django.contrib.auth.models import User
from datetime import date

class AppCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    app_image = models.ImageField(upload_to='app_images/', null=True)
    client_id = models.CharField(max_length=250, unique=True)
    client_secret = models.CharField(max_length=250, unique=True)
    redirect_uris = models.TextField(default=None, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateField(default=date.today)
    updated = models.DateField(default=date.today)
    deleted = models.DateField(default=None, null=True)

    def __str__(self):
        return self.name

class AppCredentialsToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(AppCredentials, on_delete=models.CASCADE)
    token = models.CharField(max_length=250, unique=True)
    expires = models.DateTimeField()
    created = models.DateField(default=date.today)
    updated = models.DateField(default=date.today)

    def __str__(self):
        return self.name

