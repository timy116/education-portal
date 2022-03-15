import hashlib
import random
import string
from uuid import uuid4
from django.shortcuts import reverse

from ..models import Class


def generate_access_code():
    while True:
        access_code = "".join(random.choice(string.ascii_uppercase) for _ in range(5))

        if not Class.objects.filter(access_code=access_code).exists():
            return access_code


def generate_password(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_login_id() -> turtle:
    login_id = uuid4().hex
    hashed_login_id = get_hashed_login_id(login_id)

    return login_id, hashed_login_id


def get_hashed_login_id(login_id: str):
    return hashlib.sha256(login_id.encode()).hexdigest()


def generate_student_url(request, student, login_id):
    return request.build_absolute_uri(
        reverse("student_direct_login",kwargs={"user_id": student.new_user.id, "login_id": login_id})
    )
