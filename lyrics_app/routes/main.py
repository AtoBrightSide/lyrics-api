from flask import Blueprint, jsonify, Response
from ..models import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Index"

@main.route('/profile/<string:user_id>')
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(user.to_dict())

    return Response('User does not exist!', status=404)