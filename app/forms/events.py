from wtforms import Form, fields, validators

from .. import models


class EventForm(Form):
    name = fields.StringField(
        "Name",
        [
            validators.InputRequired(),
            validators.Length(max=100),
        ],
    )

    start = fields.DateTimeField(
        "Start",
        [
            validators.InputRequired(),
        ],
    )

    end = fields.DateTimeField(
        "End",
        [
            validators.InputRequired(),
        ],
    )

    category = fields.SelectField(
        "Category",
        [
            validators.InputRequired(),
        ],
        choices=[(category, category.name) for category in models.Event.CategoryEnum],
    )

    link = fields.StringField(
        "Link",
        [
            validators.Length(max=1000),
        ]
    )
