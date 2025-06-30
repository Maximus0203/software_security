from flask import Flask, request, render_template, redirect, session
from flask_bcrypt import Bcrypt
import pyotp
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# 🔐 Session secret aus .env
app.secret_key = os.getenv("SECRET_KEY")

# ✅ Cookie-Konfiguration
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # auf True bei HTTPS
    SESSION_COOKIE_SAMESITE='Strict'
)

# Nutzer-Datenbank mit Umgebungsvariablen
USER_DB = {
    "admin": {
        "password": os.getenv("ADMIN_PASSWORD_HASH"),
        "totp_secret": os.getenv("ADMIN_TOTP_SECRET")
    }
}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = USER_DB.get(username)
        if user and bcrypt.check_password_hash(user["password"], password):
            session['username'] = username
            return redirect("/2fa")
        return "Login fehlgeschlagen!"
    return render_template("login.html")

@app.route("/2fa", methods=["GET", "POST"])
def two_factor():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        token = request.form.get("token")
        username = session["username"]
        totp = pyotp.TOTP(USER_DB[username]["totp_secret"])
        if totp.verify(token):
            session["authenticated"] = True
            return redirect("/dashboard")
        return "Ungültiger TOTP-Code!"
    return '''
        <form method="POST">
            TOTP-Code: <input name="token"><br>
            <input type="submit" value="Verify">
        </form>
    '''

@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect("/")
    return f"Willkommen im Dashboard, {session['username']}!"

if __name__ == "__main__":
    app.run(debug=True)
