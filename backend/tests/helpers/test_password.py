import pytest
from apps.portal.helpers.password import (PasswordStrength,
                                          clean_password_helper)
from django import forms


@pytest.mark.parametrize(
    "password_field_name,password,strength", [
        ("password","aBcd!@#$12", PasswordStrength.TEACHER),
        ("password","Abcd$_)(*34", PasswordStrength.TEACHER),
    ]
)
def test_password_strength_is_enough(object, password_field_name, password, strength):
    object.cleaned_data[password_field_name] = password

    assert clean_password_helper(object, password_field_name, strength) == password


@pytest.mark.parametrize(
    "password_field_name,password,strength", [
        ("password","123456", PasswordStrength.TEACHER),
        ("password","Len<10", PasswordStrength.TEACHER),
        ("password","only_have_lowercase", PasswordStrength.TEACHER),
        ("password","ONLY_HAVE_UPPERCASE", PasswordStrength.TEACHER),
        ("password","HAve_No_Special_char", PasswordStrength.TEACHER),
    ]
)
def test_password_strength_is_not_enough(object, password_field_name, password, strength):
    object.cleaned_data[password_field_name] = password

    with pytest.raises(forms.ValidationError):
        clean_password_helper(object, password_field_name, strength)
