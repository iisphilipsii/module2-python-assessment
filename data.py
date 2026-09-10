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
