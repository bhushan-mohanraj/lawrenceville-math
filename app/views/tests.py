from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from sqlalchemy import select

from app import models, forms
from app.views.base import *
from app.decorators import user_required, staff_required


bp = Blueprint(
    "tests",
    __name__,
    url_prefix="/tests",
)


@bp.route("/")
@user_required
def index():
    tests = models.db_session.execute(select(models.Test)).scalars().all()
    tests = sorted(tests, key=lambda test: test.start)

    # TODO: Separate tests into tryouts and practices.
    tryouts = []
    practices = []

    return render_template(
        "tests/index.html",
        tests=tests,
    )


class TestCreateView(CreateView):
    model = models.Test
    form = forms.TestForm

    redirect_view_name = ".index"


bp.add_url_rule("/create/", view_func=TestCreateView.as_view("create"))


@bp.route("/<int:id>/update/", methods=("GET", "POST"))
@staff_required
def update(id):
    test = models.db_session.get(models.Test, id)

    if request.method == "GET":
        form = forms.TestForm(
            name=test.name,
            start=test.start,
            end=test.end,
            category=test.category,
        )
    else:
        form = forms.TestForm(request.form)

        if form.validate():
            test.name = form.name.data
            test.start = form.start.data
            test.end = form.end.data
            test.category = form.category.data

            models.db_session.commit()

            return redirect(url_for(".index"))

    return render_template(
        "form.html",
        title="Update Test",
        form=form,
    )


@bp.route("/<int:id>/delete/")
@staff_required
def delete(id):
    test = models.db_session.get(models.Test, id)

    models.db_session.delete(test)
    models.db_session.commit()

    return redirect(url_for(".index"))
