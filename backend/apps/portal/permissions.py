from django.contrib.auth import get_user_model

User = get_user_model()


def teacher_login(user: User):
    try:
        if user.userprofile.teacher:
            return True
    except AttributeError:
        return False


def student_login(user: User):
    try:
        if user.userprofile.student:
            return True
    except AttributeError:
        return False


def independent_student_login(user: User):
    return student_login(user) and user.userprofile.student.is_independent()
