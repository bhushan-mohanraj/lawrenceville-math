from wtforms import Form, validators, ValidationError

from wtforms.fields import (
    StringField,
    IntegerField,
    PasswordField,
    SelectField,
    SubmitField,
)

from wtforms.fields.html5 import (
    DateTimeLocalField,
)

# The default date format returned by the HTML5 datetime field.
DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"
