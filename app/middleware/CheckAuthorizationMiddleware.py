from functools import wraps


def middleware():
    def _middleware(f):
        @wraps(f)
        def __middleware(*args, **kwargs):
            # just do here everything what you need
            print('before home')
            result = f(*args, **kwargs)
            print('home result: %s' % result)
            print('after home')
            return result

        return __middleware

    return _middleware()
