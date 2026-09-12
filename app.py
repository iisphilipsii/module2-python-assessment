"""Liverpool FC Talent Pathway - a Flask web application.

The app walks a visitor through a fictional trial process at Anfield:
read about the club, submit a player profile, receive contract offers
generated from that profile, and confirm the offer they want.
"""

import os

from flask import Flask, redirect, render_template, request, session, url_for

import data
import validation

app = Flask(__name__)

# The session cookie is signed with this key. It is read from the environment
# so the real value never appears in the source; the fallback only ever runs
# on a local development machine.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-for-production")

@app.route("/")
def home():
    """Render the club introduction page with honours and club facts."""
    return render_template("index.html", honours=data.HONOURS, facts=data.CLUB_FACTS)

@app.route("/squad")
def squad():
    """Render the first-team squad and which shirt numbers are still available."""
    return render_template(
        "squad.html",
        squad=data.SQUAD,
        taken_numbers=data.TAKEN_NUMBERS,
        shirt_range=range(1, 31),
    )

@app.route("/trials", methods=["GET", "POST"])
def trials():
    """Show the player profile form and process its submission.

    A GET renders an empty form. A POST validates the submission: if it passes,
    the cleaned profile is stored in the session and the player moves on to
    their offers, otherwise the form is redisplayed with error messages and
    the values they already typed.
    """
    errors: dict[str, str] = {}

    if request.method == "POST":
        profile, errors = validation.validate_profile(request.form)
        if not errors:
            session["profile"] = profile
            return redirect(url_for("offers"))

    return render_template(
        "trials.html",
        positions=data.POSITIONS,
        feet=data.PREFERRED_FEET,
        errors=errors,
        submitted=request.form,
    )

@app.route("/offers")
def offers():
    """Show the profile the player submitted, read back from the session."""
    profile = session.get("profile")
    # Landing here without completing the form has nothing to show, so send
    # the visitor back to fill it in.
    if profile is None:
        return redirect(url_for("trials"))

    return render_template("offers.html", profile=profile)

if __name__ == "__main__":
    # debug=True restarts the server automatically when a file changes.
    app.run(debug=True)
