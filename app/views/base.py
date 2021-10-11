from flask import Blueprint, render_template, request, url_for, redirect, abort
from flask.views import View

from app import models
from app.decorators import staff_required


__all__ = [
    "CreateView",
    "UpdateView",
    "DeleteView",
    "register_crud_views",
]


class CRUDView(View):
    # The model and form classes used in the view.
    model: type
    form: type

    # The Flask view to redirect to after the request.
    redirect_name: str

    def model_object(self, **kwargs) -> models.Model:
        """
        Returns the model object to update or delete.

        The passed kwargs are the URL arguments.
        """

        return models.db_session.get(
            self.model,
            kwargs.get("id"),
        )

    def data(self, **kwargs) -> dict:
        """
        Returns a dictionary of other data to include when creating or updating models (outside of form data).

        The passed kwargs are the URL arguments.
        """

        return {}


class CreateView(CRUDView):
    """
    A view for creating a new model object.
    """

    methods = ["GET", "POST"]
    decorators = [staff_required]

    def dispatch_request(self, **kwargs):
        form_object = self.form(request.form)

        if request.method == "POST" and form_object.validate():
            model_object = self.model()

            form_object.populate_obj(model_object)

            for key, value in self.data(**kwargs).items():
                setattr(model_object, key, value)

            models.db_session.add(model_object)
            models.db_session.commit()

            return redirect(url_for(self.redirect_name))

        return render_template(
            "form.html",
            title="Create " + self.model.__name__,
            form=form_object,
        )


class UpdateView(CRUDView):
    """
    A view for updating a model object.

    Unless the "model_object" method is redefined,
    the route for this view should contain the integer "id" parameter.
    """

    methods = ["GET", "POST"]
    decorators = [staff_required]

    def dispatch_request(self, **kwargs):
        model_object = self.model_object(**kwargs)

        if model_object is None:
            abort(404)

        # Create the form from the request, if nonempty, or from the model.
        form_object = self.form(request.form, obj=model_object)

        if request.method == "POST" and form_object.validate():
            form_object.populate_obj(model_object)

            for key, value in self.data(**kwargs).items():
                setattr(model_object, key, value)

            models.db_session.commit()

            return redirect(url_for(self.redirect_name))

        return render_template(
            "form.html",
            title="Update " + self.model.__name__,
            form=form_object,
        )


class DeleteView(CRUDView):
    """
    A view for deleting a model object.

    Unless the "model_object" method is redefined,
    the route for this view should contain the integer "id" parameter.
    """

    methods = ["GET"]
    decorators = [staff_required]

    def dispatch_request(self, **kwargs):
        model_object = self.model_object(**kwargs)

        if model_object is None:
            abort(404)

        models.db_session.delete(model_object)
        models.db_session.commit()

        return redirect(url_for(self.redirect_name))


def register_crud_views(
    blueprint: Blueprint,
    model_: type,
    form_: type,
    redirect_name_: str,
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

        redirect_name = redirect_name_

    class ModelUpdateView(UpdateView):
        model = model_
        form = form_

        redirect_name = redirect_name_

    class ModelDeleteView(DeleteView):
        model = model_

        redirect_name = redirect_name_

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
