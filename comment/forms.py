from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comments
        fields = ('content',)