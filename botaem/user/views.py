from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.forms import LoginForm, UserCreateForm
from user.factories import CustomUserFactory
from referral.factories import ReferralRelationshipFactory
from myprofile.factories import ProfileFactory
import logging

logger = logging.getLogger(__name__)

# View to register user
def register_user(request):
    if request.method == 'POST':
        return _handle_register_post(request)
    form = UserCreateForm()
    return render(request, 'user/register.html', {'form': form})


def _handle_register_post(request):
    form = UserCreateForm(request.POST)
    if form.is_valid():
        logger.info('Got post request for register', extra={'form_data': form.data})
        form.save(commit=False)
        user = _create_user(form)
        profile = _create_profile(user)
        _create_referral(request)
        if user and profile:
            logger.info('Created user', extra={'username': user.username})
            return redirect('user:login')
        return redirect('user:register')
    return render(request, 'user/register.html', {'form': form})


def _create_referral(request):
    if 'referred_by' in request.session:
        user = CustomUserFactory.get_by_username(request.session['referred_by'])
        referral_relationship = ReferralRelationshipFactory.create(inviter=user, invitee=request.user)
        if referral_relationship:
            logger.info('Created referral relationship', extra={'referral_relationship': referral_relationship})
        return referral_relationship


def _create_user(form):
    user = CustomUserFactory.create(
        username=form.cleaned_data['username'],
        email=form.cleaned_data['email'],
        password=form.cleaned_data['password1']
    )
    return user


def _create_profile(user):
    profile = ProfileFactory.create(user=user)
    return profile


# View to login user
def login_user(request):
    if request.method == 'POST':
        user = CustomUserFactory.get_by_username(request.POST['username'])
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('myprofile:main_page')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('user:login')
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


# View to logout user
def logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return redirect('user:login')