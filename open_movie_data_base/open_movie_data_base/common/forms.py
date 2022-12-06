from django import forms

from open_movie_data_base.common.models import Review


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
                    'step': 0.01,
                    'min': Review.MIN_RATING_NUM,
                    'max': Review.MAX_RATING_NUM,
                    'id': 'slider',
                }
            )

        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        return float(rating)
