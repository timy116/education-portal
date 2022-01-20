from datetime import timedelta

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
