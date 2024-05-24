from flask import Blueprint, render_template, g, flash, redirect, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
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


@bp.route('/add_to_cart/<int:post_id>', methods=['POST'])
@login_required
def add_to_cart(post_id):
    db = get_db()
    user_id = g.user['id']

    # Check if the item is already in the cart
    cart_item = db.execute(
        'SELECT * FROM cart WHERE user_id = ? AND post_id = ?', (user_id, post_id,)
    ).fetchone()

    if cart_item:
        # Update quantity if the item is already in the cart
        db.execute(
            'UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND post_id = ?',
            (user_id, post_id,)
        )
    else:
        # Insert new item into the cart
        db.execute(
            'INSERT INTO cart (user_id, post_id, quantity) VALUES (?, ?, ?)',
            (user_id, post_id, 1,)
        )

    db.commit()
    flash('Item added to cart.')
    return redirect(url_for('shop.index'))


@bp.route('/cart')
@login_required
def view_cart():
    db = get_db()
    user_id = g.user['id']

    cart_items = db.execute(
        'SELECT c.id, c.quantity, p.id as post_id, p.title, p.description, p.price, p.image_path'
        ' FROM cart c JOIN post p ON c.post_id = p.id'
        ' WHERE c.user_id = ?', (user_id,)
    ).fetchall()

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('shop/cart.html', cart_items=cart_items, total_price=total_price)


@bp.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    db = get_db()
    user_id = g.user['id']

    db.execute(
        'DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_id, user_id)
    )

    db.commit()
    flash('Item removed from cart.')
    return redirect(url_for('shop.view_cart'))


@bp.route('/post/<int:post_id>')
@login_required
def post_detail(post_id):
    db = get_db()
    post = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_path, p.created, u.username as author'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (post_id,)
        ).fetchone()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist")

    return render_template('shop/post_detail.html', post=post)