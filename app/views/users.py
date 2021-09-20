"""
Authenticate users with Google.

See https://developers.google.com/identity/protocols/oauth2/web-server.
See https://developers.google.com/identity/protocols/oauth2/scopes.
"""

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
)

from sqlalchemy import select

import google_auth_oauthlib.flow

from app import models
from app.decorators import staff_required

import json


bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
)


# Details for Google authentication.
CLIENT_SECRETS = json.loads(
    current_app.config["GOOGLE_CLIENT_SECRETS"],
)

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# Emails of staff members (others can be added through the website).
STAFF_EMAILS = [
    "bmohanraj24@lawrenceville.org",
]


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


@bp.route("/login/")
def login():
    # See https://developers.google.com/identity/protocols/oauth2/web-server.

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        CLIENT_SECRETS,
        scopes=SCOPES,
        redirect_uri=url_for(".login_callback", _external=True),
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )

    session["state"] = state

    return redirect(authorization_url)


@bp.route("/login/callback/")
def login_callback():
    state = session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        CLIENT_SECRETS,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for(".login_callback", _external=True),
    )

    flow.fetch_token(authorization_response=request.url)

    user_details = (
        flow.authorized_session()
        .get("https://www.googleapis.com/userinfo/v2/me")
        .json()
    )

    email = user_details["email"]
    name = user_details["name"]

    user = (
        models.db_session.execute(select(models.User).where(models.User.email == email))
        .scalars()
        .first()
    )

    if user:
        session["user_id"] = user.id

        return redirect(url_for("index"))
    else:
        user = models.User(
            email=email,
            name=name,
        )

        if email in STAFF_EMAILS:
            user.staff = True

        models.db_session.add(user)
        models.db_session.commit()

        session["user_id"] = user.id

        return redirect(url_for("index"))


@bp.route("/logout/")
def logout():
    session.pop("user_id", None)

    return redirect(url_for("index"))


@bp.route("/<int:id>/staff/")
@staff_required
def staff(id):
    """
    Switch the staff status of a user.
    """

    user = models.db_session.get(models.User, id)

    user.staff = not user.staff

    models.db_session.commit()

    return redirect(url_for(".index"))
