"""Turns a player profile into an overall rating, a market value and offers.

The numbers here are invented for the purposes of the assignment, but the
shape of the calculation follows how clubs actually think about a player:
age relative to peak years, commitment to training, and how rare their
attributes are.
"""

BASE_RATING = 52
MIN_RATING = 1
MAX_RATING = 99

# (lowest age, highest age, rating points, how the band is described)
AGE_BANDS: list[tuple[int, int, int, str]] = [
    (16, 20, 10, "Academy age, rated on potential rather than current output"),
    (21, 23, 14, "Approaching peak physical years"),
    (24, 28, 18, "Peak physical years"),
    (29, 32, 10, "Experienced, just past peak"),
    (33, 40, 4, "Veteran, valued for experience"),
]

# Three sessions a week is treated as the baseline, so anything above it
# adds to the rating and anything below it subtracts.
BASELINE_TRAINING_DAYS = 3
POINTS_PER_TRAINING_DAY = 3

# Two-footed players are rare, so they are scored highest.
FOOT_POINTS: dict[str, int] = {"Both": 6, "Left": 4, "Right": 2}

# Scales the wage curve so a top rated player lands on a realistic figure.
WAGE_SCALE = 15

# Value multiplier by age - a young player with the same rating is worth more
# because a buying club gets more years out of them.
AGE_VALUE_MULTIPLIERS: list[tuple[int, float]] = [
    (21, 1.3),
    (27, 1.0),
    (31, 0.7),
    (40, 0.4),
]


def age_band(age: int) -> tuple[int, str]:
    """Return the rating points and description for a player's age."""
    for lowest, highest, points, description in AGE_BANDS:
        if lowest <= age <= highest:
            return points, description
    return 0, "Outside the trial age range"


def calculate_rating(profile: dict) -> int:
    """Score a profile out of 100 from age, training commitment and foot.

    The result is clamped so no combination of inputs can produce a rating
    outside a believable range.
    """
    points, _ = age_band(profile["age"])
    training_points = (profile["training_days"] - BASELINE_TRAINING_DAYS) * POINTS_PER_TRAINING_DAY
    foot_points = FOOT_POINTS.get(profile["preferred_foot"], 0)

    rating = BASE_RATING + points + training_points + foot_points
    return max(MIN_RATING, min(MAX_RATING, rating))


def estimate_market_value(rating: int, age: int) -> int:
    """Estimate a transfer value in pounds from the rating and the age.

    Squaring the rating above a floor makes the curve steep at the top end,
    which mirrors how transfer fees behave in reality - the gap between a
    good player and an elite one is far wider than the rating gap suggests.
    """
    if rating <= 45:
        base_millions = 0.1
    else:
        base_millions = ((rating - 45) ** 2) / 45

    multiplier = AGE_VALUE_MULTIPLIERS[-1][1]
    for upper_age, value in AGE_VALUE_MULTIPLIERS:
        if age <= upper_age:
            multiplier = value
            break

    # Rounded to the nearest hundred thousand so the figure reads like a fee.
    return int(round(base_millions * multiplier * 10) / 10 * 1_000_000)


def round_to(amount: float, nearest: int = 500) -> int:
    """Round a money amount so every wage on the page reads as a tidy figure."""
    return int(round(amount / nearest) * nearest)


def weekly_wage(rating: int) -> int:
    """Derive a weekly wage in pounds from the rating."""
    return round_to((rating ** 2) * WAGE_SCALE)


def build_offers(profile: dict, rating: int) -> list[dict[str, object]]:
    """Return the contract offers a player with this rating has unlocked.

    Offers are gated on the rating, so a stronger profile is shown strictly
    more choices. The transfer offer is always available, because any player
    can be sold.
    """
    value = estimate_market_value(rating, profile["age"])
    wage = weekly_wage(rating)

    catalogue: list[dict[str, object]] = [
        {
            "key": "starter",
            "min_rating": 80,
            "title": "Senior Squad - Starting XI",
            "summary": "Named in the first eleven",
            "detail": (
                "You go straight into the starting line-up at Anfield with a "
                "four year deal and the number you asked for."
            ),
            "terms": f"4 years - GBP {wage:,} per week",
        },
        {
            "key": "rotation",
            "min_rating": 70,
            "title": "Senior Squad - Rotation",
            "summary": "In the squad, competing for a starting place",
            "detail": (
                "A three year contract with the senior squad. You will feature "
                "in cup competitions and from the bench in the league."
            ),
            "terms": f"3 years - GBP {round_to(wage * 0.7):,} per week",
        },
        {
            "key": "loan",
            "min_rating": 60,
            "title": "Loan Move",
            "summary": "A season in the Championship to build match minutes",
            "detail": (
                "You stay a Liverpool player but spend the season on loan, "
                "where regular football will do more for you than the bench."
            ),
            "terms": f"1 season on loan - GBP {round_to(wage * 0.5):,} per week",
        },
        {
            "key": "academy",
            "min_rating": 0,
            "title": "Academy Development Deal",
            "summary": "Train at Kirkby and earn your way up",
            "detail": (
                "A two year development contract at the academy, with a "
                "review at the end of each season."
            ),
            "terms": f"2 years - GBP {round_to(wage * 0.25):,} per week",
        },
        {
            "key": "transfer",
            "min_rating": 0,
            "title": "Accept a Transfer",
            "summary": "Be sold to a club willing to meet your valuation",
            "detail": (
                "The club accepts a bid and you move on. Your valuation is "
                "based on your rating and your age."
            ),
            "terms": f"Transfer fee - GBP {value:,}",
        },
    ]

    return [offer for offer in catalogue if rating >= offer["min_rating"]]
