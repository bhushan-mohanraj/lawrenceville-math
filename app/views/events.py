from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from app import models, forms
from app.views.base import *
from app.decorators import user_required, staff_required

from sqlalchemy import select


bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events",
)


@bp.route("/")
@user_required
def index():
    events = models.db_session.execute(select(models.Event)).scalars().all()
    events = sorted(events, key=lambda event: event.start)

    meetings = []
    contests = []

    for event in events:
        if event.category == event.MEETING:
            meetings.append(event)
        elif event.category == event.CONTEST:
            contests.append(event)

    return render_template(
        "events/index.html",
        meetings=meetings,
        contests=contests,
    )


register_crud_views(
    bp,
    models.Event,
    forms.EventForm,
    ".index",
)
