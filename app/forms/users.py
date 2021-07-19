from wtforms import Form, fields, validators


class LoginForm(Form):
    username = fields.StringField(
        "Username",
        [
            validators.InputRequired(),
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
