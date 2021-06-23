from datetime import datetime
import pandas as pd
import mleap.sklearn.pipeline
import mleap.sklearn.base
from mleap.sklearn.preprocessing.data import FeatureExtractor

import time
import pandas as pd
import math
import numpy as np
import os
import requests
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

def normalize_data(data):
    mean, std = data.mean(axis=0), data.std(axis=0)
    normalized = (data - mean) / (std * math.sqrt(442))
    return normalized, (mean, std)

unnormalized = pd.read_csv("../data/diabetes.txt", sep='\t').to_numpy()
diabetes_X, diabetes_y = unnormalized[:, :-1], unnormalized[:, -1]
diabetes_X, norma = normalize_data(diabetes_X)
# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]
diabetes_y_train = diabetes_y[:-20]
diabetes_y_test = diabetes_y[-20:]


regr = LinearRegression()
regr.mlinit(input_features="input_features", prediction_column="prediction")
regr.fit(diabetes_X_train, diabetes_y_train)
regr.intercept_ = np.array([regr.intercept_])
regr.coef_ = np.array([regr.coef_])

print("Got R2-score:", regr.score(diabetes_X_test, diabetes_y_test))

cur_time = int(time.time())
current_datetime = datetime.now()
current_datetime = current_datetime.replace(microsecond=0)

regr.serialize_to_bundle("../data", model_name="Linear-regression_{}".format(cur_time))

with open("../data/Linear-regression_{time}.node/Coef_{time}.txt".format(time=cur_time), "w") as coef_file:
    coef_file.write(" ".join(map(str, norma[0])))
    coef_file.write("\n")
    coef_file.write(" ".join(map(str, norma[1])))


with open("../data/Linear-regression_{time}.node/R2.txt".format(time=cur_time), "w") as r2_score_file:
    r2_score_file.write(str(regr.score(diabetes_X_test, diabetes_y_test)))

requests.post("http://{td_agent_host}:9880/train_log".format(td_agent_host=os.environ["TD_AGENT_HOST"]), json={"log": "[{time}]: {coef}".format(time=current_datetime.isoformat(sep=" "), coef=regr.coef_.tolist())})
