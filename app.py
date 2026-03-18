from flask import Flask, render_template, request, redirect, session
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
import main

app = Flask(__name__)
app.secret_key = "dev"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        result = main.run(ticker)

    return render_template("index.html", result=result, user=session.get("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["user"] = username
        return redirect("/")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return redirect("/")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)