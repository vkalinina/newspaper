from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Article, Redactor, Topic


class ArticleForm(forms.ModelForm):
    redactors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Article
        fields = ["title", "content", "published_date", "topic","redactors"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "published_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "topic": forms.Select(attrs={"class": "form-control"}),
            "redactors": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class RedactorCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Password",
        })
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password confirmation",
        })
    )
    class Meta:
        model = Redactor
        fields = ["username", "first_name", "last_name", "years_of_experience"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Username"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last Name"
            }),
            "years_of_experience": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Years of experience",
                "min": "0"
            })
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")

        if password1.isdigit():
            raise forms.ValidationError("Password must contain at least one digit")

        return password1

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters")

        return username

    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")

        if years is not None and years < 0:
            raise forms.ValidationError("Experience must be greater than 0")

        if years is not None and years > 100:
            raise forms.ValidationError("Put a year of experience")

        return years

    def save(self, commit=True):
        redactor = super().save(commit=False)
        redactor.set_password(self.cleaned_data["password1"])
        if commit:
            redactor.save()
        return redactor


class RedactorExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["years_of_experience"]
        widgets = {
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control"}),
        }


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class ArticleSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
