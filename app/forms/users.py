from .base import *


class LoginForm(Form):
    email = StringField(
        "Email",
        [
            validators.InputRequired(),
            validators.Email(),
        ],
    )

    password = PasswordField(
        "Password",
        [
            validators.InputRequired(),
        ],
    )

    submit = SubmitField(
        "Log In",
    )


class RegistrationForm(Form):
    email = StringField(
        "Email",
        [
            validators.InputRequired(),
            validators.Email(),
        ],
    )

    password = PasswordField(
        "Password",
        [
            validators.InputRequired(),
        ],
    )

    password_confirm = PasswordField(
        "Confirm Password",
        [
            validators.InputRequired(),
            validators.EqualTo("password", message="Invalid password confirmation."),
        ],
    )

    submit = SubmitField(
        "Register",
    )
