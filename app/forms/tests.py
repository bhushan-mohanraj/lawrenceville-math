

class AttemptForm(Form):
    answer = IntegerField(
        "Answer",
        [
            validators.InputRequired(),
        ],
    )
