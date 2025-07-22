from flask import Flask, render_template, request, redirect, session
from utils import get_user, get_qr_data, log_access, create_feedback
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = get_user(request.form["username"], request.form["password"])
        if user:
            session["user"] = user[1]
            return redirect("/scan")
    return render_template("login.html")

@app.route("/scan")
def scan():
    if "user" not in session:
        return redirect("/")
    return render_template("scan.html")

@app.route("/page/<code>")
def page(code):
    if "user" not in session:
        return redirect("/")

    qr = get_qr_data(code)
    if not qr:
        return "Invalid QR code."
    if code == 'final':
        return render_template("feedback.html")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_access(session["user"], code, current_time)
    return render_template("page.html", qr=qr)


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    rating_event = request.form.get("rating_event")
    rating_portal = request.form.get("rating_portal")
    comments = request.form.get("comments")

    create_feedback(username,rating_event,rating_portal,comments)
    return render_template("thanks.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)