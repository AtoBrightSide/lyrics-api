from flask import Blueprint, request, Response, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Follow

follow = Blueprint('follow', __name__)


@follow.route('/follow', methods=['POST'])
@follow.route('/follow/info/<string:user_id>')
@login_required
def follows(user_id=None):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if not user:
            return Response("User not found!", status=404)

        return jsonify({
            "following": user.number_of_following,
            "followers": user.number_of_followers,
        })
    else:
        follower = request.form.get('follower')
        following = request.form.get('following')

        if not follower or not following:
            return Response("Required fields have not been entered!", status=404)
        if follower == following:
            return Response('Users can not follow themselves!', status=404)

        follower = User.query.get(follower)
        following = User.query.get(following)
        if not follower or not following:
            return Response("User/s does found!", status=404)

        action = Follow(follower=follower.id, following=following.id)

        db.session.add(action)
        db.session.commit()

        return jsonify(action.to_dict())
