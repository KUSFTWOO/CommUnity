from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser account for admin access"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="admin@example.com",
            help="Admin email address",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="admin123",
            help="Admin password",
        )

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]

        # Check if admin already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"✓ Admin account '{email}' already exists. Skipping creation."
                )
            )
            return

        # Create superuser
        try:
            admin_user = User.objects.create_superuser(
                username=email.split("@")[0],  # username from email
                email=email,
                password=password,
                nickname="Administrator",
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Admin account created successfully!"
                )
            )
            self.stdout.write(f"  Email: {email}")
            self.stdout.write(f"  Username: {admin_user.username}")
            self.stdout.write(f"  Access: /admin/")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"✗ Failed to create admin account: {str(e)}")
            )
