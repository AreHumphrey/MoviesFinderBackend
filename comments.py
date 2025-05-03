from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Comment, User

comments_bp = Blueprint("comments", __name__)

@comments_bp.route("/comments/<movie_id>", methods=["GET"])
def get_comments(movie_id):
    comments = Comment.query.filter_by(movie_id=movie_id).order_by(Comment.date.desc()).all()
    result = [
        {
            "id": c.id,
            "text": c.text,
            "date": c.date.isoformat(),
            "user": User.query.get(c.user_id).email
        }
        for c in comments
    ]
    return jsonify(result)

@comments_bp.route("/comments/<movie_id>", methods=["POST"])
@jwt_required()
def add_comment(movie_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    comment = Comment(
        movie_id=movie_id,
        text=data.get("text"),
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({"msg": "Комментарий добавлен"})
