from flask import render_template, Blueprint, redirect, request, url_for, flash, session
from flask_login import current_user , login_required, logout_user, login_user
from ..db.models import Users, Staff, Trekker, Messages
from ..extension import db, login_manager, bcrypt

auth_bp = Blueprint('auth',__name__,template_folder='templates')

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))
    return render_template('index.html', title='Hykr')

@auth_bp.route('/policy')
def policy():
    return render_template('policy.html', title='Refund Policy')

@auth_bp.route('/contact',methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':

        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        message = request.form.get("message").strip()

        obj = Messages(name=name, email=email, message = message)

        db.session.add(obj)
        db.session.commit()

        flash("Message sent successfully",category='success')
    return render_template('contact.html', title='Hykr')

@auth_bp.route('/about')
def about_us():
    return render_template('about.html', title='Hykr')

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


@auth_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name'].strip()
        email = data['email'].strip()
        role = data['role']
        dob = data['dob'],
        phone_number = int(data['phone_number']),
        gender = data['gender']
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('An account with this email already exists',category='danger')
            return redirect(url_for('auth.index'))
        password = bcrypt.generate_password_hash(data['password'])
        new_user = Users(name=name,email=email,password=password,dob=dob[0],role=role,phone_number=phone_number[0])
        db.session.add(new_user)
        db.session.commit()
        present_user_id = Users.query.filter_by(email=email).first()
        if role=='trekker':
            new_trekker = Trekker(gender=gender, trekker_id=present_user_id.get_id(), status='Active')
            db.session.add(new_trekker)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('dash.dashboard'))
        else:
            new_staff = Staff(gender=gender, staff_id=present_user_id.get_id(), status='Pending')
            db.session.add(new_staff)
            db.session.commit()
            flash('Your account is pending please wait for Admin Aprroval',category='warning')
            return redirect(url_for('dash.dashboard'))
        
    else:
        return redirect(url_for('auth.index'))

@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()

        if not user:
            flash('User Not Found Please Register',category='danger')
            return redirect(url_for('auth.index'))
        
        elif not bcrypt.check_password_hash(user.password,password):
            flash('Wrong Password',category='danger')
            return redirect(url_for('auth.index'))
        
        else:
            login_user(user, remember=True)
            return redirect(url_for('dash.dashboard'))
    else:
        return redirect(url_for('auth.index'))
    

@auth_bp.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully',category='success')
    return redirect(url_for('auth.index'))