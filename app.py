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


if __name__ == "__main__":
    # debug=True restarts the server automatically when a file changes.
    app.run(debug=True)
