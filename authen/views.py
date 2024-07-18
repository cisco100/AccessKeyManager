from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.views import LogoutView,PasswordResetView
from django.utils import timezone
from django.contrib.auth import get_user_model,authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from authen.models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin

from authen.forms import CustomUserCreationForm ,LoginForm
import random
from django.urls import reverse_lazy,reverse

from authen.utils import generate_verification_code
User = get_user_model()


def send_verification_email(user, code):
    subject = 'Verify your email'
    message = f'Your verification code is: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False   
            user.verification_code = generate_verification_code()
            user.save()
            send_verification_email(user, user.verification_code)
            return redirect('verify_email')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     redirect_field_name="dashboard"


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                msg = "Invalid Credentials"
        else:
            msg = "Validation Error"
    return render(request, 'accounts/login.html', {"form": form, "msg": msg})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        try:
            user = User.objects.get(verification_code=code, is_active=False)
            user.is_active = True
            user.is_verified = True
            user.verification_code = None
            user.save()
            login(request, user)
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'accounts/verify_email.html', {'error': 'Invalid verification code'})
    return render(request, 'accounts/verify_email.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')