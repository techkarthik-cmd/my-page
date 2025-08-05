# my/myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project, ContactMessage
from .forms import ContactForm
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Profile, OTPCode
from .forms import LoginForm, SignupForm, OTPRequestForm, OTPVerifyForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')  # this will redirect to /


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Profile

@login_required(login_url='/auth/login/')
def profile_view(request):
    # Show ONLY if the profile exists — do NOT create new one
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})



def is_admin(user):
    return user.is_staff or user.is_superuser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login_key = form.cleaned_data['login']
        password = form.cleaned_data['password']  # may be empty if user prefers OTP
        if password:
            user = authenticate(request, username=login_key, password=password)
            if user:
                login(request, user)
                return redirect('profile')
            messages.error(request, "Invalid credentials.")
        else:
            messages.info(request, "Use OTP Login if you don't have a password.")
    return render(request, 'auth_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if User.objects.filter(email__iexact=form.cleaned_data['email']).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            Profile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                headline="AWS Data Engineer",
                summary="",
                skills="",
                experience=""
            )
            messages.success(request, "Signup successful. Please login.")
            return redirect('login')
    return render(request, 'auth_signup.html', {'form': form})

def otp_request_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = OTPRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        phone = form.cleaned_data['phone']
        # find user by phone
        try:
            profile = Profile.objects.get(phone__iexact=phone)
        except Profile.DoesNotExist:
            messages.error(request, "Phone not found. Please sign up first.")
            return redirect('signup')
        # generate OTP
        code = f"{random.randint(100000, 999999)}"
        otp = OTPCode.objects.create(phone=phone, code=code)
        # DEV: print/send to console email (simulate SMS)
        send_mail(
            subject="Your OTP Code",
            message=f"OTP for login: {code}. It expires in 5 minutes.",
            from_email=None,
            recipient_list=[profile.user.email],
        )
        messages.success(request, "OTP sent (check console email).")
        return render(request, 'auth_otp_verify.html', {'form': OTPVerifyForm(initial={'token': otp.token})})
    return render(request, 'auth_otp_request.html', {'form': form})

def otp_verify_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = OTPVerifyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        token = form.cleaned_data['token']
        code = form.cleaned_data['code']
        try:
            otp = OTPCode.objects.get(token=token, is_used=False)
        except OTPCode.DoesNotExist:
            messages.error(request, "Invalid or used OTP link.")
            return redirect('otp_request')
        # expire after 5 minutes
        if (timezone.now() - otp.created_at).total_seconds() > 300:
            messages.error(request, "OTP expired. Please request again.")
            return redirect('otp_request')
        if otp.code != code:
            messages.error(request, "Incorrect OTP code.")
            return render(request, 'auth_otp_verify.html', {'form': form})
        # login user by phone
        try:
            profile = Profile.objects.get(phone__iexact=otp.phone)
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found.")
            return redirect('login')
        otp.is_used = True
        otp.save()
        login(request, profile.user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('profile')
    return render(request, 'auth_otp_verify.html', {'form': form})

# Optional: password reset using Django built-ins (email console)
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
class ResetRequestView(PasswordResetView):
    template_name = 'auth_reset.html'
    email_template_name = 'auth_reset_email.txt'
    subject_template_name = 'auth_reset_subject.txt'
    success_url = '/auth/reset/done/'

class ResetDoneView(PasswordResetDoneView):
    template_name = 'auth_reset_done.html'

class ResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth_reset_confirm.html'
    success_url = '/auth/reset/complete/'

class ResetCompleteView(PasswordResetCompleteView):
    template_name = 'auth_reset_complete.html'


def home(request):
    recent = Project.objects.all()[:6]
    return render(request, 'home.html', {'recent': recent})

def mind(request):
    return render(request, 'mind.html')

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to DB
            ContactMessage.objects.create(**form.cleaned_data)
            # Send email to console
            send_mail(
                subject=f"Portfolio contact from {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=None,
                recipient_list=['you@example.com'],
            )
            messages.success(request, "Thanks! I'll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
