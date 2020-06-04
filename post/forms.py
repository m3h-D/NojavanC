from django import forms
from django.contrib.auth.models import User

from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class AddPostForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorUploadingWidget(config_name='default'))
    # author = forms.CharField(widget=forms.HiddenInput, required=False)
    slug = forms.SlugField(required=False, allow_unicode=True)
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image',
                  'content', 'special', 'status', 'video']

    def __init__(self, *args, **kwargs):
        self.requested_user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.requested_user
        if commit:
            post.save()
        return post