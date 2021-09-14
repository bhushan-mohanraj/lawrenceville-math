from wtforms import Form as BaseForm
from wtforms import validators, fields
from wtforms.fields import html5

from sqlalchemy import inspect, types


# The default date format returned by the HTML5 datetime field.
DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"


class Form(BaseForm):
    pass


def model_form(model, exclude_names=(), submit=True):
    """
    Create a WTForms Form from an SQLAlchemy Model.

    Any column names that should not be included as fields can be added to the "exclude_names" tuple.

    The ID column is, by default, not added to the form.

    A submit field, by default, is added to the form.
    """

    # TODO: Connect SQLAlchemy Column.default and WTForms Field.default.

    class ModelForm(Form):
        pass

    columns = inspect(model).c

    for column in columns:
        name = column.name

        # Skip any excluded column names and skip the ID column.
        if name in exclude_names or name == "id":
            continue

        # The field type, corresponding to the column type.
        field_type = None

        # Any keyword arguments required for constructing the field.
        field_kwargs = {
            "label": name.replace("_", " ").title(),
            "validators": [],
        }

        if column.doc:
            field_kwargs["description"] = column.doc

        # Determine the field type.
        if type(column.type) == types.Integer:
            field_type = fields.IntegerField

        elif type(column.type) == types.String:
            field_type = fields.StringField

        elif type(column.type) == types.Boolean:
            field_type = fields.BooleanField

        elif type(column.type) == types.Enum:
            field_type = fields.SelectField

            field_kwargs["choices"] = [
                (choice, choice.title()) for choice in column.type.enums
            ]

        elif type(column.type) == types.DateTime:
            field_type = html5.DateTimeField

            field_kwargs["format"] = DATETIME_LOCAL_FORMAT

        # Add the input required or optional validator.
        if not column.nullable:
            field_kwargs["validators"] += [validators.InputRequired()]
        else:
            field_kwargs["validators"] += [validators.Optional()]

        # Add the max length validator for strings.
        if isinstance(column.type, types.String):
            field_kwargs["validators"] += [validators.Length(max=column.type.length)]

        # Construct the field and add it to the form.
        setattr(
            ModelForm,
            name,
            field_type(**field_kwargs),
        )

    if submit:
        setattr(
            ModelForm,
            "submit",
            fields.SubmitField("Submit"),
        )

    return ModelForm
