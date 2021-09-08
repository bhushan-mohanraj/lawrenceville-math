from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from .. import models, forms

from ..decorators import (
    user_required,
    staff_required,
)

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


@bp.route("/create/", methods=("GET", "POST"))
@staff_required
def create():
    form = forms.EventForm(request.form)

    if request.method == "POST" and form.validate():
        event = models.Event(
            name=form.name.data,
            start=form.start.data,
            end=form.end.data,
            category=form.category.data,
            link=form.link.data,
        )

        models.db_session.add(event)
        models.db_session.commit()

        return redirect(url_for(".index"))

    return render_template(
        "form.html",
        title="Create Event",
        form=form,
    )


@bp.route("/<int:id>/update/", methods=("GET", "POST"))
@staff_required
def update(id):
    event = models.db_session.get(models.Event, id)

    if request.method == "GET":
        form = forms.EventForm(
            name=event.name,
            start=event.start,
            end=event.end,
            category=event.category,
            link=event.link,
        )
    else:
        form = forms.EventForm(request.form)

        if form.validate():
            event.name = form.name.data
            event.start = form.start.data
            event.end = form.end.data
            event.category = form.category.data
            event.link = form.link.data

            models.db_session.commit()

            return redirect(url_for(".index"))

    return render_template(
        "form.html",
        title="Update Event",
        form=form,
    )


@bp.route("/<int:id>/delete/")
@staff_required
def delete(id):
    event = models.db_session.get(models.Event, id)

    models.db_session.delete(event)
    models.db_session.commit()

    return redirect(url_for(".index"))
