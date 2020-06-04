from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from category.models import Favorite
from django.shortcuts import reverse
from nojavan.utils import hash_file_name
# Create your models here.

class User(AbstractUser):
    """a custome user model that use phone number to login
    
    Arguments:
        AbstractBaseUser {CLASS} -- a django built-in class
    
    Returns:
        STRING -- returns user first_name last_name or phone number
    """
    phone_reg = RegexValidator(regex=r'[0][9][0-9]{9,9}$')
    phone = models.CharField(
        validators=[phone_reg],
        max_length=120,
        unique=True
    )
    SEX_TYPE = (
        ('male', 'آقا'),
        ('female', 'خانم'),
    )
    sex = models.CharField(max_length=6, choices=SEX_TYPE)
    national_code = models.CharField(max_length=120, blank=True, null=True, unique=True)
    is_compeleted = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    @property
    def get_absolute_url(self):
        return reverse('user:profile_view', args=[self.username])

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to=hash_file_name)
    favorite = models.ManyToManyField(
        Favorite, related_name='user', blank=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    province = models.CharField(max_length=120, blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(max_length=100, blank=True, null=True)
    skill = models.CharField(max_length=200, blank=True, null=True)
    social_media = models.CharField(max_length=120, blank=True, null=True)
    STUDIED = (
        ('diploma', 'دیپلم'),
        ('associate', 'کاردانی'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),

    )
    grade = models.CharField(max_length=70, blank=True,
                             null=True, choices=STUDIED)
    cv = models.FileField(blank=True, null=True)
    following = models.ManyToManyField(User, blank=True, related_name="followers")
    # is_accepted = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username



class Group(models.Model):
    owner = models.ForeignKey(User, related_name='groupowner', blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True, allow_unicode=True)
    members = models.ManyToManyField(User, related_name='groupteam', blank=True)
    logo = models.ImageField(blank=True, null=True, upload_to=hash_file_name)
    cover = models.ImageField(blank=True, null=True, upload_to=hash_file_name)
    description = models.TextField(blank=True, null=True)

    @property
    def get_absolute_url(self):
        return reverse('user:group_detail', args=[self.slug])
