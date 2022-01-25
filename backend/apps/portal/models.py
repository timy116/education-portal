from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    can_view_aggregated_data = models.BooleanField(default=False)
    developer = models.BooleanField(default=False)
    awaiting_email_verification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def joined_recently(self):
        now = timezone.now()

        return now - timedelta(days=7) <= self.user.date_joined


class EmailVerification(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="email_verifications", null=True, blank=True
    )
    token = models.CharField(max_length=30)
    email = models.CharField(max_length=200, null=True,
                             default=None, blank=True)
    expiry = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Email verification for {self.user.username}, ({self.email})"


class School(models.Model):
    name = models.CharField(max_length=200)
    postcode = models.CharField(max_length=10)
    town = models.CharField(max_length=200)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    country = CountryField(blank_label="(select country)")
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name

    def classes(self):
        teachers = self.teacher_school.all()

        if teachers:
            classes = []

            for teacher in teachers:
                if teacher.class_teacher.all():
                    classes.extend(list(teacher.class_teacher.all()))

            return classes

        return None


class TeacherManager(models.Manager):
    def factory(self, first_name, last_name, email, password):
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user_profile = UserProfile.objects.create(user=user)

        return Teacher.objects.create(user=user_profile, new_user=user)


class Teacher(models.Model):
    user_profile = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE)
    user = models.OneToOneField(
        to=User,
        related_name="teacher",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    school = models.ForeignKey(
        to=School, related_name="teacher_school", null=True, on_delete=models.SET_NULL
    )
    is_admin = models.BooleanField(default=False)
    pending_join_request = models.ForeignKey(
        to=School,
        related_name="join_request",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    blocked_time = models.DateTimeField(null=True)

    objects = TeacherManager()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def has_school(self):
        return True if self.school else False


class ClassModelManager(models.Manager):
    def all_members(self, user):
        members = []

        if hasattr(user, "teacher"):
            members.append(user.teacher)

            if user.teacher.has_school():
                classes = user.teacher.class_teacher.all()

                for c in classes:
                    members.extend(c.students.all())
        else:
            c = user.student.class_field
            members.append(c.teacher)
            members.extend(c.students.all())

        return members


class Class(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(to=Teacher, related_name="class_teacher", on_delete=models.CASCADE)
    access_code = models.CharField(max_length=5)
    can_view_classmates_data = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    objects = ClassModelManager()

    def __str__(self):
        return self.name

    def has_students(self) -> bool:
        students = self.students.all()

        return students.count() != 0

    class Meta:
        verbose_name_plural = "classes"


class UserSession(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    login_at = models.DateTimeField(default=timezone.now)
    school = models.ForeignKey(to=School, null=True, on_delete=models.SET_NULL)
    class_field = models.ForeignKey(to=Class, null=True, on_delete=models.SET_NULL)
    login_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user}, login at: {self.login_at} type: {self.login_type}"


class StudentManager(models.Manager):
    def get_random_username(self):
        while True:
            random_username = uuid4().hex[:30]

            if not User.objects.filter(username=random_username).exists():
                return random_username

    def schoolFactory(self, klass, name, password, login_id=None):
        user = User.objects.create_user(
            username=self.get_random_username(), password=password, first_name=name
        )
        user_profile = UserProfile.objects.create(user=user)

        return Student.objects.create(
            login_id=login_id,
            class_field=klass,
            user_profile=user_profile,
            user=user
        )

    def independentStudentFactory(self, username, name, email, password):
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=name
        )
        user_profile = UserProfile.objects.create(user=user)

        return Student.objects.create(user_profile=user_profile, user=user)

    def independent_students(self) -> list:
        return [
            student for student in Student.objects.all() if student.is_independent()
        ]


class Student(models.Model):
    # For unique direct login url
    login_id = models.CharField(max_length=64, null=True)
    class_field = models.ForeignKey(
        Class, related_name="students", null=True, on_delete=models.CASCADE
    )
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        related_name="new_student",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    pending_class_request = models.ForeignKey(
        to=Class, related_name="class_request", null=True, on_delete=models.SET_NULL
    )
    blocked_time = models.DateTimeField(null=True)

    objects = StudentManager()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def is_independent(self) -> bool:
        return not self.class_field
