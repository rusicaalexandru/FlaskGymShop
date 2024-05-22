from flask import Blueprint, render_template, flash
from flaskr.db import get_db
bp = Blueprint('shop', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_path, p.created, u.username as author'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY p.created DESC'
    ).fetchall()
    return render_template('shop/index.html', posts=posts)


@bp.route('/post/<int:post_id>')
def post_detail(post_id):
    db = get_db()
    post = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_path, p.created, u.username as author'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (post_id,)
        ).fetchone()

    if post is None:
        flash(f"404. Post id {post_id} doesn't exist")

    return render_template('shop/post_detail.html', post=post)