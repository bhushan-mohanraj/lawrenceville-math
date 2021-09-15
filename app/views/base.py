from abc import ABC


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
