import os
from flask import Flask
from supabase import create_client
from dotenv import load_dotenv
import requests



headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def get_questions():
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/questions",
        headers=headers
    )
    return res.json()

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not app.secret_key:
    raise RuntimeError("Environment variables missing")

# just create client, do not use auth yet
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    return "Flask + Supabase minimal test"


