from flask import (
    Blueprint,
jsonify,
)

from .. import models, forms

from sqlalchemy import select


bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events",
)
