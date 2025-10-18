from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin' or not session.get('admin_id'):
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('admins_bp.admin_login'))
        return f(*args, **kwargs)
    return decorated_function
