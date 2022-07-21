from django.conf import settings
from django.contrib.auth import get_user_model, user_logged_out
from django.contrib.sessions.backends.cache import KEY_PREFIX
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.core import otp

UserModel = get_user_model()


class SendVerificationCodeThrottle(AnonRateThrottle):
    rate = '1/s'  # this will be overwritten by parse_rate

    def parse_rate(self, rate):
        # one request every two minutes
        return 1, settings.VERIFICATION_CODE_THROTTLE


class SendVerificationCodeAPIView(APIView):
    throttle_classes = [SendVerificationCodeThrottle]

    def get(self, request, *args, **kwargs):
        # todo: better response status code
        if not request.session.get('auth_user_id'):
            return Response(
                {'detail': _('The session does not have required credentials.')},
                status=HTTP_400_BAD_REQUEST,
            )

        user = self.get_user()
        self._send_code(user)
        # todo: better response text
        return Response({'detail': _('The verification code sent.')})

    def get_user(self):
        return UserModel.objects.filter(
            id=self.request.session['auth_user_id'],
        ).first()

    @staticmethod
    def _send_code(user):
        code = otp.generate_code(user.id)
        # todo: send the code to user phone number
        print(code)


class RevokeSessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        session_key = request.query_params.get('session_key')
        key = KEY_PREFIX + session_key
        cache.delete(key)

        user_logged_out.send(
            self.request.user.__class__,
            request=self.request,
            session_key=session_key,
        )

        return Response(status=HTTP_204_NO_CONTENT)
