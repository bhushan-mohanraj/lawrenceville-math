from wtforms import Form, fields, validators, ValidationError


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


class RegistrationForm(Form):
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

    password_confirm = fields.PasswordField(
        "Confirm Password",
        [
            validators.InputRequired(),
            validators.EqualTo("password", message="Invalid password confirmation."),
        ],
    )

    submit = fields.SubmitField(
        "Register",
    )
