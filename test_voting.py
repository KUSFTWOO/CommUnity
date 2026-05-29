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
    # Get options
    options = poll.options.all()
    print(f"  Options: {', '.join([opt.text for opt in options])}")

    # Get a test user
    user = CustomUser.objects.filter(email='user1@example.com').first()
    if user:
        print(f"  Test User: {user.nickname}")

        # Check if user has already voted
        existing_vote = Vote.objects.filter(poll=poll, user=user).first()
        if existing_vote:
            print(f"  User already voted for: {existing_vote.option.text}")
        else:
            print(f"  User has not voted yet")

            # Create a vote
            option = options.first()
            vote = Vote.objects.create(poll=poll, user=user, option=option)
            print(f"  OK: Created vote for: {option.text}")

            # Verify vote count
            vote_count = Vote.objects.filter(poll=poll).count()
            print(f"  Total votes on poll: {vote_count}")

            # Verify the option vote count is updated
            option.refresh_from_db()
            print(f"  Votes for {option.text}: {option.votes_count}")
