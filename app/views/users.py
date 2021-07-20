from flask import (
    Blueprint,
    render_template,
)

from .. import models, forms


bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
)


@bp.route("/login/", methods=("GET",))
def login():
    form = forms.LoginForm()

    return render_template(
        "users/login.html",
        form=form,
    )


@bp.route("/login/", methods=("POST",))
def login_post():
    ...


@bp.route("/logout/")
def logout():
    ...
