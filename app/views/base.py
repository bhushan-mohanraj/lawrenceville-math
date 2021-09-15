from abc import ABC

from flask import render_template, request, url_for, redirect
from flask.views import View

from app import models
from app.decorators import staff_required


__all__ = [
    "CRUDBaseView",
    "CreateView",
]


class CRUDBaseView(View, ABC):
    """
    The base class for views that create, read, update, or delete model objects.
    """

    # The SQLAlchemy model class.
    model_class = None

    # The WTForms form class, with form fields matching model columns.
    form_class = None

    # The template name used for displaying objects or forms.
    template_name: str

    # The view name to redirect to.
    redirect_name: str


class CreateView(CRUDBaseView):
    methods = ["GET", "POST"]
    decorators = [staff_required]

    # Use the form template for rendering the create form.
    template_name = "form.html"

    def dispatch_request(self):
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            model = self.model_class()

            for field in form:
                if field.name in self.model_class.__table__.columns.keys():
                    setattr(
                        model,
                        field.name,
                        field.data,
                    )

            models.db_session.add(model)
            models.db_session.commit()

            return redirect(url_for(self.redirect_name))

        return render_template(
            self.template_name,
            title="Create " + self.model_class.__name__,
            form=form,
        )
