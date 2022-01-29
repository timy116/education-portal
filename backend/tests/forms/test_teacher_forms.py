import pytest
from django.urls import reverse

from apps.portal.email.message import SUBJECT_PREFIX
from apps.portal.forms.teacher import TeacherRegisterForm
from apps.portal.helpers.password import ERROR_MESSAGE as PASSWORD_ERROR_MESSAGE

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
        "g-recaptcha-response": "dummy_recaptcha",
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


def test_last_name_is_empty(client, register_form, fields):
    f = fields["last_name"]
    register_form["teacher_reg-last_name"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


def test_last_name_is_too_long(client, register_form, fields):
    f = fields["last_name"]
    register_form["teacher_reg-last_name"] = "Wangggggggg"

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["max_length"] % {'limit_value': f.max_length}


INVALID_LAST_NAME = [
    '1Wang',
    '!Wang',
    ' Wang',
    'Wang!'
    'Wang_'
]


@pytest.mark.parametrize("last_name", INVALID_FIRST_NAME)
def test_last_name_is_invalid(client, register_form, fields, last_name):
    f = fields["last_name"]
    register_form["teacher_reg-first_name"] = last_name

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["invalid"]


def test_email_is_empty(client, register_form, fields):
    f = fields["email"]
    register_form["teacher_reg-email"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


INVALID_EMAIL = [
    'amy',
    'amy wu@',
]


@pytest.mark.parametrize("email", INVALID_EMAIL)
def test_email_is_invalid(client, register_form, fields, email):
    f = fields["email"]
    register_form["teacher_reg-email"] = email

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["invalid"]


def test_password_is_empty(client, register_form, fields):
    f = fields["password"]
    register_form["teacher_reg-password"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


INVALID_PASSWORD = [
    "654321",
    "abcdefg",
    "ABCDEFG",
    "!@#$%",
    "12345abcdef",
    "12345Abcdef",
    "!2345Abcd",
]


@pytest.mark.parametrize("password", INVALID_PASSWORD)
def test_password_is_invalid(client, register_form, password):
    register_form["teacher_reg-password"] = password

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == PASSWORD_ERROR_MESSAGE % 10


def test_register_successful(client, register_form, outbox):
    resp = client.post(path=reverse("register"), data=register_form)

    assert resp.context["is_teacher"] == True
    assert resp.context["obj"] is not None
