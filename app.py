from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------- HTML ROUTES --------------------
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/quiz")
def quiz_page():
    if "user" not in session:
        return redirect(url_for("login_page"))
    return render_template("quiz.html")

# -------------------- API --------------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "error": "Email and password required"}), 400

    existing = supabase.table("users").select("*").eq("email", email).execute()
    if existing.data and len(existing.data) > 0:
        return jsonify({"success": False, "error": "Email already registered"}), 400

    result = supabase.table("users").insert({"email": email, "password": password}).execute()
    if result.status_code in [200, 201]:
        session["user"] = email
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Signup failed"}), 500

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
    return jsonify({"success": False, "error": "Invalid email or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
