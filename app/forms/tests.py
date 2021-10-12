from app import models
from app.forms.base import *


TestForm = model_form(models.Test)

ProblemForm = model_form(
    models.Problem,
    exclude_names=("test_id",),
)

ProblemAttemptForm = model_form(
    models.ProblemAttempt,
    exclude_names=(
        "problem_id",
        "user_id",
    ),
)
