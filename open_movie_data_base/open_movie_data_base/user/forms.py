from enum import Enum

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.admin.widgets import FilteredSelectMultiple

from open_movie_data_base.user.models import RegularUser, MovieDirector, Actor
from open_movie_data_base.utils.mixins import ChoicesMixin

UserModel = get_user_model()


class UserSignInForm(AuthenticationForm):
    error_messages = {
        "invalid_login":
            "Please enter a correct %(username)s and password. Note that both "
            "fields are case-sensitive."}


class UserTypesChoices(ChoicesMixin, Enum):
    User = 'User'
    Actor = 'Actor'
    MovieDirector = 'Movie Director'


class AppUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control form-control-lg'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control form-control-lg'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'type_of_user']
        field_classes = {'username': UsernameField}
        widgets = {
            'type_of_user': forms.RadioSelect(

            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_placeholders()

    def set_placeholders(self):
        for _, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class GenericProfileEditForm(forms.ModelForm):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_forms_with_classes()

    def append_forms_with_classes(self):
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if name == 'birth_date':
                field.widget = forms.DateInput(
                    attrs={
                        'type': 'date',
                        'class': 'form-control'
                    }
                )


class MovieDirectorEditForm(GenericProfileEditForm):
    class Meta:
        model = MovieDirector
        exclude = ['user', 'slug', 'description']


class RegularUserEditForm(GenericProfileEditForm):
    class Meta:
        model = RegularUser
        exclude = ['user', 'slug']


class ActorEditForm(GenericProfileEditForm):
    class Meta:
        model = Actor
        exclude = ['user', 'slug', 'description']
