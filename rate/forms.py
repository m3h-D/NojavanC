from django import forms
from .models import Rate


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('rating',)

    def __init__(self, *args, **kwargs):
        try:
            self.requested_user = kwargs.pop("user")
            self.post = kwargs.pop("post")
        except:
            self.requested_user = None
            self.post = None
        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        rate = super().save(commit=False)
        rate.user = self.requested_user
        rate.post = self.post
        if commit:
            rate.save()
        return rate