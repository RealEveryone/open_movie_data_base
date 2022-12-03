from django import forms

from open_movie_data_base.common.models import Review
from open_movie_data_base.movie.models import Movie


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(
                attrs={
                    'rows': 5,
                    'cols': 60
                }
            ),
            'rating': forms.NumberInput(
                attrs={
                    'type': 'range',
                    'step': 0.25,
                    'min': Review.MIN_RATING_NUM,
                    'max': Review.MAX_RATING_NUM,
                    'id': 'customRange2',
                }
            )

        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        return float(rating)
