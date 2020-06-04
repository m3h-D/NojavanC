from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from nojavan.utils import get_client_ip


# Create your models here.
User = get_user_model()


class UserTrackerManager(models.Manager):
    """custom ORM
    
    Arguments:
        models {class Module} -- it's a model manager that inharitanced from django Manager
    
    Returns:
        QS -- returns/create a queryset of UserTracker record
    """

    def filter_by_model(self, instance, the_status=None):
        """a custome ORM that filter the UserTracker by Model or content_type
        
        Arguments:
            instance {OBJECT} -- instance is an object of a model that been selected as content_type in GenericForeignKey
        
        Returns:
            QS -- returns a queryset of usertracker records
        """
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super().filter(
            content_type=content_type, object_id=object_id)

    def create_by_model(self, url, ip_address, user_agent, user=None, instance=None):
        """create a record in UserTracker table
        
        Arguments:
            instance {OBJECT} -- assign a model instance to detailing the info
            url {URL} -- a path that user has been visited
            user_ip {REMOTE_IP} -- the ip of requeted user
            user_agent {MODULE} -- a module tha specife the user agent(browser, device)
        
        Keyword Arguments:
            user {OBJECT} -- assign the requested user if is authenticated (default: {None})
        
        Returns:
            QS -- return queryset of created record
        """
        content_type = None
        object_id = 0
        if instance is not None:
            content_type = ContentType.objects.get_for_model(
                instance.__class__)
            object_id = instance.id
        return super().create(user=user, content_type=content_type, object_id=object_id, url=url, ip_address=ip_address, user_agent=user_agent)


    def recommended_list(self, request, instance):
        """ye recommended list bar assasse category va session"""
        if request.user.is_authenticated:
            viewed_item = self.filter_by_model(
                instance=instance).filter(user=request.user)
        elif request.user.is_anonymous:
            ip_address = get_client_ip(request)
            viewed_item = self.filter_by_model(
                instance=instance).filter(user__isnull=True, ip_address=ip_address)
        same_category = list()
        for item in viewed_item:
            # category e post haei ke user dide
            same_category = item.content_object.category.values_list(
                'id', flat=True)

        queryset = instance.__class__.objects.filter(
            category__id__in=same_category)
        try:
            """ye session e listi misaze ke Model o bar assasse category e bala filter mikone"""
            request.session['same_categories'] += list(queryset.values_list(
                'pk', flat=True))  # bareye in az values_list o pk estefade kardim ke dg niaz be serialize kardan nabshe

        except:
            request.session['same_categories'] = list(
                queryset.values_list('pk', flat=True))

        same_item = instance.__class__.objects.filter(
            pk__in=request.session.get('same_categories'))

        return same_item


class UserTracker(models.Model):
    """a model to track requested user by visited path, ip, id
    
    Arguments:
        models {class Module} -- a Model module that inharitanced from django Model to create Table
    
    Returns:
        STRING -- returns requested user specifications
    """
    user = models.ForeignKey(
        User, related_name='usertracker', blank=True, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    url = models.URLField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    # status = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = UserTrackerManager()

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        try:
            return f"{self.user.first_name} {self.user.last_name}/{self.user.phone}"
        except:
            return self.content_object.title
        finally:
            return f"{self.ip_address}"


