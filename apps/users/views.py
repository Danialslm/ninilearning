import throttle
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordChangeView as BasePasswordChangeView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.core import otp
from . import forms
from .models import Device

UserModel = get_user_model()


class VerificationCodeMixin:
    """ Send verification code if the form was valid. """

    def form_valid(self, form):
        user = self.get_user()
        self._send_code(user)
        return super().form_valid(form)

    def get_user(self):
        return UserModel.objects.filter(
            id=self.request.session['auth_user_id'],
        ).first()

    @staticmethod
    @throttle.wrap(settings.VERIFICATION_CODE_THROTTLE, 1)
    def _send_code(user):
        code = otp.generate_code(user.id)
        # todo: send the code to user phone number
        print(code)


class LimitLoginDevicesMixin:
    """ Limit number of devices can login to an account. """

    def form_valid(self, form):
        devices_count = Device.objects.filter(user=form.get_user()).count()
        if devices_count >= settings.MAX_LOGGED_IN_DEVICES:
            messages.error(self.request, _('The number of devices logged into this account has been maximized.'))
            # todo: better response status code
            return self.render_to_response(self.get_context_data(), status=401)
        return super().form_valid(form)


class LoginView(LimitLoginDevicesMixin, BaseLoginView):
    form_class = forms.LoginForm
    redirect_authenticated_user = True


class SignupView(VerificationCodeMixin, FormView):
    form_class = forms.SignupForm
    template_name = 'registration/signup/signup.html'
    success_url = reverse_lazy('users:signup_verification')

    def form_valid(self, form):
        user = form.save()
        self.request.session['auth_user_id'] = user.id
        return super().form_valid(form)


class SignupVerificationView(FormView):
    form_class = forms.VerificationForm
    template_name = 'registration/signup/signup_verification.html'
    success_url = reverse_lazy('users:signup_complete')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('auth_user_id'):
            return redirect('users:signup')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['identifier'] = self.request.session['auth_user_id']
        return kwargs


class SignupConfirmView(FormView):
    form_class = forms.SignupCompleteForm
    template_name = 'registration/signup/signup_complete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('auth_user_id'):
            return redirect('users:signup')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session['auth_user_id']
        user = UserModel.objects.filter(id=user_id).first()

        kwargs['user'] = user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class PasswordChangeView(BasePasswordChangeView):
    success_url = reverse_lazy('dashboard:profile')
    template_name = 'dashboard/password_change_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(self.request, _('Your password was changed successfully.'))
        return response


class PasswordResetView(VerificationCodeMixin, FormView):
    form_class = forms.PasswordResetForm
    template_name = 'registration/password_reset/password_reset.html'
    success_url = reverse_lazy('users:password_reset_verification')

    def form_valid(self, form):
        user = form.save()
        self.request.session['auth_user_id'] = user.id
        return super().form_valid(form)


class PasswordResetVerificationView(FormView):
    form_class = forms.VerificationForm
    template_name = 'registration/password_reset/password_reset_verification.html'
    success_url = reverse_lazy('users:password_reset_confirm')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('auth_user_id'):
            return redirect('users:password_reset')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['identifier'] = self.request.session['auth_user_id']
        return kwargs


class PasswordResetConfirmView(FormView):
    form_class = SetPasswordForm
    template_name = 'registration/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('auth_user_id'):
            return redirect('users:password_reset')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Your new password has been set. You can login now.'))
        del self.request.session['auth_user_id']

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = UserModel.objects.filter(
            id=self.request.session['auth_user_id'],
        ).first()
        kwargs['user'] = user
        return kwargs
