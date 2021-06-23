import numpy as np
import os
import pandas as pd
import math
import mleap.sklearn.pipeline
import mleap.sklearn.base
import requests
from mleap.sklearn.preprocessing.data import FeatureExtractor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def get_best_model():
    timestamps = [path.split("_")[1].split(".")[0] for path in os.listdir("./../data") if path.startswith("Linear")]
    candidates = []
    for timestamp in timestamps:
        if os.path.exists("../data/Linear-regression_{version}.node/R2.txt".format(version=timestamp)):
            with open("../data/Linear-regression_{version}.node/R2.txt".format(version=timestamp), "r") as r2_file:
                candidates.append((float(r2_file.readline()), timestamp))
    max_candidate = candidates[0]
    for candidate in candidates:
        if max_candidate[0] <= candidate[0] and int(max_candidate[1]) < int(candidate[1]):
            max_candidate = candidate
    return max_candidate[1]


def normalize_vector(input_vector, best_model_ts):
    with open("../data/Linear-regression_{version}.node/Coef_{version}.txt".format(version=best_model_ts), "r") as coef_file:
        means = np.array(list(map(float, coef_file.readline().split())))
        stds = np.array(list(map(float, coef_file.readline().split())))
    input_vector = np.array(input_vector)
    normalized_vector = (input_vector - means) / (stds * math.sqrt(442))
    return normalized_vector


def test_correct_output_format(model, model_ts, input_vector):
    normalized_vector = normalize_vector(input_vector, model_ts)
    prediction = model.predict([normalized_vector]).tolist()
    assert isinstance(prediction, list) and isinstance(prediction[0], list), "Got bad prediction, should be list with one value, got: %s" % prediction
    prediction = prediction[0][0]
    assert isinstance(prediction, float), "Got bad prediction type: %s" % type(prediction)


def normalize_data(data):
    mean, std = data.mean(axis=0), data.std(axis=0)
    normalized = (data - mean) / (std * math.sqrt(442))
    return normalized, (mean, std)


def test_model_is_better_than_border(model):
    unnormalized = pd.read_csv("../data/diabetes.txt", sep='\t').to_numpy()
    diabetes_X, diabetes_y = unnormalized[:, :-1], unnormalized[:, -1]
    diabetes_X, norma = normalize_data(diabetes_X)
    diabetes_X_test = diabetes_X[-20:]
    diabetes_y_test = diabetes_y[-20:]
    model_score = model.score(diabetes_X_test, diabetes_y_test)
    assert model_score > 0.51, "Got too low best model score: %s" % model_score


def send_best_model_version(best_model_version):
    requests.post("http://flask_app:5100/new_model_version", json={"version": best_model_version})


def test_best_model():
    best_model_ts = get_best_model()
    best_model = LinearRegression().deserialize_from_bundle("../data", "Linear-regression_{}.node".format(best_model_ts))
    test_correct_output_format(best_model, best_model_ts, [59, 2, 32.1, 101, 157, 93.2, 38, 4, 4.8598, 87])
    test_model_is_better_than_border(best_model)
    send_best_model_version(best_model_ts)


test_best_model()

