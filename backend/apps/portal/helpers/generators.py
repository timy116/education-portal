import random
import string
from ..models import Class


def generate_access_code():
    while True:
        access_code = "".join(random.choice(string.ascii_uppercase) for _ in range(5))

        if not Class.objects.filter(access_code=access_code).exists():
            return access_code
