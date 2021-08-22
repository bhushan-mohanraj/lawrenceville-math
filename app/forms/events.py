from .base import (
    Form,
    validators,
    StringField,
    SelectField,
    SubmitField,
    DateTimeLocalField,
    DATETIME_LOCAL_FORMAT,
)

from .. import models


class EventForm(Form):
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

    category = SelectField(
        "Category",
        [
            validators.InputRequired(),
        ],
        choices=[
            (category, category.title()) for category in models.Event.CATEGORY_CHOICES
        ],
    )

    link = StringField(
        "Link",
        [
            validators.Length(max=1000),
        ],
    )

    submit = SubmitField(
        "Submit",
    )
