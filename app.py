from flask import Flask, render_template, request, redirect, session
from utils import get_user, get_qr_data, log_access, create_feedback, get_feedbacks, get_access_logs
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

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_access(session["user"], code, current_time)
    if code == 'final':
        return render_template("feedback.html")
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

@app.route("/view-feedback")
def view_feedback():
    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "Access denied."

    feedbacks = get_feedbacks()
    return render_template("view_feedback.html", feedbacks=feedbacks)

@app.route("/view-logs")
def view_logs():
    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "Access denied."

    logs = get_access_logs()
    return render_template("view_logs.html", logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)