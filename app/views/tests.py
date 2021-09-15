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


class TestUpdateView(UpdateView):
    model = models.Test
    form = forms.TestForm

    redirect_view_name = ".index"


class TestDeleteView(DeleteView):
    model = models.Test

    redirect_view_name = ".index"


bp.add_url_rule("/create/", view_func=TestCreateView.as_view("create"))
bp.add_url_rule("/<int:id>/update/", view_func=TestUpdateView.as_view("update"))
bp.add_url_rule("/<int:id>/delete/", view_func=TestDeleteView.as_view("delete"))
