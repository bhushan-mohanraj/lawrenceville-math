from app import models
from app.forms.base import model_form


UserForm = model_form(
    models.User,
    exclude_names=(
        "email",
        "staff",
    ),
)
