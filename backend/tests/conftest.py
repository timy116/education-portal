import pytest


class Object:
    """
    Test for password strength.
    """

    def __init__(self):
        self.cleaned_data = {}


@pytest.fixture
def object():
    return Object()
