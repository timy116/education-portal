import threading
import uuid
import factory
from django.conf import settings
from django.utils import timezone
import datetime


class Factory(factory.django.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1

            return cls._SEQUENCE


class UserFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@email.com")
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.username))


class EmailVerificationFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "portal.EmailVerification"

    user = factory.SubFactory("tests.factories.UserFactory")
    token = factory.LazyAttribute(lambda obj: uuid.uuid4().hex[:30])
    email = factory.LazyAttribute(lambda obj: obj.user.email)
    expiry = factory.LazyAttribute(lambda obj: timezone.now() + datetime.timedelta(hours=1))


class UserProfileFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "portal.UserProfile"

    user = factory.SubFactory("tests.factories.UserFactory")


class TeacherFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "portal.Teacher"

    user_profile = factory.SubFactory("tests.factories.UserProfileFactory")
    user = factory.SubFactory("tests.factories.UserFactory")
