from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '회원가입 유저 테스트'

    def handle(self, *args, **options):
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'dummyuser{i}',
                defaults={
                    'email': f'dummy{i}@test.com',
                    'password': 'test1234!',
                    'name': f'테스트{i}',
                    'birth': '2001-01-01',
                    'phone': f'010-0000-00{i}',
                    'address': f'서울시 어딘가 {i}',
                    'zipcode': f'1234{i}',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {user.username}'))
