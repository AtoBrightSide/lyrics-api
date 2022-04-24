from flask import Blueprint, request, Response, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Lyric

lyrics = Blueprint('lyrics', __name__)

@lyrics.route('/lyrics', methods=['GET', 'POST'])
@lyrics.route('/lyrics/user/<string:user_id>')
@lyrics.route('/lyrics/<string:lyric_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def lyric(lyric_id=None, user_id=None):
    if request.method == 'GET':
        # lyrics uploaded by single user
        if user_id:
            lyrics = Lyric.query.filter_by(user=user_id)
            if not lyrics.count():
                return Response('Lyrics not found!', status=404)
            
            return jsonify([lyric.to_dict() for lyric in lyrics])
        # get specific lyric
        elif lyric_id:
            lyric = Lyric.query.get(lyric_id)
            if not lyric:
                return Response('Lyric does not exist', status=404)
            return jsonify(lyric.to_dict())
            
        lyrics = Lyric.query.all()
        return jsonify([lyric.to_dict() for lyric in lyrics])
    
    # to upload(create) a lyric
    elif request.method == 'POST':
        content = request.form.get('content')
        title = request.form.get('title')
        if not content or not title:
            return Response('Required fields have not been entered!', status=404)
        
        new_lyric = Lyric(user=current_user.id, title=title, content=content)

        db.session.add(new_lyric)
        db.session.commit()

        return jsonify(new_lyric.to_dict())
    
    # to delete a single lyric
    elif request.method == 'DELETE':
        lyric = Lyric.query.get(lyric_id)
        
        if not lyric or lyric.user != current_user.id:
            errormsg = 'Lyric Does Not Exist' if not lyric else 'Unauthorized Action!'
            return Response(errormsg, status=404)
        
        db.session.delete(lyric)
        db.session.commit()
        return Response('Successfully Deleted', status=200)