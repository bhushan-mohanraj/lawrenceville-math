from pytz import timezone
from datetime import datetime


def current_edt_datetime() -> datetime:
    """
    The current date and time in EDT (Eastern Daylight Time, accounting for daylight savings).
    """

    edt = timezone("US/Eastern")

    return datetime.now(edt).replace(tzinfo=None)


def title(string: str) -> str:
    """
    Format a string in title case.

    This differs from string.title() by preserving
    letters within each word that are already uppercase.
    For example, "made in the USA" becomes "Made In The USA"
    rather than "Made In The Usa."

    Based on https://stackoverflow.com/questions/25512102.
    """

    return "".join(
        [
            character if character.isupper() else title_character
            for character, title_character in zip(string, string.title())
        ]
    )
