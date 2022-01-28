import pytest
from bs4 import BeautifulSoup


class Object:
    """
    Test for password strength.
    """

    def __init__(self):
        self.cleaned_data = {}


@pytest.fixture
def object():
    return Object()


@pytest.fixture
def outbox():
    from django.core import mail

    return mail.outbox


@pytest.fixture
def client():
    from django.test.client import Client

    class _Client(Client):

        def get_soup(self, *args, **kwargs):
            response = self.get(*args, **kwargs)

            return BeautifulSoup(response.render().content, "lxml")

        def post_soup(self, *args, **kwargs):
            response = self.post(*args, **kwargs)

            try:
                return BeautifulSoup(response.render().content, "lxml")
            except AttributeError:
                return BeautifulSoup(response.content, "lxml")

    return _Client()
