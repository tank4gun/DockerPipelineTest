import numpy as np
import pandas as pd


def test_input_data_size():
    dataset = pd.read_csv("../data/diabetes.txt", sep='\t').to_numpy()
    dataset = np.where(np.isnan(dataset), None, dataset)
    for data_element in dataset:
        data_element_list = data_element.tolist()
        assert all(data_element_list), "Got None element in dataset: %s" % data_element_list

def test_parameters():
    dataset = pd.read_csv("../data/diabetes.txt", sep='\t').to_numpy()
    X, y = dataset[:, :-1], dataset[:, -1]
    X = X.T
    assert all([15 < age < 100 for age in X[0]]), "Got incorrect age value in dataset: %s" % [age for age in X[0] if age <= 15 or age >=100]
    assert all([sex in [1, 2] for sex in X[1]]), "Got incorrect sex value in dataset: %s" % [sex for sex in X[1] if sex not in [1, 2]]
    assert all([10 < bmi < 50 for bmi in X[2]]), "Got incorrect bmi value in dataset: %s" % [bmi for bmi in X[2] if bmi <= 10 or bmi >= 50]
    assert all([50 < bp < 200 for bp in X[3]]), "Got incorrect bp value in dataset: %s" % [bp for bp in X[3] if bp <= 50 or bp >= 200]
    assert all([80 < tc < 360 for tc in X[4]]), "Got incorrect tc value in dataset: %s" % [tc for tc in X[4] if tc <= 80 or tc >= 360]
    assert all([20 < ldl < 250 for ldl in X[5]]), "Got incorrect ldl value in dataset: %s" % [ldl for ldl in X[5] if ldl <= 20 or ldl >= 250]
    assert all([10 < hdl < 100 for hdl in X[6]]), "Got incorrect hdl value in dataset: %s" % [hdl for hdl in X[6] if hdl <= 10 or hdl >= 100]
    assert all([0 < tch < 10 for tch in X[7]]), "Got incorrect tch value in dataset: %s" % [tch for tch in X[7] if tch <= 0 or tch >= 100]
    assert all([2 < ltg < 8 for ltg in X[8]]), "Got incorrect ltg value in dataset: %s" % [ltg for ltg in X[8] if ltg <= 2 or ltg >= 8]
    assert all([40 < glu < 140 for glu in X[9]]), "Got incorrect glu value in dataset: %s" % [glu for glu in X[9] if glu <= 40 or glu >= 140]
    for data_element in dataset:
        data_element_list = data_element.tolist()
        assert all(data_element_list), "Got None element in dataset: %s" % data_element_list


test_input_data_size()
test_parameters()

