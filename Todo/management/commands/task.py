from django.core.management import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.models import UserDetail
from Todo.models import Todo
from datetime import date


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        user = get_user_model()
        try:
            user.objects.create_user(email='test@gmail.com', password='1234!@#$')
        except:
            print('this is user already exists.')
        finally:
            user_object = user.objects.get(email='test@gmail.com')
            user_detail = UserDetail.objects.get(User_id=user_object)
            if user_detail.FirstName is None:
                user_detail.FirstName = 'test'
                user_detail.save()
            for _ in range(5):
                Todo.objects.create(
                    user=user_object,
                    Title=self.fake.name(),
                    CreateDate=date.today(),
                    Is_active=self.fake.random.choice(['True', 'False']),
                    Completed=True
                )
