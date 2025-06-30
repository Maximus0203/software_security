from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# ❌ Hardcoded credentials
HARDCODED_USER = "admin"
HARDCODED_PASS = "password123"

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ❌ Vergleich im Klartext
        if username == HARDCODED_USER and password == HARDCODED_PASS:
            # ❌ Session-ID über URL
            return f"Willkommen {username}! <a href='/dashboard?session=12345'>Dashboard</a>"
        return "Login fehlgeschlagen!"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    session = request.args.get("session", "nicht gesetzt")
    return f"""
    <!DOCTYPE html>
    <html>
      <head><title>Dashboard</title></head>
      <body>
        <h1>Willkommen im Dashboard!</h1>
        <p>Session-ID: {session}</p>
        <a href="/login">Zurück zum Login</a>
      </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
