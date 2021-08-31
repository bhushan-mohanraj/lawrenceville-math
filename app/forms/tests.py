from .. import models

from .base import *


class TestForm(Form):
    name = StringField(
        "Name",
        [
            validators.InputRequired(),
            validators.Length(max=100),
        ],
    )

    start = DateTimeLocalField(
        "Start",
        [
            validators.InputRequired(),
        ],
        format=DATETIME_LOCAL_FORMAT,
    )

    end = DateTimeLocalField(
        "End",
        [
            validators.InputRequired(),
        ],
        format=DATETIME_LOCAL_FORMAT,
    )

    length = IntegerField(
        "Length (Minutes)",
        [
            validators.InputRequired(),
        ]
    )

    category = SelectField(
        "Category",
        [
            validators.InputRequired(),
        ],
        choices=[
            (category, category.title()) for category in models.Test.CATEGORY_CHOICES
        ],
    )

    submit = SubmitField(
        "Submit",
    )
