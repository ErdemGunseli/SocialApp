from models import Post
from enums import Order


def order_query(query, order_by: Order = Order.DATE):
    if order_by == Order.DATE:
        return query.order_by(Post.created_at.desc())
    elif order_by == Order.POPULARITY:
        return query.order_by(Post.upvote_count.desc())
    else:
        raise ValueError("Invalid order value")
