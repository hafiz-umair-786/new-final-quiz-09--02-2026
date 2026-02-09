import os
from flask import Flask, jsonify
from supabase import create_client
from dotenv import load_dotenv
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not SECRET_KEY:
    raise RuntimeError("Missing environment variables")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = SECRET_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    return "Flask + Supabase minimal test"

@app.route("/questions")
def questions():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/questions", headers=headers)
    return jsonify(res.json())

# Required for Vercel
app = app
