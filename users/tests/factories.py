import factory
from django.contrib.auth import get_user_model
from users.models import Invitation

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword123')
    role = 'USER'

class ModeratorFactory(UserFactory):
    role = 'MODERATOR'

class AdminFactory(UserFactory):
    role = 'ADMIN'
    is_staff = True
    is_superuser = True

class InvitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invitation

    email = factory.Sequence(lambda n: f"invite{n}@example.com")
    token = factory.Faker('uuid4')
    is_used = False