from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# Signup page
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

# Login page
@app.route("/login")
def login_page():
    return render_template("login.html")

# Quiz page - only for logged-in users
@app.route("/quiz")
def quiz_page():
    if "user" not in session:
        return redirect(url_for("login_page"))
    return render_template("quiz.html")
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password required"}), 400

    # Check if user exists
    existing_user = supabase.table("users").select("*").eq("email", email).execute()
    if existing_user.data and len(existing_user.data) > 0:
        return jsonify({"success": False, "error": "Email already registered"}), 400

    # Create user
    result = supabase.table("users").insert({"email": email, "password": password}).execute()
    if result.status_code in [200, 201]:
        session["user"] = email
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Failed to create user"}), 500
