import pytest
from django.urls import reverse

from apps.portal.forms.teacher import TeacherRegisterForm

pytestmark = pytest.mark.django_db


@pytest.fixture
def fields():
    return TeacherRegisterForm().fields


@pytest.fixture
def register_form():
    teacher_prefix = "teacher_reg"

    return {
        f"{teacher_prefix}-first_name": "XIAO-MING",
        f"{teacher_prefix}-last_name": "WANG",
        f"{teacher_prefix}-email": "user@email.com",
        f"{teacher_prefix}-password": "!DummyPass1word2@",
        f"{teacher_prefix}-confirm_password": "!DummyPass1word2@",
    }


def test_first_name_is_empty(client, register_form, fields):
    f = fields["first_name"]
    register_form["teacher_reg-first_name"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


def test_first_name_is_too_long(client, register_form, fields):
    f = fields["first_name"]
    register_form["teacher_reg-first_name"] = "Xaioooooo Minggg"

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["max_length"] % {'limit_value': f.max_length}


INVALID_FIRST_NAME = [
    '1Amy',
    '!Amy',
    ' Amy',
    '艾!咪'
    '艾咪_'
]


@pytest.mark.parametrize("first_name", INVALID_FIRST_NAME)
def test_first_name_is_invalid(client, register_form, fields, first_name):
    f = fields["first_name"]
    register_form["teacher_reg-first_name"] = first_name

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["invalid"]
