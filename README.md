# Liverpool FC Talent Pathway

A dynamic web application built with Flask for the UCD Professional Academy
Python assignment. The site takes a visitor through a fictional trial process
at Liverpool FC: read about the club, submit a player profile, receive contract
offers calculated from that profile, and confirm the one they want.

## Live application

**https://lfc-talent-pathway.onrender.com**

The app is hosted on Render's free tier, which puts a service to sleep after
roughly 15 minutes without traffic. The first request after an idle period can
take up to a minute while the service wakes up. Every request after that is
immediate.

## Pages

| Route | Description |
| --- | --- |
| `/` | Club introduction, honours table and club facts |
| `/squad` | First team squad and which shirt numbers are still available |
| `/trials` | Player profile form, with server-side validation |
| `/offers` | Overall rating, estimated market value and available contract offers |
| `/contract` | Confirm the chosen offer, then a confirmation page |

## Features

- **Template inheritance** - every page extends `base.html`, which holds the
  shared header, navigation and footer.
- **Data driven content** - honours, club facts and the squad are Python lists
  of dictionaries rendered with Jinja loops, not hardcoded HTML.
- **Server-side validation** - `validation.py` checks every submitted field and
  returns error messages alongside the values the user already typed. Choices
  are validated against the same lists used to build the form, so a submission
  cannot bypass the checks by editing the page.
- **Shirt number availability** - the form rejects a number already held by a
  squad member and suggests numbers that are free.
- **Rating engine** - `ratings.py` scores a profile out of 100 from age band,
  training commitment and preferred foot, then derives a market value and a
  weekly wage. Offers unlock by rating, so a stronger profile sees more choices.
- **Session state** - the validated profile is held in the Flask session so it
  carries across the trials, offers and contract pages.

## Project structure

```
ucd-pa-python/
├── app.py              Flask application and route definitions
├── data.py             Club, squad and form option data
├── validation.py       Server-side validation for the profile form
├── ratings.py          Rating, market value and offer generation
├── requirements.txt    Python dependencies
├── runtime.txt         Python version for the host
├── render.yaml         Render service configuration
├── templates/
│   ├── base.html       Shared layout
│   ├── index.html      Home
│   ├── squad.html      Squad
│   ├── trials.html     Profile form
│   ├── offers.html     Rating and offers
│   └── contract.html   Confirmation and congratulations
└── static/
    └── css/
        └── style.css   Stylesheet
```

## Running it locally

Requires Python 3.12.

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Deploying to Render

1. Push the project to a GitHub repository.
2. On https://render.com, choose New + then Web Service and connect
   the repository.
3. Configure the service:
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
   - Instance Type: Free
4. Under Environment Variables, add SECRET_KEY with a long random value.
   The application reads it with os.environ.get, so no secret is stored in
   the source code. Without it the app falls back to a development-only value.
5. Deploy. Render rebuilds automatically on every push to main.

## Notes

This is a student project and is not affiliated with Liverpool Football Club.
Squad data is illustrative. Ratings, valuations and contract terms are invented
for the purposes of the assignment.
