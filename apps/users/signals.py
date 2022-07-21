from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.users.models import Device
from apps.core import get_client_ip


@receiver(user_logged_in)
def save_device(request, user, *args, **kwargs):
    """ Save logged-in device info. """
    ip_address = get_client_ip(request)
    device_name = request.user_agent

    Device.objects.update_or_create(
        user=user,
        ip_address=ip_address,
        device_name=device_name,
        defaults={
            'session_key': request.session.session_key,
        }
    )


@receiver(user_logged_out)
def remove_device(request, *args, **kwargs):
    """ Remove logged-out device info. """
    session_key = kwargs.get('session_key')

    Device.objects.filter(
        session_key=session_key or request.session.session_key,
    ).delete()
