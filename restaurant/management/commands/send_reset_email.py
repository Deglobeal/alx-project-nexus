from django.core.management.base import BaseCommand
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# Management command to send password reset email to a user
# Usage: python manage.py send_reset_email <user_email>
class Command(BaseCommand):
    help = "Send password reset email to a user"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    def handle(self, *args, **options):
        email = options["email"]
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_link = f"http://localhost:8000/reset-password/{user.pk}/{token}/"
# In production, send via email
            send_mail(
                "Password Reset",
                f"Click the link to reset password: {reset_link}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            self.stdout.write(self.style.SUCCESS(f"Password reset email sent to {email}"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("User not found"))
