from flask import render_template, request, url_for, redirect
from flask.views import View

from app import models
from app.decorators import staff_required


__all__ = [
    "CRUDBaseView",
    "CreateView",
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

    # By default, only staff can update objects.
    decorators = [staff_required]

    def dispatch_request(self, id):
        model_object = models.db_session.get(self.model, id)

        # test = models.db_session.get(models.Test, id)

        # if request.method == "GET":
        #     form = forms.TestForm(
        #         name=test.name,
        #         start=test.start,
        #         end=test.end,
        #         category=test.category,
        #     )
        # else:
        #     form = forms.TestForm(request.form)

        #     if form.validate():
        #         test.name = form.name.data
        #         test.start = form.start.data
        #         test.end = form.end.data
        #         test.category = form.category.data

        #         models.db_session.commit()

        #         return redirect(url_for(".index"))

        # return render_template(
        #     "form.html",
        #     title="Update Test",
        #     form=form,
        # )


class DeleteView(CRUDBaseView):
    methods = ["GET"]

    # By default, only staff can delete objects.
    decorators = [staff_required]

    def dispatch_request(self, id):
        model_object = models.db_session.get(self.model, id)

        models.db_session.delete(model_object)
        models.db_session.commit()

        return redirect(url_for(self.redirect_view_name))
