from datetime import datetime


def current_edt_datetime() -> datetime:
    """
    The current date and time in EDT (Eastern Daylight Time, accounting for daylight savings).
    """

    return datetime.now()
