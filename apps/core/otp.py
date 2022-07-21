import base64
import hashlib

import pyotp
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


def _hash_code(code):
    return hashlib.sha256(code.encode()).hexdigest()


def generate_code(identifier):
    """
    Generate a otp code and store the hashed value in cache.

    :param identifier: a unique id for creating otp code. it's can be user id.

    :returns: the original generated code.
    """

    def gen_key():
        raw_key = f'{identifier}{timezone.now()}{settings.SECRET_KEY}'.encode()
        return base64.b32encode(raw_key).decode()

    key = gen_key()
    otp = pyotp.HOTP(key)
    code = otp.at(identifier)
    hashed_code = _hash_code(code)
    cache_key = f'{identifier}:otp'

    cache.set(cache_key, hashed_code, settings.OTP_TTL)
    return code


def verify_code(identifier, code):
    """
    Verify the given code.

    :returns: a boolean that shows the verification status
    """
    hashed_code = _hash_code(code)

    cache_key = f'{identifier}:otp'
    otp = cache.get(cache_key)
    if otp and hashed_code == otp:
        cache.delete(cache_key)
        return True
    return False
