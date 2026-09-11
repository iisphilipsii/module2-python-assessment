"""Liverpool FC Talent Pathway - a Flask web application.

The app walks a visitor through a fictional trial process at Anfield:
read about the club, submit a player profile, receive contract offers
generated from that profile, and confirm the offer they want.
"""

from flask import Flask, render_template

import data

app = Flask(__name__)


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

if __name__ == "__main__":
    # debug=True restarts the server automatically when a file changes.
    app.run(debug=True)
