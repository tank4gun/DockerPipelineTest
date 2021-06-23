from create_app import app
from datetime import datetime
from flask import Flask, url_for, request, render_template
import pandas as pd
import mleap.sklearn.pipeline
import mleap.sklearn.base
from mleap.sklearn.preprocessing.data import FeatureExtractor

import pandas as pd
import math
import numpy as np
import os
import requests
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score


input_names = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("input_screen.html", deploy_version=app.config["deploy_version"])


@app.route("/new_model_version", methods=["POST", "GET"])
def new_model_version():
    app.config["deploy_version"] = request.json["version"] 
    return "New deploy version added", 200


@app.route("/send_data", methods=["POST"])
def send_data():
    app.logger.debug("Got request data %s", request.form)
    input_vector = np.array([float(request.form[name]) for name in input_names])
    if app.config["deploy_version"] is not None:
        new_regr = LinearRegression().deserialize_from_bundle("../data", "Linear-regression_{}.node".format(app.config['deploy_version']))
        with open("../data/Linear-regression_{version}.node/Coef_{version}.txt".format(version=app.config['deploy_version']), "r") as coef_file:
    	    means = np.array(list(map(float, coef_file.readline().split())))
    	    stds = np.array(list(map(float, coef_file.readline().split())))
        app.logger.debug("Got mean data {}, std data {}".format(means, stds))
        input_vector = np.array([float(request.form[name]) for name in input_names])
        normalized_vector = (input_vector - means) / (stds * math.sqrt(442))
        prediction = new_regr.predict([normalized_vector])[0][0]
    else:
        normalized_vector = input_vector
        prediction = normalized_vector[0]
    app.logger.debug(
        "Deploy version: {version}, input vector: {input_vector}, prediction: {prediction}".format(
            version=app.config["deploy_version"],
            input_vector=input_vector.tolist(),
            prediction=prediction,
        )
    )
    requests.post("http://{td_agent_host}:9880/app_log".format(td_agent_host=os.environ["TD_AGENT_HOST"]), json={"log": "{time} Deploy version: {version}, input vector: {input_vector}, prediction: {prediction}".format(
            time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            version=app.config["deploy_version"],
            input_vector=input_vector.tolist(),
            prediction=prediction,
        )
    })
    return render_template("result_screen.html", model_prediction=prediction)
    
