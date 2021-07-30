from flask import (
    Blueprint,
    render_template,
)

from .. import models, forms

from sqlalchemy import select


bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events",
)


@bp.route("/")
def index():
    events = [row[0] for row in models.db_session.execute(select(models.Event)).all()]

    return render_template(
        "events/index.html",
        events=events,
    )
