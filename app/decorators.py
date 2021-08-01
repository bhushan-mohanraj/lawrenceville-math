from functools import wraps

from flask import g, abort


def user_required(view):
    @wraps(view)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return abort(401)

        return view(*args, **kwargs)

    return decorated_view


def staff_required(view):
    @wraps(view)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return abort(401)

        if not g.user.staff:
            return abort(403)

        return view(*args, **kwargs)

    return decorated_view
