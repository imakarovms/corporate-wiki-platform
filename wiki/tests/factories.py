import factory
from django.contrib.auth import get_user_model
from wiki.models import Category, Tag, Article

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'defaultpass123')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower())

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower())

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
    title = factory.Faker('sentence')
    slug = factory.LazyAttribute(lambda obj: obj.title.lower().replace(' ', '-').rstrip('.'))
    content = factory.Faker('text')
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    status = 'PUBLISHED'