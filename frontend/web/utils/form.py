from django import forms
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    r"^\d{10}$",
    message="Phone number does not match the required format",
)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
    phone = forms.CharField(
        max_length=16,
        required=True,
        validators=[phone_validator],
        help_text="Phone number must be 10 digits long, e.g. 07774444555",
    )
