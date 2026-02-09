import os
from flask import Flask, request, render_template, redirect, session
from supabase import create_client

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
from typing import cast

SUPABASE_URL = cast(str, os.getenv("SUPABASE_URL"))
SUPABASE_KEY = cast(str, os.getenv("SUPABASE_KEY"))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase environment variables missing")

assert SUPABASE_URL is not None
assert SUPABASE_KEY is not None

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Signup
@app.route("/")
def home():
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Supabase me insert
        data = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": password  # ideally hash karna chahiye
        }).execute()

        return redirect("/login")
    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()

        if user.data:
            session["user"] = user.data[0]["username"]
            return redirect("/quiz")
        else:
            return "Invalid credentials"
    return render_template("login.html")
@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect("/login")
    return render_template("quiz.html", username=session["user"])
