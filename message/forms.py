from django import forms
from .models import Message



class SendMessageForm(forms.ModelForm):
    """a form for sending message that includes all fields except sender, reciever and is_readed

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    # content = forms.CharField(required=False)
    class Meta:
        model = Message
        fields = ['content',]

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('user')
        self.th_content = kwargs.pop('ajax_content', None)
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False
    
    def save(self, commit=True):
        message = super().save(commit=False)
        message.sender = self.sender
        if self.th_content:
            message.content = self.th_content
        if commit:
            message.save()
        return message