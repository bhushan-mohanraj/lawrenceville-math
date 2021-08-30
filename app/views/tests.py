from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from sqlalchemy import select

from .. import models, forms
from ..decorators import user_required, staff_required


bp = Blueprint(
    "tests",
    __name__,
    url_prefix="/tests",
)


@bp.route("/")
@user_required
def index():
    tests = models.db_session.execute(select(models.Test)).scalars().all()

    return render_template(
        "tests/index.html",
        tests=tests,
    )


@bp.route("/create/", methods=("GET", "POST"))
@staff_required
def create():
    form = forms.TestForm(request.form)

    if request.method == "POST" and form.validate():
        test = models.Test(
            name=form.name.data,
            start=form.start.data,
            end=form.end.data,
            link=form.link.data,
        )

        models.db_session.add(test)
        models.db_session.commit()

        return redirect(url_for(".index"))

    return render_template(
        "form.html",
        title="Create Test",
        form=form,
    )


@bp.route("/update/<int:id>/", methods=("GET", "POST"))
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


@bp.route("/delete/<int:id>/")
@staff_required
def delete(id):
    test = models.db_session.get(models.Test, id)

    models.db_session.delete(test)
    models.db_session.commit()

    return redirect(url_for(".index"))
