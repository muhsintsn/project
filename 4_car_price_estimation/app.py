from flask import Flask, request, render_template
import joblib
import pandas as pd


app = Flask(__name__)

@app.route("/", methods= ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index2.html")
    if request.method == "POST":
        data = {}
        data["age"]=int(request.form["age"])
        data["km"]= float(request.form["km"])
        data["hp_kW"]= int(request.form["hp_kW"])
        data["Gearing_Type"]=request.form["Gearing_Type"]
        data["make_model"]=request.form["make_model"]
        
        df = pd.DataFrame([data])
        df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)
        df = scaler.transform(df)
        result = model.predict(df)
        return render_template("result2.html", result=f" $ {result[0]:.4f}")
    

# api codes

@app.route("/api", methods= ["GET", "POST"])
def api():
    if request.method == "GET":
        return "my API server is running"
    if request.method == "POST":
        data = {}
        data["age"]=int(request.json["age"])
        data["km"]= float(request.json["km"])
        data["hp_kW"]= int(request.json["hp_kW"])
        data["Gearing_Type"]=request.json["Gearing_Type"]
        data["make_model"]=request.json["make_model"]
        df = pd.DataFrame([data])
        df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)
        df = scaler.transform(df)
        result = model.predict(df)
        return {"predicted_price":f" $ {result[0]:.4f}"}
    
if __name__ == "__main__":
    scaler = joblib.load(open("scaler.joblib","rb"))
    model = joblib.load(open("xgb_model.joblib","rb"))
    columns = joblib.load("columns.joblib")
    app.run(debug=True, host="0.0.0.0")
