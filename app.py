from flask import Flask, request, render_template, redirect, session
import os
from supabase import create_client

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Signup
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
