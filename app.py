from flask import Flask, render_template, request, redirect, session
import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
import main
import alert

app = Flask(__name__)
app.secret_key = "dev"

stocks = []
tracked = set()
with open("company_tickers.json","r") as file:
    raw = json.load(file)

for value in raw.values():
    stocks.append({"ticker": value["ticker"], "name": value["title"]})

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ticker = None
    chart = None
    saved = False
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker in tracked:
            saved = True
        result = main.run(ticker)
        if "error" not in result:
            chart = result["chart"]
        #alert.send_alert(session["email"], ticker)


    return render_template("index.html", result=result, stocks=stocks, chart=chart, saved=saved, user=session.get("user"))

@app.route('/save_ticker', methods=['POST'])
def save_ticker():
    ticker = request.form.get('ticker')
    tracked.add(ticker)
    main.track_ticker(session['email'], ticker)
    print(f"Ticker {ticker} saved successfully!")
    return '', 204

@app.route('/unsave_ticker', methods=['POST'])
def unsave_ticker():
    ticker = request.form.get('ticker')
    tracked.discard(ticker)
    main.untrack_ticker(session['email'], ticker)
    print(f"Ticker {ticker} removed successfully!")
    return '', 204

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not main.has_user(username):
            return render_template("login.html", dne = True)
        elif main.check_pw(username, password):
            session["user"] = username
            session['email'] = main.get_email(username)
            tracked.clear()
            tracked.update(main.get_tracked(session['email']))
            return redirect("/")
        else:
            return render_template("login.html", wrong = True)

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        session["user"] = username
        session["email"] = email
        try:
            alert.register_email(session["email"], session["user"])
            main.signup(email, username, password)
            tracked.clear()
        except Exception as error:
            print("Error:", error)
            return render_template("signup.html", errmail = True)
        return redirect("/")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    tracked.clear()
    return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    trackString = ", ".join(sorted(tracked))
    return render_template("profile.html", user=session.get("user"), email=session.get("email"), tracked=trackString)

@app.route("/profile/edit", methods=["GET", "POST"])
def update_profile():
    if request.method == "POST":
        newusername = request.form.get("username")
        password = request.form.get("password")
        #if password != users[username]:
         #   return render_template("profile.html", edit=True, user=session.get("user"), email=session.get("email"), tracked=tracked, wrong=True)
        session["user"] = newusername
        main.edit_username(session['email'], newusername)
        return render_template("profile.html", user=session.get("user"), email=session.get("email"), tracked=tracked)

    return render_template("profile.html", edit=True, user=session.get("user"), email=session.get("email"), tracked=tracked)

if __name__ == "__main__":
    app.run(debug=True, port=8080, use_reloader = False)