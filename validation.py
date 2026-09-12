"""Server-side validation for the player profile submitted on the trials page.

Every check here runs on the server after the form is posted, so a submission
cannot bypass it by disabling JavaScript or editing the HTML.
"""

import data

MIN_AGE = 16
MAX_AGE = 40
MIN_SHIRT_NUMBER = 1
MAX_SHIRT_NUMBER = 30
MIN_TRAINING_DAYS = 1
MAX_TRAINING_DAYS = 7
MAX_TEXT_LENGTH = 60


def _parse_int(raw: str | None) -> int | None:
    """Return raw as a whole number, or None if it is missing or not numeric."""
    try:
        return int(raw.strip())
    except (AttributeError, ValueError):
        return None


def validate_profile(form: dict[str, str]) -> tuple[dict[str, object], dict[str, str]]:
    """Check a submitted profile and return a (profile, errors) pair.

    profile holds the cleaned values, with numbers converted to integers ready
    for the rating calculation. errors maps a field name to a message; an empty
    errors dictionary means the submission passed every check.
    """
    profile: dict[str, object] = {}
    errors: dict[str, str] = {}

    name = form.get("name", "").strip()
    if not name:
        errors["name"] = "Please enter your full name."
    elif len(name) > MAX_TEXT_LENGTH:
        errors["name"] = f"Name must be {MAX_TEXT_LENGTH} characters or fewer."
    else:
        profile["name"] = name

    age = _parse_int(form.get("age"))
    if age is None:
        errors["age"] = "Please enter your age as a whole number."
    elif not MIN_AGE <= age <= MAX_AGE:
        errors["age"] = f"Trialists must be between {MIN_AGE} and {MAX_AGE}."
    else:
        profile["age"] = age

    position = form.get("position", "")
    # Checking against the same list the template renders means a hand-edited
    # dropdown cannot smuggle in a position the app does not recognise.
    if position not in data.POSITIONS:
        errors["position"] = "Please choose one of the listed positions."
    else:
        profile["position"] = position

    foot = form.get("preferred_foot", "")
    if foot not in data.PREFERRED_FEET:
        errors["preferred_foot"] = "Please choose your preferred foot."
    else:
        profile["preferred_foot"] = foot

    shirt_number = _parse_int(form.get("shirt_number"))
    if shirt_number is None:
        errors["shirt_number"] = "Please enter a shirt number as a whole number."
    elif not MIN_SHIRT_NUMBER <= shirt_number <= MAX_SHIRT_NUMBER:
        errors["shirt_number"] = (
            f"Choose a number between {MIN_SHIRT_NUMBER} and {MAX_SHIRT_NUMBER}."
        )
    elif shirt_number in data.TAKEN_NUMBERS:
        free = data.available_numbers()
        errors["shirt_number"] = (
            f"Number {shirt_number} belongs to {data.TAKEN_NUMBERS[shirt_number]}. "
            f"Still free: {', '.join(str(number) for number in free[:8])}."
        )
    else:
        profile["shirt_number"] = shirt_number

    training_days = _parse_int(form.get("training_days"))
    if training_days is None:
        errors["training_days"] = "Please enter your training days as a whole number."
    elif not MIN_TRAINING_DAYS <= training_days <= MAX_TRAINING_DAYS:
        errors["training_days"] = (
            f"Training days must be between {MIN_TRAINING_DAYS} and {MAX_TRAINING_DAYS}."
        )
    else:
        profile["training_days"] = training_days

    club = form.get("current_club", "").strip()
    if len(club) > MAX_TEXT_LENGTH:
        errors["current_club"] = f"Club name must be {MAX_TEXT_LENGTH} characters or fewer."
    else:
        # An empty optional field reads better as a label than as a blank.
        profile["current_club"] = club or "Unattached"

    return profile, errors
