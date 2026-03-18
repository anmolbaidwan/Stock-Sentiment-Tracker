from flask import Flask, render_template, request
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import main

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        result = main.run(ticker)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)