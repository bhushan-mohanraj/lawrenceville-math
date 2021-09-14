from datetime import datetime


def current_edt_datetime() -> datetime:
    """
    The current date and time in EDT (Eastern Daylight Time, accounting for daylight savings).
    """

    # TODO: Fix this function (currently correct only if the server is in EDT).

    return datetime.now()
