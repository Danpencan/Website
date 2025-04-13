from flask import Flask, render_template, request, redirect
import json
from datetime import datetime, timedelta

app = Flask(__name__)

BOOKING_FILE = 'bookings.json'
MAX_TABLES = 10
DURATION = timedelta(minutes=30)
ADMIN_NAME = "daniil"
ADMIN_ID = "2804"

def load_bookings():
    try:
        with open(BOOKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_booking(data):
    bookings = load_bookings()
    bookings.append(data)
    with open(BOOKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=4)

def is_available(date_str, time_str):
    bookings = load_bookings()
    new_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    count = 0
    for b in bookings:
        b_time = datetime.strptime(f"{b['date']} {b['time']}", "%Y-%m-%d %H:%M")
        if abs((new_time - b_time).total_seconds()) < DURATION.total_seconds():
            count += 1
    return count < MAX_TABLES

@app.route("/registr", methods=["GET", "POST"])
def registr():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        time = request.form["time"]
        guests = request.form["guests"]

        if is_available(date, time):
            save_booking({
                "name": name,
                "date": date,
                "time": time,
                "guests": guests
            })
            return redirect("/result")
        else:
            return redirect("/error")

    return render_template("registr.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/error_for_admin")
def error_for_admin():
    return render_template("error_for_admin.html")



@app.route("/admin/<admin_name>/<admin_id>", methods=["GET", "POST"])
def admin_dashboard(admin_name, admin_id):
    if admin_name == ADMIN_NAME and admin_id == ADMIN_ID:
        bookings = load_bookings()
        date_filter = request.args.get('date')
        if date_filter:
            bookings = [b for b in bookings if b['date'] == date_filter]

        return render_template("admin.html", bookings=bookings, admin_name=admin_name, admin_id=admin_id)
    else:
        return redirect("/error_for_admin")


if __name__ == "__main__":
    app.run(debug=True)
