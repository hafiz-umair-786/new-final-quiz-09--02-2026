import os
from flask import Flask, render_template, request, redirect, session
from supabase import create_client
from dotenv import load_dotenv

# Load local .env (Vercel will ignore)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not app.secret_key:
    raise RuntimeError("❌ Environment variables missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return redirect("/login")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Supabase Auth signup
        try:
            supabase.auth.sign_up({"email": email, "password": password})
        except Exception as e:
            return f"Signup failed: {str(e)}"

        return redirect("/login")
    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        except Exception as e:
            return f"Login failed: {str(e)}"

        if user.user:  # Successful login
            session["user"] = email
            return redirect("/quiz")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# Quiz page (protected)
@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect("/login")
    return render_template("quiz.html", user=session["user"])

# ---------------------------
# Run server (optional local dev)
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
