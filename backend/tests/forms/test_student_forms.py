import pytest
from django.urls import reverse

from apps.portal.forms.student import IndependentStudentRegisterForm, BaseLoginForm
from apps.portal.helpers.password import ERROR_MESSAGE as PASSWORD_ERROR_MESSAGE
from tests import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def fields():
    return IndependentStudentRegisterForm().fields


@pytest.fixture
def register_form():
    ind_prefix = "ind_reg"

    return {
        f"{ind_prefix}-name": "XIAO-MING WANG",
        f"{ind_prefix}-username": "xiao-ming",
        f"{ind_prefix}-email": "user@email.com",
        f"{ind_prefix}-password": "Dummy1Password",
        f"{ind_prefix}-confirm_password": "Dummy1Password",
        "g-recaptcha-response": "dummy_recaptcha",
    }


"""
 ############################
 ### Testing RegisterForm ###
 ############################
"""


def test_name_is_empty(client, register_form, fields):
    f = fields["name"]
    register_form["ind_reg-name"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


INVALID_NAME = [
    '1XIAO-MING WANG',
    '!XIAO-MING WANG',
    ' XIAO-MING WANG',
    '王小!明'
    '王小明_'
]


@pytest.mark.parametrize("name", INVALID_NAME)
def test_name_is_invalid(client, register_form, fields, name):
    f = fields["name"]
    register_form["ind_reg-name"] = name

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["invalid"]


def test_name_is_too_long(client, register_form, fields):
    f = fields["name"]
    register_form["ind_reg-name"] = "XIAO-MING WANGGGGGGGGGGGGG"

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["max_length"] % {'limit_value': f.max_length}


def test_username_is_empty(client, register_form, fields):
    f = fields["username"]
    register_form["ind_reg-username"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


INVALID_USERNAME = [
    '1XIAO-MING WANG',
    '!XIAO-MING WANG',
    ' XIAO-MING WANG',
]


@pytest.mark.parametrize("username", INVALID_USERNAME)
def test_username_is_invalid(client, register_form, fields, username):
    f = fields["username"]
    register_form["ind_reg-username"] = username

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["invalid"]


def test_username_is_too_long(client, register_form, fields):
    f = fields["username"]
    register_form["ind_reg-username"] = "xiao-ming-wanggggggggggggg"

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["max_length"] % {'limit_value': f.max_length}


def test_email_is_empty(client, register_form, fields):
    f = fields["email"]
    register_form["ind_reg-email"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


INVALID_EMAIL = [
    'amy',
    'amy wu@',
]


@pytest.mark.parametrize("email", INVALID_EMAIL)
def test_email_is_invalid(client, register_form, fields, email):
    f = fields["email"]
    register_form["ind_reg-email"] = email

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["invalid"]


def test_password_is_empty(client, register_form, fields):
    f = fields["password"]
    register_form["ind_reg-password"] = ""

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == f.error_messages["required"]


INVALID_PASSWORD = [
    "654321",
    "abcdefg",
    "ABCDEFG",
    "12345abcdef",
    "12345ABCDEF",
]


@pytest.mark.parametrize("password", INVALID_PASSWORD)
def test_password_is_invalid(client, register_form, password):
    register_form["ind_reg-password"] = password

    resp = client.post_soup(path=reverse("register"), data=register_form)
    assert resp.select(".errorlist")[0].text == PASSWORD_ERROR_MESSAGE % 8


def test_password_does_not_match(client, register_form):
    register_form["ind_reg-password"] = "Dummy1Password2"

    resp = client.post_soup(path=reverse("register"), data=register_form)
    error_msg = IndependentStudentRegisterForm.error_messages["password_does_not_match"]

    assert resp.select(".errorlist")[0].text == error_msg
    assert resp.select(".errorlist")[1].text == error_msg


def test_register_successful(client, register_form):
    resp = client.post(path=reverse("register"), data=register_form)

    assert resp.context["is_teacher"] is False
    assert resp.context["obj"] is not None


"""
 ############################
 ### Testing LoginForm ######
 ############################
"""


@pytest.fixture
def login_form():
    return {
        "username": "dummy-user",
        "password": "Dummy1Password",
    }


def test_user_does_not_exist(client, login_form):
    resp = client.post_soup(path=reverse("independent_student_login"), data=login_form)
    error_msg = BaseLoginForm.error_messages["invalid_login"]

    assert resp.select(".errorlist")[0].text == error_msg


def test_invalid_username(client):
    user = f.UserFactory.create()
    form = {"username": f"{user.username}-extra", "password": user.username}
    resp = client.post_soup(path=reverse("independent_student_login"), data=form)
    error_msg = BaseLoginForm.error_messages["invalid_login"]

    assert resp.select(".errorlist")[0].text == error_msg


def test_invalid_password(client):
    user = f.UserFactory.create()
    form = {"username": user.username, "password": f"{user.username}-extra"}
    resp = client.post_soup(path=reverse("independent_student_login"), data=form)
    error_msg = BaseLoginForm.error_messages["invalid_login"]

    assert resp.select(".errorlist")[0].text == error_msg


def test_account_is_not_independent_student(client):
    teacher = f.TeacherFactory.create()

    form = {"username": teacher.user.username, "password": teacher.user.username}
    resp = client.post_soup(path=reverse("independent_student_login"), data=form)
    error_msg = BaseLoginForm.error_messages["invalid_login"]

    assert resp.select(".errorlist")[0].text == error_msg


def test_account_is_inactive(client):
    ind_student = f.StudentFactory.create()
    f.EmailVerificationFactory.create(user=ind_student.user)

    form = {"username": ind_student.user.username, "password": ind_student.user.username}
    resp = client.post_soup(path=reverse("independent_student_login"), data=form)
    error_msg = BaseLoginForm.error_messages["inactive"]

    assert resp.select(".errorlist")[0].text == error_msg


def test_login_success(client):
    ind_student = f.StudentFactory.create()
    f.EmailVerificationFactory.create(user=ind_student.user, verified=True)

    form = {"username": ind_student.user.username, "password": ind_student.user.username}
    resp = client.post(path=reverse("independent_student_login"), data=form)

    assert "dashboard/independent/" in resp["Location"]
