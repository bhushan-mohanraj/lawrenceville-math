from flask import (
    Blueprint,
    render_template,
    abort,
    g,
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

    tryouts = []
    practices = []

    for test in tests:
        if test.category == test.TRYOUT:
            tryouts.append(test)
        elif test.category == test.PRACTICE:
            practices.append(test)

    return render_template(
        "tests/index.html",
        tryouts=tryouts,
        practices=practices,
    )


register_crud_views(
    bp,
    models.Test,
    forms.TestForm,
    ".index",
)


@bp.route("/<int:id>/problems/")
@user_required
def problems(id):
    test = models.db_session.get(models.Test, id)

    form = forms.AttemptForm()

    if not g.user.staff:
        if not test.active:
            return abort(404)

    return render_template(
        "tests/problems.html",
        test=test,
        form=form,
    )


class ProblemCreateView(CreateView):
    model = models.Problem
    form = forms.ProblemForm

    redirect_view_name = ".index"

    def other_data(self, **kwargs):
        return {
            "test_id": kwargs.get("test_id"),
        }


bp.add_url_rule(
    "/<int:test_id>/problems/create/",
    view_func=ProblemCreateView.as_view("create_problem"),
)


class ProblemUpdateView(UpdateView):
    model = models.Problem
    form = forms.ProblemForm

    redirect_view_name = ".index"


bp.add_url_rule(
    "/<int:test_id>/problems/<int:id>/update/",
    view_func=ProblemUpdateView.as_view("update_problem"),
)


class ProblemDeleteView(DeleteView):
    model = models.Problem
    form = forms.ProblemForm

    redirect_view_name = ".index"


bp.add_url_rule(
    "/<int:test_id>/problems/<int:id>/delete/",
    view_func=ProblemDeleteView.as_view("delete_problem"),
)
