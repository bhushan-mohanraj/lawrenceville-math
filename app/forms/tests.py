from app import models
from app.forms.base import *


TestForm = model_form(models.Test)

ProblemForm = model_form(
    models.Problem,
    exclude_names=("test_id",),
)

AttemptForm = model_form(
    models.Attempt,
    exclude_names=("problem_id", "user_id"),
)
