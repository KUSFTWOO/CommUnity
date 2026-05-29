"""Vercel build script: run migrations when DATABASE_URL is configured."""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    import django

    django.setup()

    from django.core.management import call_command

    if os.environ.get("DATABASE_URL"):
        print("Running database migrations...")
        try:
            call_command("migrate", "--noinput")
        except Exception as exc:
            # Allow deploy to finish; fix DATABASE_URL in Vercel if this fails.
            print(f"WARNING: migrate failed: {exc}")
    else:
        print("DATABASE_URL not set; skipping migrations.")

    print("Build complete.")


if __name__ == "__main__":
    main()
    sys.exit(0)
