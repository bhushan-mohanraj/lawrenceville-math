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
    events = [row[0] for row in models.db_session.execute(select(models.Event)).all()]

    return render_template(
        "events/index.html",
        events=events,
    )


@bp.route("/create/", methods=("GET", "POST"))
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
        "events/create.html",
        form=form,
    )
