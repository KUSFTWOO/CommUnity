#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.notices.models import Notice
from apps.board.models import Post
from apps.accounts.models import CustomUser

# Get a staff user to create notice
user = CustomUser.objects.filter(is_staff=True).first()
if user:
    # Create a test notice
    notice = Notice.objects.create(
        title="Testing Search Feature",
        content="This is a test notice for searching functionality",
        author=user,
        is_important=False
    )
    print(f"OK: Created notice '{notice.title}'")

# Create a test post
author = CustomUser.objects.filter(email='user1@example.com').first()
if author:
    post = Post.objects.create(
        title="Search Test Post",
        content="This post is for testing the search functionality",
        author=author
    )
    print(f"OK: Created post '{post.title}'")
