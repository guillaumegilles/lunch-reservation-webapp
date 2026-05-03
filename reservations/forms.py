from django import forms


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=1)
    badge_number = forms.CharField(max_length=150, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    badge_number = forms.CharField(max_length=150, widget=forms.PasswordInput)
    confirm_badge_number = forms.CharField(max_length=150, widget=forms.PasswordInput)


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
