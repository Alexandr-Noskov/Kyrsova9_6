from django.core.management import BaseCommand

from users.models import User
import os
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(os.getenv("SUPERUSER_PASSWORD"))
        user.save()