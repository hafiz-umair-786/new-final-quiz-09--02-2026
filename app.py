import os
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not SECRET_KEY:
    raise RuntimeError("Missing environment variables")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)
app.secret_key = SECRET_KEY
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        res = requests.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
            headers=HEADERS,
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            session["user"] = email
            return redirect("/quiz")

        return "Signup failed"

    return render_template("signup.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        res = requests.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
            headers=HEADERS,
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            session["user"] = email
            return redirect("/quiz")

        return "Invalid credentials"

    return render_template("login.html")
@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect("/login")

    return render_template("quiz.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

