from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError

from catalog.models import Article, Redactor


class ArticleForm(forms.ModelForm):
    redactors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Article
        fields = "__all__"


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    # def clean_license_number(self):  # this logic is optional, but possible
    #     return validate_license_number(self.cleaned_data["license_number"])


class RedactorExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["years_of_experience"]

    # def clean_license_number(self):
    #     return validate_license_number(self.cleaned_data["license_number"])


# def validate_license_number(
#     license_number,
# ):  # regex validation is also possible here
#     if len(license_number) != 8:
#         raise ValidationError("License number should consist of 8 characters")
#     elif not license_number[:3].isupper() or not license_number[:3].isalpha():
#         raise ValidationError("First 3 characters should be uppercase letters")
#     elif not license_number[3:].isdigit():
#         raise ValidationError("Last 5 characters should be digits")
#
#     return license_number


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
