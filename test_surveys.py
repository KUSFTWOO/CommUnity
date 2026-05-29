#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.surveys.models import Survey, Question, Response, Answer
from apps.accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta

# Create a test survey if none exists
surveys = Survey.objects.all()
print(f"Total Surveys: {surveys.count()}")

if surveys.count() == 0:
    user = CustomUser.objects.filter(is_staff=True).first()
    if user:
        # Create a survey
        survey = Survey.objects.create(
            title="Python vs JavaScript",
            description="Which language do you prefer?",
            is_anonymous=True,
            created_by=user,
            expires_at=timezone.now() + timedelta(days=7)
        )

        # Create questions
        q1 = Question.objects.create(
            survey=survey,
            text="Do you use Python?",
            question_type='CHOICE',
            required=True,
            options="Yes\nNo\nMaybe",
            order=1
        )

        q2 = Question.objects.create(
            survey=survey,
            text="How many years of experience?",
            question_type='SCALE',
            required=True,
            order=2
        )

        print(f"OK: Created survey '{survey.title}'")
        print(f"Questions: {survey.questions.count()}")
else:
    survey = surveys.first()
    print(f"Survey: {survey.title}")
    print(f"Questions: {survey.questions.count()}")
    print(f"Responses: {survey.responses.count()}")

    # Try creating a response
    user = CustomUser.objects.filter(email='user2@example.com').first()
    if user:
        # Check if user already responded
        existing = Response.objects.filter(survey=survey, respondent=user).exists()
        if existing:
            print(f"User already responded")
        else:
            # Create a response
            response = Response.objects.create(survey=survey, respondent=user)

            # Add answers
            for question in survey.questions.all():
                answer = Answer.objects.create(
                    response=response,
                    question=question,
                    answer_text="Yes" if question.question_type == 'CHOICE' else "5"
                )

            print(f"OK: Created response from {user.nickname}")
            print(f"Survey now has {survey.responses.count()} responses")
