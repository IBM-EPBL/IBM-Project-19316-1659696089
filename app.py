from email import contentmanager
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def demo2():
    return render_template("demo2.html")

@app.route("/chance")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()