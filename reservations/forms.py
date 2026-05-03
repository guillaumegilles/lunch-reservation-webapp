from django import forms
from django.core.validators import RegexValidator

IDENTIFIER_REGEX = r"^[A-Za-z][0-9]{6}$"
identifier_validator = RegexValidator(
    regex=IDENTIFIER_REGEX,
    message="Format attendu : 1 lettre suivie de 6 chiffres (ex: K589479).",
)


class LoginForm(forms.Form):
    identifier = forms.CharField(min_length=7, max_length=7, validators=[identifier_validator])
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    identifier = forms.CharField(min_length=7, max_length=7, validators=[identifier_validator])
    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=150, widget=forms.PasswordInput)


class WeeklyMenuForm(forms.Form):
    week_start = forms.DateField(
        label="Semaine du (lundi)",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    monday_menu = forms.CharField(max_length=200, label="Lundi")
    tuesday_menu = forms.CharField(max_length=200, label="Mardi")
    wednesday_menu = forms.CharField(max_length=200, label="Mercredi")
    thursday_menu = forms.CharField(max_length=200, label="Jeudi")
    friday_menu = forms.CharField(max_length=200, label="Vendredi")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class SuggestionForm(forms.Form):
    text = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        label="Votre suggestion ou amelioration",
        help_text="Partagez vos idees pour ameliorer l'application (500 caracteres maximum)"
    )
