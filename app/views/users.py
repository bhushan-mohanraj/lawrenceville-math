from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
)

from .. import models, forms

from sqlalchemy import select


bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
)


@bp.before_app_request
def load_user():
    if "user_id" in session:
        g.user = models.db_session.get(
            models.User,
            session["user_id"],
        ).first()[0]
    else:
        g.user = None


@bp.route("/login/", methods=("GET",))
def login():
    form = forms.LoginForm()

    return render_template(
        "users/login.html",
        form=form,
    )


@bp.route("/login/", methods=("POST",))
def login_post():
    form = forms.LoginForm(request.form)

    if form.validate():
        email, password = form.email.data, form.password.data

        user = models.db_session.execute(
            select(models.User).where(models.User.email == email)
        ).first()[0]

        if user and user.check_password(password):
            session["user_id"] = user.id

            return redirect(url_for("main.index"))

    return render_template(
        "users/login.html",
        form=form,
    )


@bp.route("/logout/")
def logout():
    session.pop("user_id", None)

    return redirect(url_for("main.index"))
