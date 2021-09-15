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


register_crud_views(
    bp,
    models.Test,
    forms.TestForm,
    ".index",
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




