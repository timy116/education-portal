from django import forms
from ..fields import CharField


class ClassCreationForm(forms.Form):
    class_name = CharField(
        widget=forms.TextInput(attrs={"placeholder": "班級名稱"}),
        help_text="請輸入一個班級名稱",
    )
    classmate_progress = forms.BooleanField(
        label="是否允許學生看到其他同學的進度？",
        widget=forms.CheckboxInput(),
        initial=False,
        required=False,
    )
