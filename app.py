from flask import Flask, request, jsonify, session, redirect
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")  # keep this secret in production

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------- SIGNUP --------------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password required"}), 400

    # Check if user already exists
    existing_user = supabase.table("users").select("*").eq("email", email).execute()
    if existing_user.data and len(existing_user.data) > 0:
        return jsonify({"success": False, "error": "Email already registered"}), 400

    # Create user
    result = supabase.table("users").insert({"email": email, "password": password}).execute()
    if result.status_code == 201 or result.status_code == 200:
        session["user"] = email  # login user after signup
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Failed to create user"}), 500


# -------------------- LOGIN --------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password required"}), 400

    user = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
    if user.data and len(user.data) > 0:
        session["user"] = email
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401


# -------------------- PROTECT QUIZ --------------------
@app.route("/quiz.html")
def quiz_page():
    if "user" not in session:
        return redirect("/login.html")  # redirect to login if not signed in
    return app.send_static_file("quiz.html")
