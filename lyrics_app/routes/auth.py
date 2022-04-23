from flask import Blueprint, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from ..models import User
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return "Incorrect Username and/or password"
    
    login_user(user, remember=remember)
    return "Login Successful!"

@auth.route('/signup', methods=['GET','POST'])
def signup_post():
    if request.method == 'POST':
        # validate here
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password = generate_password_hash((request.form.get('password')), method='sha256')

        user = User.query.filter_by(email=email).first()
        if user:
            return f'{email} already in use!'

        new_user = User(email=email, user_name=user_name, password=password)
        
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict())
    else:
        return Response('Sign Up Page', status=200)

@auth.route('/logout')
def logout():
    return 'Logout'