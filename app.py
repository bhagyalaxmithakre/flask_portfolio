import os
import csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")

# Projects from your resume (edit summaries/images as you wish)
PROJECTS = [
    {
        "id": 1,
        "title": "E-Commerce Website",
        "summary": "Full-stack e-commerce app with authentication, product catalog, cart, and payment integration.",
        "image": "images/project1.png",
        "slug": "e-commerce-website",
    },
    {
        "id": 2,
        "title": "Text-to-Speech Converter",
        "summary": "Multilingual speech synthesis tool using Google gTTS for accessibility and audio rendering.",
        "image": "images/project2.png",
        "slug": "text-to-speech-converter",
    },
    {
        "id": 3,
        "title": "Audio Book Generator",
        "summary": "Offline audiobook generator using pyttsx3 for converting large text into audio.",
        "image": "images/project3.png",
        "slug": "audio-book-generator",
    },
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.csv")

def save_message(name, email, message):
    write_header = not os.path.exists(MESSAGES_FILE)
    with open(MESSAGES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["name", "email", "message"])
        writer.writerow([name, email, message])

@app.route("/")
def home():
    return render_template("index.html", projects=PROJECTS)

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)

@app.route("/projects/<slug>")
def project_detail(slug):
    proj = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not proj:
        return "Project not found", 404
    return render_template("project_detail.html", project=proj)

@app.route("/resume")
def resume():
    # serve resume.pdf from static folder
    return send_from_directory(directory=os.path.join(app.root_path, "static"), path="resume.pdf", as_attachment=True)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("contact"))
        save_message(name, email, message)
        flash("Thanks! Your message has been received.", "success")
        return redirect(url_for("home"))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
