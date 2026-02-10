import os
import requests
from flask import Flask, request, session, redirect, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not app.secret_key:
    raise RuntimeError("Missing environment variables")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/quiz")
    return redirect("/login")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

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

    return "Signup failed", 401

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

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

    return "Invalid login", 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect("/login")
    return render_template("quiz.html")
@app.route("/api/questions")
def get_questions():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/questions?select=question,category,difficulty",
        headers=HEADERS
    )

    return jsonify(res.json())
@app.route("/api/quiz/next", methods=["POST"])
def next_question():
    data = request.json
    category = data.get("category")
    asked_ids = data.get("askedIds", [])

    # Fetch a random question from Supabase that has not been asked yet
    query = supabase.table("questions").select("*").neq("id", asked_ids).eq("category", category).limit(1).execute()
    if query.data:
        q = query.data[0]
        return jsonify({
            "originalIndex": q["id"],
            "question": q["question"],
            "options": [q["option1"], q["option2"], q["option3"], q["option4"]],
            "correctAnswer": q["correctAnswer"],
            "whyCorrect": q.get("whyCorrect", "")
        })
    else:
        return jsonify({"finished": True})

