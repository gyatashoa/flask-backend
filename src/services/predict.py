import os
import pickle
import json
# import pandas as pd

__symptom_headers = None
__model = None
# __drug_db = None

__path_to_artifacts = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'artifacts')


# def load_drug():
#     global __drug_db
#     __drug_db = pd.read_csv(os.path.join(
#         __path_to_artifacts, 'diseases_drugs.csv'))


def load_symptoms():
    global __symptom_headers
    with open(os.path.join(__path_to_artifacts, 'symptom_columns.json'), 'r') as f:
        __symptom_headers = json.load(f)['symptom_names']


def load_model():
    global __model
    with open(os.path.join(__path_to_artifacts, 'mnb_model.pickle'), 'rb') as m:
        __model = pickle.load(m)


def make_prediction(symptoms):
    encoded_values: list[int] = []
    if __symptom_headers is None:
        load_symptoms()

    if __model is None:
        load_model()

    for s in __symptom_headers:
        try:
            index = symptoms.index(s)
            encoded_values.append(1)
        except ValueError as err:
            encoded_values.append(0)
    value = __model.predict([encoded_values])
    prob = (__model.predict_proba([encoded_values])).max()
    return value[0], prob


def get_symptoms():
    if __symptom_headers is None:
        load_symptoms()
    return __symptom_headers


print(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))), 'artifacts', 'mnb_model.pickle'))
