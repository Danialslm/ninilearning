from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from apps.core import otp
from .models import User

UserModel = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        validators=(User.phone_number_validator,)
    )
    error_messages = {
        'invalid_login': _(
            'Any user with this %(username)s and password not found. Note that password '
            'may be case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }


class SignupForm(forms.Form):
    phone_number = forms.CharField(
        label=_('Phone number'),
        widget=forms.TextInput(),
        validators=(User.phone_number_validator,),
    )

    def clean(self):
        user, created = UserModel.objects.get_or_create(
            phone_number=self.cleaned_data['phone_number'],
            defaults={
                'is_active': False,
            }
        )
        # user with this phone number already signed up
        if user.is_active:
            self.add_error('phone_number', _('A user with this phone number already exist.'))
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data

    def save(self):
        return self.cleaned_data['user']


class SignupCompleteForm(forms.Form):
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        # need to save user info for validating password
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        password = self.cleaned_data['password']

        if first_name and last_name and password:
            self.user.first_name = first_name
            self.user.last_name = last_name

            # validate the password
            try:
                password_validation.validate_password(password, self.user)
                self.user.set_password(password)
            except ValidationError as error:
                self.add_error('password', error)
        return self.cleaned_data

    def save(self):
        self.user.is_active = True
        self.user.save()

        return self.user


class PasswordResetForm(forms.Form):
    phone_number = forms.CharField(
        label=_('Phone number'),
        widget=forms.TextInput(),
        validators=(User.phone_number_validator,),
    )

    @staticmethod
    def get_user(phone_number):
        user = UserModel.objects.filter(
            phone_number=phone_number,
            is_active=True
        ).first()

        if user is not None and user.has_usable_password():
            return user

    def clean(self):
        user = self.get_user(self.cleaned_data['phone_number'])

        if not user:
            self.add_error('phone_number', _('Any user with this phone number not found.'))
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

    def save(self):
        user = self.cleaned_data['user']
        return user


class VerificationForm(forms.Form):
    otp_validator = RegexValidator(
        regex=r'^[0-9]{6}$',
        message=_('The verification code is invalid. Note that you use English numbers.'),
    )
    verification_code = forms.CharField(
        label=_('Verification code'),
        validators=(otp_validator,)
    )

    def __init__(self, identifier, *args, **kwargs):
        self.identifier = identifier
        super().__init__(*args, **kwargs)

    def clean_verification_code(self):
        verification_code = self.cleaned_data['verification_code']
        is_valid = otp.verify_code(self.identifier, verification_code)

        if not is_valid:
            self.add_error('verification_code', _('The verification code is invalid or expired.'))

        return verification_code
