

from flask import url_for,redirect

def is_login(user_id):
    if user_id:
        return 1
    else:
        return redirect(url_for('login'))