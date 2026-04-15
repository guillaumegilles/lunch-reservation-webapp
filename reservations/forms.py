from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)


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
