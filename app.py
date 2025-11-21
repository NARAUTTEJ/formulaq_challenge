import os
from datetime import datetime

from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import pytz

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# OAuth setup
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


def get_india_time():
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    return now.strftime("%d-%m-%Y %I:%M:%S %p")


# -------------------------
# PATTERN GENERATOR LOGIC
# -------------------------

def generate_pattern(n: int):
    """
    Build a FULL rhombus (diamond) using the word 'FORMULAQSOLUTIONS'.

    - Top half (including middle) has line lengths: 1, 3, 5, ..., (2*n - 1)
    - Bottom half mirrors the top (excluding the middle), so total rows = 2*n - 1
    - Same character logic as before:
        * row i starts from word index i (mod len)
        * odd rows (i = 1, 3, ...) are hollow with '-' in the middle
    """
    word = "FORMULAQSOLUTIONS"
    L = len(word)

    # First build the top half (including middle)
    top_segments = []
    for i in range(n):
        length = 1 + (i * 2)  # 1, 3, 5, ..., (2*n - 1)

        # Build continuous sequence of characters from the word
        chars = []
        for j in range(length):
            chars.append(word[(i + j) % L])
        raw_segment = "".join(chars)

        # Same dash logic as before
        if i % 2 == 0:
            segment = raw_segment
        else:
            if len(raw_segment) == 1:
                segment = raw_segment
            else:
                segment = raw_segment[0] + "-" * (len(raw_segment) - 2) + raw_segment[-1]

        top_segments.append(segment)

    # Mirror the top (excluding the middle) to get the bottom
    bottom_segments = top_segments[-2::-1]  # from second-last down to first

    all_segments = top_segments + bottom_segments

    # Center each line so the first and last lines are in the middle
    max_width = len(top_segments[-1])  # length of the middle (widest) row
    result = []
    for seg in all_segments:
        spaces = (max_width - len(seg)) // 2
        line = " " * spaces + seg
        result.append(line)

    return result


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def index():
    user = session.get("user")
    if not user:
        return render_template("index.html")

    return render_template(
        "home.html",
        name=user["name"],
        email=user["email"],
        picture=user.get("picture"),
        india_time=get_india_time(),
        pattern=None,
    )


@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/auth/callback")
def auth_callback():
    # Exchange the "code" for an access token
    token = google.authorize_access_token()  # noqa: F841 (we don't directly use token here)

    # Get user info from Google's userinfo endpoint
    resp = google.get("https://openidconnect.googleapis.com/v1/userinfo")
    userinfo = resp.json()

    # Save what you need in the session
    session["user"] = {
        "name": userinfo.get("name"),
        "email": userinfo.get("email"),
        "picture": userinfo.get("picture"),
    }

    # After login, go to the main page (which shows home if logged in)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/design", methods=["POST"])
def design():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    try:
        lines = int(request.form.get("lines"))
        if not (1 <= lines <= 100):
            raise ValueError
    except Exception:
        return render_template(
            "home.html",
            name=user["name"],
            email=user["email"],
            picture=user.get("picture"),
            india_time=get_india_time(),
            error="Enter a valid number between 1 and 100.",
            pattern=None,
        )

    pattern = generate_pattern(lines)

    return render_template(
        "home.html",
        name=user["name"],
        email=user["email"],
        picture=user.get("picture"),
        india_time=get_india_time(),
        pattern=pattern,
        lines=lines
    )


if __name__ == "__main__":
    app.run(debug=True)