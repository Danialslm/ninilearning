def get_client_ip(request):
    """
    Get the client ip address from request object.

    :param request: The request object.

    :return: the client ip address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    return ip_address
