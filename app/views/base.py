from flask import Blueprint, render_template, request, url_for, redirect
from flask.views import View

from app import models
from app.decorators import staff_required


__all__ = [
    "CreateView",
    "UpdateView",
    "DeleteView",
    "register_crud_views",
]


class CRUDBaseView(View):
    """
    The base class for CRUD views.
    """

    model: type  # The SQLAlchemy model class.
    form: type  # The WTForms form class, with form fields matching model columns.

    template_name: str  # The template name used for displaying objects or forms.

    redirect_view_name: str  # The view name to redirect to after processing.

    def other_data(self, **kwargs) -> dict:
        """
        Returns a dictionary of other data (outside submitted forms) to include in creating or updating models.

        The dictionary keys should be column names and the values should be the desired column values.

        The keyword arguments passed to this function are, by default, URL parameters from the view.
        """

        return {}


class CreateView(CRUDBaseView):
    methods = ["GET", "POST"]
    decorators = [staff_required]

    template_name = "form.html"  # Use the form template for rendering the create form.

    def dispatch_request(self, **kwargs):
        form_object = self.form(request.form)

        if request.method == "POST" and form_object.validate():
            model_object = self.model()

            form_object.populate_obj(model_object)

            for key, value in self.other_data(**kwargs):
                setattr(model_object, key, value)

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

    def dispatch_request(self, **kwargs):
        model_object = models.db_session.get(self.model, kwargs.get("id"))

        # Create the form from the request form, if it exists, or from the model.
        form_object = self.form(request.form, obj=model_object)

        if request.method == "POST" and form_object.validate():
            form_object.populate_obj(model_object)

            for key, value in self.other_data(**kwargs):
                setattr(model_object, key, value)

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

    def dispatch_request(self, **kwargs):
        model_object = models.db_session.get(self.model, kwargs.get("id"))

        models.db_session.delete(model_object)
        models.db_session.commit()

        return redirect(url_for(self.redirect_view_name))


def register_crud_views(
    blueprint: Blueprint,
    model_: type,
    form_: type,
    redirect_view_name_: str,
    url_prefix: str = "",
    view_name_prefix: str = "",
):
    """
    Register a CreateView, UpdateView, and DeleteView to a blueprint.

    A URL prefix can be added, which should start, but not end, with a slash.

    The views are named "create", "update", and "delete" by default.
    This means they can be accessed, for example, by url_for("bp.create").
    A view name prefix can be added to prefix these names.

    Underscores are used after certain parameters because of Python's variable scopes.
    """

    class ModelCreateView(CreateView):
        model = model_
        form = form_

        redirect_view_name = redirect_view_name_

    class ModelUpdateView(UpdateView):
        model = model_
        form = form_

        redirect_view_name = redirect_view_name_

    class ModelDeleteView(DeleteView):
        model = model_

        redirect_view_name = redirect_view_name_

    blueprint.add_url_rule(
        url_prefix + "/create/",
        view_func=ModelCreateView.as_view(view_name_prefix + "create"),
    )

    blueprint.add_url_rule(
        url_prefix + "/<int:id>/update/",
        view_func=ModelUpdateView.as_view(view_name_prefix + "update"),
    )

    blueprint.add_url_rule(
        url_prefix + "/<int:id>/delete/",
        view_func=ModelDeleteView.as_view(view_name_prefix + "delete"),
    )
