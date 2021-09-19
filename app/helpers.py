from pytz import timezone
from datetime import datetime


def current_edt_datetime() -> datetime:
    """
    The current date and time in EDT (Eastern Daylight Time, accounting for daylight savings).
    """

    edt = timezone("US/Eastern")

    return datetime.now(edt).replace(tzinfo=None)
