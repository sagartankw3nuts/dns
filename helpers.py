from django.utils import timezone
import uuid
from datetime import timedelta

def generate_custom_token():
    return uuid.uuid4()

def calculate_expiration():
    return timezone.now() + timedelta(days=1)

def is_expired(expiration_date):
    return timezone.now() > expiration_date