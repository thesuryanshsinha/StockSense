from functools import wraps
from flask_login import current_user, login_required, logout_user
from flask import abort, flash, redirect, url_for

def role_needed(role1, role2=None):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if role2==None:
                if current_user.role != role1:
                    abort(403)
            else:
                if current_user.role != role1 and current_user.role != role2:
                    abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# def approval_needed(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if current_user.role != 'admin':
#             if (current_user.staff_profile is not None):
#                 if current_user.staff_profile.status != 'Approved' :
#                     if current_user.staff_profile.status == 'Pending':
#                         flash(f'You are not Approved your current status is Pending',category='warning')
#                     elif current_user.staff_profile.status in ['Blacklisted', 'Dead', 'Injured']:
#                         flash(f'You are {current_user.staff_profile.status}',category='danger')
#                     logout_user()
#                     return redirect(url_for('auth.login'))
#             else:
#                 if current_user.trekker_profile.status != 'Active' :
#                     if current_user.trekker_profile.status in ['Inactive', 'Dead'] :
#                         flash(f'You are {current_user.trekker_profile.status}',category='danger')
#                     logout_user()
#                     return redirect(url_for('auth.login'))
#         return func(*args, **kwargs)
#     return wrapper