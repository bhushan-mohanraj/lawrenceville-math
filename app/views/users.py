from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
)

from sqlalchemy import select

from .. import models, forms
from ..decorators import staff_required


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
        )
    else:
        g.user = None


@bp.route("/")
@staff_required
def index():
    users = models.db_session.execute(select(models.User)).scalars().all()

    return render_template(
        "users/index.html",
        users=users,
    )


@bp.route("/login/", methods=("GET", "POST"))
def login():
    form = forms.LoginForm(request.form)

    if request.method == "POST" and form.validate():
        email, password = form.email.data, form.password.data

        user = models.db_session.execute(
            select(models.User).where(models.User.email == email)
        ).scalar()

        if user:
            if user.check_password(password):
                session["user_id"] = user.id

                return redirect(url_for("main.index"))
            else:
                form.password.errors.append("Incorrect password.")
        else:
            form.email.errors.append("Incorrect email address.")

    return render_template(
        "users/login.html",
        form=form,
    )


@bp.route("/logout/")
def logout():
    session.pop("user_id", None)

    return redirect(url_for("main.index"))


@bp.route("/register/", methods=("GET", "POST"))
def register():
    form = forms.RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        email, password = form.email.data, form.password.data

        user = models.db_session.execute(
            select(models.User).where(models.User.email == email)
        ).scalar()

        if user:
            form.email.errors.append("Taken email address.")
        else:
            user = models.User(email=email)

            user.set_password(password)

            models.db_session.add(user)
            models.db_session.commit()

            session["user_id"] = user.id

            return redirect(url_for("main.index"))

    return render_template(
        "users/registration.html",
        form=form,
    )


@bp.route("/staff/<int:id>/")
@staff_required
def switch_staff(id):
    """
    Switch the staff status of a user.
    """

    user = models.db_session.get(models.User, id)

    user.staff = not user.staff

    models.db_session.commit()

    return redirect(url_for(".index"))
