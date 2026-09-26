from flask import render_template, jsonify , Blueprint, redirect, request, url_for, flash, session
from flask_login import current_user , login_required, logout_user, login_user
from ..db.models import User
from ..extension import db, login_manager, bcrypt

auth_bp = Blueprint('auth',__name__,template_folder='templates')


@auth_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        role = data["role"]

        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({"message":"Account with email already exists"}),200
        
        password = bcrypt.generate_password_hash(data['password'])
        new_user = User(name=name,email=email,password=password,role=role)
        db.session.add(new_user)
        db.session.commit()
        

@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message":"User Not Found Please Register"}),200
        
        elif not bcrypt.check_password_hash(user.password,password):
            return jsonify({"message":"Wrong Password"}),200
        
        
        else:
            login_user(user, remember=True)
            return redirect(url_for('dash.dashboard'))
    

@auth_bp.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))