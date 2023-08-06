from functools import wraps


def client_call(func):
    @wraps(func)
    def wrapper(self: 'I2AOauth2Client', *args, **kwargs):
        if not self.client_id:
            raise ValueError("Client call require client id.")
        return func(self, *args, **kwargs)
    return wrapper


def server_to_server_call(func):
    @wraps(func)
    def wrapper(self: 'I2AOauth2Client', *args, **kwargs):
        if not self.client_secret and not self.user_group_secret:
            raise ValueError("Servet to to server call require client secret or group secret.")
        return func(self, *args, **kwargs)
    return wrapper


def app_less_server_to_server_call(func):
    @wraps(func)
    def wrapper(self: 'I2AOauth2Client', *args, **kwargs):
        if not self.app_less_secret:
            raise ValueError("App less Servet to to server call require app less secret.")
        if not self.server_name:
            raise ValueError("App less Servet to to server call require server name.")
        return func(self, *args, **kwargs)
    return wrapper
