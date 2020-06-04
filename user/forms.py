from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Group, Profile
from nojavan.utils import create_slug
from random import randint
import uuid
import re

User = get_user_model()

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'is_active', 'is_compeleted',  'is_accepted', 'national_code')

    def clean_password(self):
        return self.initial["password"]



class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120, widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("چنین مشخصاتی وجود ندارد")
            return super(LoginForm, self).clean(*args, **kwargs)




class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email')
    
    def __init__(self, *args, **kwargs):
        self.timer = kwargs.pop('timer', None)
        super().__init__(*args, **kwargs)
        del self.fields['password2']

    def clean(self, *args, **kwargs):
        if self.timer and self.timer >= timezone.now():
            raise forms.ValidationError("لطفا بعدا تلاش کنید'")
        else:
            try:
                del self.timer
            except:
                pass
        return super().clean(*args, **kwargs)


    def clean_password1(self, *args, **kwargs):
        password = self.cleaned_data.get('password1')
        regexp = re.compile(r'[A-Za-z]')
        regexp_num = re.compile(r'[0-9]')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("حداقل باید شامل 8 کاراکتر باشد")
            if not regexp.search(password) or not regexp_num.search(password):
                raise forms.ValidationError("باید شامل حرف و عدد باشد")
            return password

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.is_active = False
        if email:
            if not User.objects.filter(username=str(email).split('@')[0]).exists():
                user.username = str(email).split('@')[0]
            else:
                user.username = str(email).split('@')[0] + "_" +f"{uuid.uuid4()}".split('-')[-1]

            if commit:
                user.save()
        return user 


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'first_name', 'last_name', 'sex', 'national_code')

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.is_active = False
        if email:
            if not User.objects.filter(username=str(email).split('@')[0]).exists():
                user.username = str(email).split('@')[0]
            else:
                user.username = str(email).split('@')[0] + "_" +f"{uuid.uuid4()}".split('-')[-1]

            if commit:
                user.save()
        return user 


class VerificationForm(forms.Form):
    code = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.validate = kwargs.pop('session')
        self.expire_time = kwargs.pop('expire_time')
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if self.expire_time and self.expire_time <= timezone.now():
            raise forms.ValidationError("کد اعتبار سنجی شما منقضی شد. لطفا یکبار دیگر برای ارسال کد اقدام کنید")
        if str(code) != str(self.validate['sms_validate']):
            raise forms.ValidationError("مقدار وارد شده اشتباه است")
        return code




class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("چنین ایمیلی موجود نیست.")
        return super(ForgetPasswordForm, self).clean(*args, **kwargs)


class NewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        new_password = self.cleaned_data.get('new_password')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password and new_password2 and new_password != new_password2:
            raise forms.ValidationError("رمز عبور وارد شده برابر نیست")
        return super(NewPasswordForm, self).clean(*args, **kwargs)


class GroupForm(forms.ModelForm):
    slug = forms.SlugField(required=False)
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
    

    def save(self, commit=True):
        group = super().save(commit=False)
        slug = self.cleaned_data.get("slug")
        if not self.request.user.is_staff:
            group.owner = self.request.user
        if not slug:
            group.slug = create_slug(group)
            if commit:
                group.save()
        return slug 


class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ('username','phone', 'email', 'first_name', 'last_name','national_code', 'sex')

    def clean_password(self, *args, **kwargs):
        import re
        password = self.cleaned_data.get('password')
        regexp = re.compile(r'[A-Za-z]')
        regexp_num = re.compile(r'[0-9]')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("حداقل باید شامل 8 کاراکتر باشد")
            if not regexp.search(password) or not regexp_num.search(password):
                raise forms.ValidationError("باید شامل حرف و عدد باشد")
            return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_compeleted = True
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user 

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)