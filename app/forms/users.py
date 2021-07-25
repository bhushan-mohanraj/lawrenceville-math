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
        ],
    )

    submit = fields.SubmitField(
        "Register",
    )

    def validate_password_confirm(self, field):
        if field.data != self.password.data:
            raise ValidationError("The password confirmation must match with the password.")
