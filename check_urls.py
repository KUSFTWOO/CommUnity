import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse

try:
    url = reverse('dashboard:notices')
    print(f"Success: {url}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e).__name__}")

# Check URL patterns
from django.urls import get_resolver
resolver = get_resolver()
dashboard_urls = []

# Find dashboard URLs
for pattern in resolver.url_patterns:
    if 'dashboard' in str(pattern):
        print(f"\nFound pattern: {pattern}")
        if hasattr(pattern, 'url_patterns'):
            for sub in pattern.url_patterns:
                dashboard_urls.append(str(sub))
                print(f"  - {sub}")

print(f"\nTotal dashboard URLs found: {len(dashboard_urls)}")
