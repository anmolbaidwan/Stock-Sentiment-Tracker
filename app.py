from flask import Flask, render_template, request, redirect, session
import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
import main

app = Flask(__name__)
app.secret_key = "dev"

users = {}
stocks = []
with open("company_tickers.json","r") as file:
    raw = json.load(file)

for value in raw.values():
    stocks.append({"ticker": value["ticker"], "name": value["title"]})

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        result = main.run(ticker)

    return render_template("index.html", result=result, stocks=stocks, user=session.get("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username not in users:
            return render_template("login.html", dne = True)
        elif users[username] == password:
            session["user"] = username
            return redirect("/")
        else:
            return render_template("login.html", wrong = True)

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users[username] = password
        session["user"] = username
        return redirect("/")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)