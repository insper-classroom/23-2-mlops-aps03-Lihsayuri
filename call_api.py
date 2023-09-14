import requests as req
import time

#  ---------------------------- Faz o get e só checa se a API tá viva ----------------------------------------------------
print(req.get("http://localhost:8900/").text)

# ------------------------------ Faz o post com os dados de exemplo mas sem autorização --------------------------------------------------------
data = {
    "age": 42,
    "job": "entrepreneur",
    "marital": "married",
    "education": "primary",
    "balance": 558,
    "housing": "yes",
    "duration": 186,
    "campaign": 2,
}

resp = req.post("http://localhost:8900/predict", json=data)
print(f"Status code: {resp.status_code}")
print(f"Response: {resp.text}")

# ------------------------------- Daz o post com os dados de exemplo e o token ---------------------------------------------------------------
token = "abc123"

headers = {"Authorization": f"Bearer {token}"}

data1 = {
    "age": 59,
    "job": "admin.",
    "marital": "married",
    "education": "secondary",
    "balance": 2343,
    "housing": "yes",
    "duration": 1042,
    "campaign": 1,
}


data2 = {
    "age": 42,
    "job": "entrepreneur",
    "marital": "married",
    "education": "primary",
    "balance": 558,
    "housing": "yes",
    "duration": 186,
    "campaign": 2,
}

resp = req.post("http://localhost:8900/predict",
                json=data2,
                headers=headers)

print(resp.status_code)
print(resp.text)