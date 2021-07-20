from wtforms import Form, fields, validators


class LoginForm(Form):
    email = fields.StringField(
        "Email",
        [
            validators.InputRequired(),
            validators.Email(),
        ],
    )

    password = fields.PasswordField(
        "Password",
        [
            validators.InputRequired(),
        ],
    )

    submit = fields.SubmitField(
        "Log In",
    )
