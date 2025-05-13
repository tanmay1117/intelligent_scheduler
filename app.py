from flask import Flask, render_template, request, redirect, url_for
import os
import json
from utils.calendar_api import GoogleCalendarAPI

app = Flask(__name__)
DATA_FILE = "data/tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add-task", methods=["POST"])
def add_task():
    tasks = load_tasks()
    task = {
        "name": request.form["name"],
        "priority": request.form["priority"],
        "duration": request.form["duration"],
        "energy": request.form["energy"],
        "deadline": request.form["deadline"],
    }
    tasks.append(task)
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/schedule")
def schedule():
    tasks = load_tasks()
    event_list = []

    try:
        calendar = GoogleCalendarAPI()
        events = calendar.get_upcoming_events()
        event_list = [calendar.format_event(event) for event in events]
    except Exception as e:
        event_list = [f"Error: {e}"]

    return render_template("schedule.html", schedule=tasks, events=event_list)

if __name__ == "__main__":
    app.run(debug=True)
