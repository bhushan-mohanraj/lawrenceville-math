from wtforms import Form, validators

from wtforms.fields import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
)

from wtforms.fields.html5 import (
    DateTimeLocalField,
)

# The default date format returned by the HTML% datetime field.
DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"
