import json
import pickle
import os
import pandas as pd

def load_model():
    # model_path = os.path.join(os.path.dirname(__file__), "../models/model.pkl")
    model = pickle.load(open("models/model.pkl", "rb"))
    return model

def load_encoder():
    # ohe_path = os.path.join(os.path.dirname(__file__), "../models/ohe.pkl")
    one_hot_enc = pickle.load(open("models/ohe.pkl", "rb"))
    return one_hot_enc

def lambda_handler(event, context):
    ml_models = {}
    ml_models["ohe"] = load_encoder()
    ml_models["models"] = load_model()
    print(event)

    body = json.loads(event['body'])
    print(body)
    person = body['person']
    print(person)

    person_t = ml_models["ohe"].transform(pd.DataFrame([person]))
    print(person_t)
    pred = ml_models["models"].predict(person_t)[0]
    print(pred)

    return {
        "prediction": str(pred)
        }

# if __name__ == "__main__":
#     # Simule um evento, como aquele que o AWS Lambda receberia
#     event = {
#         "body": json.dumps({
#             "person": {
#                 "age": 59,
#                 "job": "admin.",
#                 "marital": "married",
#                 "education": "secondary",
#                 "balance": 2343,
#                 "housing": "yes",
#                 "duration": 1042,
#                 "campaign": 1
#             }
#         })
#     }

#     # Chame a função lambda_handler manualmente
#     result = lambda_handler(event, None)

#     # Exiba o resultado
#     print(result)

