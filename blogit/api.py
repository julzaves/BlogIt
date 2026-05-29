from flask import Blueprint, jsonify, request, current_app
from pathlib import Path
from blogit import db
from blogit.models import Comment, Post, User

api_bp = Blueprint('api', __name__)


def _comment_to_dict(comment):
    return {
        'id': comment.id,
        'content': comment.content,
        'date_posted': comment.date_posted.isoformat() if comment.date_posted else None,
        'user_id': comment.user_id,
        'post_id': comment.post_id,
        'author': comment.user.username if comment.user else None,
        'post_title': comment.post.title if comment.post else None,
    }


def _error(message, status_code):
    return jsonify({'error': message}), status_code

# CREATE
@api_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    if not request.is_json:
        return _error('Request body must be JSON', 400)

    post = db.session.get(Post, post_id)
    if not post:
        return _error('Post not found', 404)

    data = request.get_json()
    content = data.get('content')
    user_id = 3 # Hardcoded to "rest_api" user

    if not content or not user_id:
        return _error('Missing required fields: content, user_id', 400)

    user = db.session.get(User, user_id)
    if not user:
        return _error('User not found', 404)

    comment = Comment(content=content, user=user, post=post)
    db.session.add(comment)
    db.session.commit()
    return jsonify(_comment_to_dict(comment)), 201

# READ - All comments in a post
@api_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def list_comments(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return _error('Post not found', 404)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_posted.desc()).all()
    return jsonify([_comment_to_dict(comment) for comment in comments]), 200

# READ - Single Comment
@api_bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return _error('Comment not found', 404)
    return jsonify(_comment_to_dict(comment)), 200

# UPDATE
@api_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    if not request.is_json:
        return _error('Request body must be JSON', 400)

    comment = db.session.get(Comment, comment_id)
    if not comment:
        return _error('Comment not found', 404)

    data = request.get_json()
    content = data.get('content')
    if not content:
        return _error('Missing required field: content', 400)

    comment.content = content
    db.session.commit()
    return jsonify(_comment_to_dict(comment)), 200

# DELETE
@api_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return _error('Comment not found', 404)

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200


@api_bp.route('/openapi.json', methods=['GET'])
def openapi_spec():
    spec_path = Path(current_app.root_path).parent / 'openapi.json'
    if not spec_path.exists():
        return jsonify({'error': 'OpenAPI specification not found'}), 500
    return current_app.response_class(spec_path.read_bytes(), mimetype='application/json')
