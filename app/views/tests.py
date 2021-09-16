from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    g,
)

from sqlalchemy import select

from app import models, forms
from app.views.base import *
from app.decorators import user_required


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

    # If the user is not staff and the test has not begun, hide the problems.
    if not g.user.staff:
        if not (test.active or test.over):
            return abort(404)

    # The attempts made by the user for the problems.
    attempts = []

    if test.active:
        for problem in test.problems:
            # The attempt made by the user for the current problem.
            current_attempt = None

            for attempt in problem.attempts:
                if attempt.user_id == g.user.id:
                    current_attempt = attempt

                    break

            attempts.append(current_attempt)

    return render_template(
        "tests/problems.html",
        test=test,
        form=forms.AttemptForm(),
        attempts=attempts,
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


@bp.route("/<int:test_id>/problems/<int:problem_id>/attempt/", methods=("POST",))
@user_required
def attempt_problem(test_id, problem_id):
    test = models.db_session.get(models.Test, test_id)
    problem = models.db_session.get(models.Problem, problem_id)

    # If the test is not active, do not allow the user to attempt it.
    if not test.active:
        return abort(404)

    form = forms.AttemptForm(request.form)

    if form.validate():
        # The attempt made by the user for the problem.
        current_attempt = None

        for attempt in problem.attempts:
            if attempt.user_id == g.user.id:
                current_attempt = attempt

                break

        # Update the current attempt object if it exists, or create a new one.
        if current_attempt is None:
            new_attempt = models.Attempt(
                user_id=g.user.id,
                problem_id=problem_id,
                answer=form.answer.data,
            )

            models.db_session.add(new_attempt)
            models.db_session.commit()
        else:
            current_attempt.answer = form.answer.data

            models.db_session.commit()

    return redirect(url_for(".problems", id=test_id))


@bp.route("/<int:id>/results/")
@user_required
def results(id):
    test = models.db_session.get(models.Test, id)

    # Only display the results to users when the test is over.
    if not g.user.staff:
        if not test.over:
            abort(404)

    # The results for each user.
    results = {}

    # Find the users to display results for (show all results only to staff).
    if g.user.staff:
        users = models.db_session.execute(select(models.User)).scalars().all()
    else:
        users = [g.user]

    # Create a list of results for each user.
    for user in users:
        if not user.staff:
            results[user.email] = []

    # Find the attempts made for each problem, and add the result to the list for the corresponding user.
    for problem in test.problems:
        for attempt in problem.attempts:
            if attempt.user in users:
                results[attempt.user.email].append(1 if attempt.correct else 0)

    # Sort the results by score.
    results = {
        email: scores
        for email, scores in sorted(
            results.items(),
            key=lambda item: -sum(item[1]),
        )
    }

    return render_template(
        "tests/results.html",
        test=test,
        results=results,
        length=len(test.problems),
    )
