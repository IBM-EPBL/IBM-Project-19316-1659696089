from email import contentmanager
from http.client import responses
import requests
import pickle
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        arr= [300,99,1,3,2,6.8,1]
        # for i in request.form:
        #     arr.append(float(request.form[i]))
        
        lab = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        
        args=""
        for nu, la in zip(arr, lab):
            args += la+'='+str(nu)+'&'

        print('\n\nhttp://usouthcloudibm.pythonanywhere.com/logistic?'+args[:-1])
        response = requests.get('http://usouthcloudibm.pythonanywhere.com/logistic?'+args[:-1])
        res = response.json()

        percent = pickle.load(open('university_percent.pkl', 'rb')).predict([arr])
        print(percent)
        print(res)
        if res['status'] == 'True':
            return redirect(url_for('chance', percent=percent[0]))
        else:
            return redirect(url_for('chance', percent=percent[0]))
    else:
        return render_template("index.html")

@app.route("/home")
def demo2():
    return render_template("demo2.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)