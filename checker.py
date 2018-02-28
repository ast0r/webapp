from flask import session, render_template
from functools import wraps


def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> 'html':
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return render_template('error_login.html',
                               the_title='Please login')

    return wrapper

