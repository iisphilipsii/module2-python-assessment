"""
Club reference data used by the Liverpool FC Talent Pathway app.
The data lives here rather than inside app.py so the route functions stay
focused on handling requests, and the content can be edited without touching
any application logic.
"""

# Each honour is a dictionary so the template can loop over the list and
# render a row per trophy without the HTML knowing how many there are.

HONOURS: list[dict[str, str | int]] = [
    {"competition": "League Titles", "count": 20, "most_recent": "2024-25"},
    {"competition": "European Cup / Champions League", "count": 6, "most_recent": "2018-19"},
    {"competition": "FA Cup", "count": 8, "most_recent": "2021-22"},
    {"competition": "League Cup", "count": 10, "most_recent": "2023-24"},
    {"competition": "UEFA Cup / Europa League", "count": 3, "most_recent": "2000-01"},
    {"competition": "UEFA Super Cup", "count": 4, "most_recent": "2019"},
    {"competition": "FIFA Club World Cup", "count": 1, "most_recent": "2019"},
]

CLUB_FACTS: list[dict[str, str]] = [
    {"label": "Founded", "value": "3 June 1892"},
    {"label": "Stadium", "value": "Anfield, Liverpool"},
    {"label": "Capacity", "value": "61,276"},
    {"label": "Nickname", "value": "The Reds"},
    {"label": "Anthem", "value": "You'll Never Walk Alone"},
    {"label": "Club Motto", "value": "This Is Anfield"},
]

# Illustrative first-team squad data for the assignment - a representative
# selection of well-known squad numbers rather than a live, current squad.
SQUAD: list[dict[str, str | int]] = [
    {"number": 1, "name": "Alisson Becker", "position": "Goalkeeper"},
    {"number": 4, "name": "Virgil van Dijk", "position": "Defender"},
    {"number": 5, "name": "Jeremy Jacquet", "position": "Defender"},
    {"number": 8, "name": "Dominik Szoboszlai", "position": "Midfielder"},
    {"number": 10, "name": "Alexis Mac Allister", "position": "Midfielder"},
    {"number": 29, "name": "Bradley Barcola", "position": "Forward"},
    {"number": 7, "name": "Florian Wirtz", "position": "Midfielder"},
    {"number": 33, "name": "Ronald Araujo", "position": "Defender"},
    {"number": 38, "name": "Ryan Gravenberch", "position": "Midfielder"},
]

# Derived from SQUAD with a dictionary comprehension so the two can never drift
# apart - add a player above and their number is marked taken automatically.
TAKEN_NUMBERS: dict[int, str] = {player["number"]: player["name"] for player in SQUAD}

# Form option lists live here so the template renders the choices from data
# and the validation in step 7 can check submissions against the same source.
POSITIONS: list[str] = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
PREFERRED_FEET: list[str] = ["Left", "Right", "Both"]
