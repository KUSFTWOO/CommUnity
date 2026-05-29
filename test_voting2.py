#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.votes.models import Poll, PollOption, Vote
from apps.accounts.models import CustomUser

# Get an existing poll
poll = Poll.objects.first()
print(f"Testing Poll: {poll.question if poll else 'No polls found'}")

if poll:
    # Get the second option (JavaScript)
    option = poll.options.filter(text='JavaScript').first()
    if not option:
        option = poll.options.all()[1]  # fallback to second option

    # Get a different test user
    user = CustomUser.objects.filter(email='user2@example.com').first()
    if user:
        print(f"Test User: {user.nickname}")

        # Check if user has already voted
        existing_vote = Vote.objects.filter(poll=poll, user=user).first()
        if existing_vote:
            print(f"User already voted for: {existing_vote.option.text}")
        else:
            # Create a vote the correct way (as the view does)
            vote = Vote.objects.create(poll=poll, user=user, option=option)

            # Increment the vote count
            option.votes_count += 1
            option.save(update_fields=['votes_count'])

            print(f"OK: Created vote for: {option.text}")
            print(f"Vote count for {option.text}: {option.votes_count}")

            # Get total votes
            total = poll.total_votes
            print(f"Total votes on poll: {total}")
