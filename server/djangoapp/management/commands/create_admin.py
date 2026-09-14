import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "ينشئ superuser تلقائياً من متغيرات البيئة إذا لم يكن موجوداً"

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write('DJANGO_SUPERUSER_USERNAME/PASSWORD غير موجودين، تم التخطي.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'المستخدم {username} موجود مسبقاً، تم التخطي.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'تم إنشاء superuser: {username}'))