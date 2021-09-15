from flask import render_template, request, url_for, redirect
from flask.views import View

from app import models
from app.decorators import staff_required


__all__ = [
    "CreateView",
    "UpdateView",
    "DeleteView",
]


class CRUDBaseView(View):
    """
    The base class for CRUD views.
    """

    model = None  # The SQLAlchemy model class.
    form = None  # The WTForms form class, with form fields matching model columns.

    template_name: str  # The template name used for displaying objects or forms.

    redirect_view_name: str  # The view name to redirect to after processing.


class CreateView(CRUDBaseView):
    methods = ["GET", "POST"]
    decorators = [staff_required]

    template_name = "form.html"  # Use the form template for rendering the create form.

    def dispatch_request(self):
        form_object = self.form(request.form)

        if request.method == "POST" and form_object.validate():
            model_object = self.model()

            form_object.populate_obj(model_object)

            models.db_session.add(model_object)
            models.db_session.commit()

            return redirect(url_for(self.redirect_view_name))

        return render_template(
            self.template_name,
            title="Create " + self.model.__name__,
            form=form_object,
        )


class UpdateView(CRUDBaseView):
    methods = ["GET", "POST"]
    decorators = [staff_required]

    template_name = "form.html"  # Use the form template for rendering the update form.

    def dispatch_request(self, id):
        model_object = models.db_session.get(self.model, id)

        # Create the form from the request form, if it exists, or from the model.
        form_object = self.form(request.form, obj=model_object)

        if request.method == "POST" and form_object.validate():
            form_object.populate_obj(model_object)

            models.db_session.commit()

            return redirect(url_for(self.redirect_view_name))

        return render_template(
            self.template_name,
            title="Update " + self.model.__name__,
            form=form_object,
        )


class DeleteView(CRUDBaseView):
    methods = ["GET"]

    # By default, only staff can delete objects.
    decorators = [staff_required]

    def dispatch_request(self, id):
        model_object = models.db_session.get(self.model, id)

        models.db_session.delete(model_object)
        models.db_session.commit()

        return redirect(url_for(self.redirect_view_name))
