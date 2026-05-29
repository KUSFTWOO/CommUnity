#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.surveys.models import Survey
from django.utils import timezone

survey = Survey.objects.first()
if survey:
    print(f"Survey: {survey.title}")
    print(f"Created: {survey.created_at}")
    print(f"Expires: {survey.expires_at}")
    print(f"Now: {timezone.now()}")
    print(f"Is Expired: {survey.is_expired}")
