from enum import Enum

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.admin.widgets import FilteredSelectMultiple

from open_movie_data_base.user.models import RegularUser, MovieDirector, Actor
from open_movie_data_base.utils.mixins import ChoicesMixin

UserModel = get_user_model()


class UserTypesChoices(ChoicesMixin, Enum):
    User = 'User'
    Actor = 'Actor'
    MovieDirector = 'Movie Director'


class AppUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'type_of_user']
        field_classes = {'username': UsernameField}
        widgets = {
            'type_of_user': forms.RadioSelect(

            )
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
        exclude = ['user', 'slug']


class RegularUserEditForm(GenericProfileEditForm):
    class Meta:
        model = RegularUser
        exclude = ['user', 'slug']


class ActorEditForm(GenericProfileEditForm):
    class Meta:
        model = Actor
        exclude = ['user', 'slug']
