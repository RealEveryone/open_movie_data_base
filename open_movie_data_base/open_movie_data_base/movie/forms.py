import django.db.utils
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from open_movie_data_base.movie.models import Movie, MovieGenres


class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['movie_director']
        widgets = {
            'release_date': forms.DateInput(
                attrs={'type': 'text',
                       'onfocus': "(this.type='date')", }
            ),
            'description': forms.Textarea(
                attrs={
                    'cols': 5,
                    'rows': 5
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_class()
        self.set_placeholder()

    def set_form_class(self):
        for name, field in self.fields.items():
            if name == 'movie_poster':
                continue
            field.widget.attrs['class'] = 'form-control form-control-lg'

    def set_placeholder(self):
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class MovieEditForm(AddMovieForm):
    class Meta:
        model = Movie
        exclude = ['movie_director']
        widgets = {
            'release_date': forms.DateInput(
                attrs={'type': 'text',
                       'onfocus': "(this.type='date')", }
            ),
            'description': forms.Textarea(
                attrs={
                    'cols': 5,
                    'rows': 5
                }
            ),
        }


class DisplayGenresForm(forms.ModelForm):
    class Meta:
        model = MovieGenres
        fields = ('category',)

    genres = forms.ModelChoiceField(
        queryset=MovieGenres.objects.all(),
        widget=forms.Select(attrs={'class': 'btn btn-dark'}),
        empty_label='Genres', required=False,

    )
