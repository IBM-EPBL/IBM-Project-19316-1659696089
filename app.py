from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        def min_max_scaling(lst):
            min_max_tup = [(290, 340), (92, 120), (1, 5), (1, 5), (1, 5), (6.5, 9.9), (0, 1)]
            for idx in range(7):
                v = lst[idx]
                lst[idx] = (v - min_max_tup[idx][0]) / (min_max_tup[idx][1] - min_max_tup[idx][0])
            return lst
        
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("demo2"))
            arr.append(float(val))

        print(arr)

        API_KEY = "wf8mge_OQdwVO8ao2kmWCtfxOfLWl8442SH44V85v2Ls"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
            })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        payload_scoring = {
            "input_data": [{"fields":[
                                        'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'
                                    ], 
                            "values": [arr]
                            }]
                        }

        response_scoring1 = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8308fd4c-24a5-46ab-96fa-263657ae4ad0/predictions?version=2022-10-18', 
            json=payload_scoring,
            headers=header).json()
        
        arr = min_max_scaling(arr)

        response_scoring2 = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/bad74619-8eab-47ee-b1bc-befef592f77f/predictions?version=2022-10-18', 
            json=payload_scoring,
            headers=header).json()
        
        print("Scoring response")
        print(response_scoring1['predictions'][0]['values'],response_scoring2['predictions'][0]['values'])
        result1 = response_scoring1['predictions'][0]['values']
        result2 = response_scoring2['predictions'][0]['values']
        if result2[0][2] == 'True':
            return redirect(url_for('chance', percent=result1[0][0]))
        else:
            return redirect(url_for('no_chance', percent=result1[0][0]))
    else:
        return redirect(url_for("demo2"))

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
    return redirect(url_for("demo2"))

if __name__ == "__main__":
    app.run(debug=True)