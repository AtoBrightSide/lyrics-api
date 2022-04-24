from flask import Blueprint, request, Response, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Lyric, Review

reviews = Blueprint('reviews', __name__)

@reviews.route('/reviews', methods=['GET', 'POST'])
@reviews.route('/reviews/user/<string:user_id>')
@reviews.route('/reviews/lyric/<string:lyric_id>')
@reviews.route('/reviews/<string:review_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def review(review_id=None, user_id=None, lyric_id=None):
    if request.method == 'GET':
        if user_id: # get reviews made by specific user
            reviews = Review.query.filter_by(reviewer=user_id)
            if not reviews.count():
                return Response('User has not made reviews!', status=404)
            return jsonify([review.to_dict() for review in reviews])
        elif lyric_id: # get reviews for a specific lyric
            reviews = Review.query.filter_by(lyric=lyric_id)
            if not reviews.count():
                return Response('Lyric has no reviews!', status=404)
            return jsonify([review.to_dict() for review in reviews])
        elif review_id: # get specific review
            if not user_id:
                review = Review.query.get(review_id)
                if not review:
                    return Response('Review Not Found!', status=404)
                return jsonify(review.to_dict())
        
        reviews = Review.query.all()
        return jsonify([r.to_dict() for r in reviews])
    
    elif request.method == 'POST':
        lyric_id = request.form.get('lyric_id')
        review = request.form.get('review')

        if not lyric_id or not review:
            return Response('Required Fields have not been met!', status=404)

        # users can not review the lyrics they uploaded themselves
        lyric = Lyric.query.get(lyric_id)
        if lyric.user == current_user.id:
            return Response('Self Review is not allowed!', status=404)
        
        new_review = Review(reviewer=current_user.id, lyric=lyric_id, review=review)

        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict())
    
    elif request.method == 'DELETE':
        if review_id:
            review = Review.query.get(review_id)
            if not review or review.reviewer != current_user.id:
                error_msg = 'No review found' if not review else 'Unauthorized Action' 
                return Response(error_msg, status=404)
            
            db.session.delete(review)
            db.session.commit()

            return Response('Successfully Deleted', status=200)
