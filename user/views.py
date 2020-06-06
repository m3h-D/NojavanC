from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Q
from urllib.parse import urlsplit
from dateutil import parser
from .forms import *
from .tokens import account_activation_token
from .tasks import send_email
from nojavan.utils import self_or_admin, search_engine, export_excel
# from nojavan.engine.smspanel import send_sms
from threading import Thread
from .models import Group
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required
import logging

logger = logging.getLogger(__name__)


User = get_user_model()

# Create your views here.

# -----------------------[authentications]--------------------------

def login_view(request):
    next = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(reverse('user:profile_view', kwargs={"user_username": request.user.username}))
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        else:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, str(form.errors), extra_tags='login_failed')
        logger.error(str(form.errors.as_data()))
    return render(request, 'user/login.html', {"form": form})


def profile_view(request, user_username):
    user = get_object_or_404(User, username=user_username)
    return render(request, 'user/profile.html', {"user": user})


def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    time = request.session.get('register_timer')
    timer = None
    if time:
        timer = parser.parse(time)
    register_form = RegisterForm(request.POST or None, timer=timer)
    if request.method == "POST":
        if register_form.is_valid():
            register_form.save()
            sms_validate = str(randint(int('1' * 6), int('9' * 6)))
            timer = timezone.now() + timezone.timedelta(minutes=2)
            request.session['sms_validate'] = sms_validate
            request.session['phone'] = register_form.instance.phone
            request.session['register_timer'] = str(timer)
            # send_sms(sms_validate, register_form.instance.phone, 'register')
            print(sms_validate)
            # messages.success(request, 'ثبت نام شما با موفقیت انجام شد', extra_tags='register_success')
            return redirect('user:verification_view')
        else:
            messages.error(request, str(register_form.errors), extra_tags='register_failed')
            logger.error(str(register_form.errors.as_data()))
    return render(request, 'user/register.html', {"register_form": register_form})



def send_sms_again(request):
    """get the phone number that stored in session in stage of 1 and calculate random number and send that as sms
    
    Arguments:
        session {SESSION} -- to store and check phone and validation code
    
    Returns:
        BOOLEAN -- returns True if everythig goes well
    """
    if request.is_ajax():
        sms_validate = str(randint(int('1' * 6), int('9' * 6)))
        request.session['sms_validate'] = sms_validate
        # send_sms(sms_validate, phone, 'register')
        print(sms_validate)
        timer = timezone.now() + timezone.timedelta(minutes=2)
        request.session['register_timer'] = str(timer)
        logger.success(str(sms_validate))
        return JsonResponse({"response": "کد جدید برای شما ارسال شد"})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def verification_view(request):
    if not 'sms_validate' in request.session:
        return redirect("user:register_view")
        
    expire_time = parser.parse(request.session['register_timer'])
    verify_form = VerificationForm(request.POST or None, session=request.session, expire_time=expire_time)
    if request.method == "POST":
        if verify_form.is_valid():
            user = get_object_or_404(User, phone=request.session.get('phone', '090000000000'))
            user.is_active = True
            user.save()
            try:
                del request.session['register_timer']
            except KeyError:
                pass
            try:
                del request.session['sms_validate']
            except KeyError:
                pass
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد', extra_tags='register_success')
            return redirect('user:login')
        else:
            messages.error(request, str(verify_form.errors), extra_tags='verification_failed')
            logger.error(str(verify_form.errors.as_data()))
    return render(request, 'user/verify.html', {"verify_form": verify_form})



def forget_password(request):
    form = ForgetPasswordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if email:
                user = User.objects.get(email__iexact=email)
                template = 'email/fp-email.html'
                sub = 'فراموشی رمز عبور'
                Uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                domain = f"{urlsplit(request.build_absolute_uri(None)).scheme}://{get_current_site(request)}"
                send_email.delay(domain=domain, to=[user.email], template=template, sub=sub, messages=[Uid, token])
                # Thread(target=send_email, args=(request,), kwargs={"domain": domain,
                #     "to": [user.email] , 'template': template, 'sub': sub, 'messages': [Uid, token]}).start()
                messages.success(request, 'لینک فراموشی برای ایمیل شما ارسال شد', extra_tags='forget_password_success')
                return redirect('user:login')
        else:
            messages.error(request, str(form.errors), extra_tags='forget_password_errors')
            logger.error(str(form.errors.as_data()))

    return render(request, 'user/forget-password.html', {'form': form})


def new_password(request, uidb64, token):
    """set the password for the requested user
    
    Returns:
        BOOLEAN -- redirect user to login page if success is True
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = NewPasswordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, 'رمزعبور شما با موفقیت تغییر کرد', extra_tags='new_password_success')
                return redirect('user:login')
            else:
                messages.error(request, str(form.errors), extra_tags='new_password_errors')
                logger.error(str(form.errors.as_data()))

    else:
        logger.error('لینک نا معتبر است.')
        return HttpResponse('لینک نا معتبر است.')
        
    return render(request, 'user/new-password.html', {'form': form})


# --------------------[ Group ]------------------------------


def add_to_group(request):
    if request.is_ajax():
        user_id = request.POST.get('user_id')
        group_slug = request.POST.get('group_slug')
        user = get_object_or_404(User, id=int(user_id))
        the_group = get_object_or_404(Group, owner=request.user, slug=group_slug)
        if user in the_group.members.all():
            the_group.members.remove(user)
            response = f"کاربر {user.username} از گروه {the_group.title} حذف شد"
        else:
            the_group.members.add(user)
            response = f"کاربر {user.username} با موفقیت به گروه {the_group.title} اضافه شد"
        return JsonResponse({"response": response})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def create_group(request):
    group_form = GroupForm(request.POST or None, request.FILES or None, request=request)
    if request.method == "POST":
        if group_form.is_valid():
            group_form.save()
            messages.success(request, 'گروه شما با موفقیت ایجاد شد', extra_tags='success_create_group')
            return redirect(reverse('user:group_detail', kwargs={'group_slug': group_form.instance.slug}))
        else:
            messages.error(request, str(group_form.errors), extra_tags='failed_create_group')
            logger.error(str(group_form.errors.as_data()))

    return render(request, 'user/create-group.html', {'group_form': group_form})
    

def group_detail(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    return render(request, 'user/group-detail.html', {'group': group})


      
# -----------------------------[Managing]------------------------------


def create_user(request):
    user_form = CreateUserForm(request.POST or None)
    if user_form.is_valid():
        user_form.save()
        messages.success(request, f'ثبت نام {user_form.instance.username} با موفقیت انجام شد', extra_tags='register_success')
        return redirect(reverse('user:profile_view', kwargs={'user_username': user_form.instance.username}))
    else:
        messages.error(request, str(user_form.errors), extra_tags='failed_create_user')
        logger.error(str(user_form.errors.as_data()))
    return render(request, 'user/create-user.html', {"user_form": user_form})


def list_user(request):
    users = User.objects.all()
    searches = request.GET
    if searches and searches != "":
        users = search_engine(searches, users)
    return render(request, 'user/list-user.html', {'users': users})


def user_action(request):
    if request.is_ajax():
        action = request.POST.get('action')
        user_ids = request.POST.getlist('ids')
        response = None
        if action == 'delete':
            for user_id in user_ids:
                user = get_object_or_404(User, id=int(user_id))
                user.delete()
            response = 'عملیات حذف با موفقیت انجام شد'
        elif action == 'export':
            redirect = reverse('export_excel', kwargs={'model': 'user', 'action': str(user_ids)})
            response = 'عملیات اکسل با موفقیت انجام شد'
        elif action == 'message':
            redirect = reverse('message:send_message', kwargs={'receivers': str(user_ids), 
                               'content': str(request.POST.get("content")), 
                               'room_ids': str(request.POST.getlist('chatroom_id'))})
            response = 'پیام ها با موفقیت ارسال شدند'
        return JsonResponse({'response': {"message": response, 'redirect': redirect}})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        


def delete_user(request):
    if request.is_ajax():
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        response = f"کاربر {user.username} با موفقیت حذف شد"
        user.delete()
        logger.info(f'deleted user : {user.username}')

        return JsonResponse({"response": response})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def edit_user(request, user_username):
    # user = get_object_or_404(User, username=user_username)
    user = self_or_admin(request, User, username=user_username)
    edit_profile_form = EditProfileForm(request.POST or None, request.FILES or None, instance=user.profile)
    edit_user_form = EditUserForm(request.POST or None, instance=user)
    if request.method == "POST":
        if edit_user_form.is_valid() and edit_profile_form.is_valid():
            edit_user_form.save()
            edit_profile_form.save()
            update_session_auth_hash(request, edit_user_form.instance)
            messages.success(request, f'پروفایل {user.first_name} {user.last_name} با موفقیت تغییر کرد', extra_tags='edit_user_success')
            return redirect(reverse("user:profile_view", kwargs={'user_username': edit_user_form.instance.username}))
        else:
            logger.error(f"{edit_user_form.errors.as_data()} \n {edit_profile_form.errors.as_data()}")
            messages.error(request, f"{edit_user_form.errors} \n {edit_profile_form.errors}", extra_tags='edit_account_failed')

    return render(request, 'user/edit-user.html', {'edit_user_form': edit_user_form, 'edit_profile_form': edit_profile_form})



def follow_user(request):
    if request.is_ajax():
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=int(user_id))
        if user in request.user.profile.following.all():
            request.user.profile.following.remove(user)
            response = f"شما کاربر {user.username} را دیگر دنبال نمی کنید"
        else:
            request.user.profile.following.add(user)
            response = f"شما کاربر {user.username} را دنبال کردید"
        return JsonResponse({"response": response})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@staff_member_required
def accept_owner(request):
    if request.is_ajax():
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=int(user_id))
        if user.is_accepted:
            user.is_accepted = False
            response = f"کاربر {user.username} مورد تایید قرار گرفت"
            logger.info(f'accepted user: {user.username}')

        else:
            user.is_accepted = True
            response = f"کاربر {user.username} رد شد"
            logger.info(f'declined user: {user.username}')

        user.save()
        return JsonResponse({"response": response})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))