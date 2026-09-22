

from flask import redirect, url_for, session
from functools import wraps


def login_required(func):
    """
    A login is required. If you are not logged in, you will be redirected to the login page.
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper