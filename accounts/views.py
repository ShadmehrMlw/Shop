import random
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from utils import send_otp_code, UserLoginAccessToRegisterMixin
from .forms import UserRegistrationForm, UserRegistrationVerifyCodeForm, UserLoginForm, ProductDetailForm
from .models import OtpCode, User
from django.contrib import messages

# Create your views here.
class UserRegisterView(UserLoginAccessToRegisterMixin, View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(10000, 99999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we sent a code for you phone number', 'success')
            return redirect('accounts:verify_code')
        return redirect(request, 'accounts/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'your loggin is successfuly!', 'success')
                return redirect('home:home')
            messages.error(request, 'your username or password is wrong...', 'warning')
            return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you are seccessfull log out', 'success')
        return redirect('home:home')


class UserRegistrationVerifyCodeView(View):
    form_class = UserRegistrationVerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instanse = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instanse.code:
                User.objects.create_user(
                    user_session['phone_number'],
                    user_session['email'],
                    user_session['full_name'],
                    user_session['password']
                )
                code_instanse.delete()
                messages.success(request, 'you are register', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
