from django import forms
from .models import Article


class ModelArticle(forms.ModelForm):
    class Meta:
        model = Article

        fields = {
            'title',
            'scene',
            'content',

        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control inp",
                'placeholder': 'Headline'

            }),

            'content': forms.Textarea(attrs={
                'class': "form-control inp",
                'placeholder': 'Story...'

            }),
        }


class Upvote(forms.Form):
    title = ""
    vote = 1

