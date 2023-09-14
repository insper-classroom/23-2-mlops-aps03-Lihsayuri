import requests

# Change the endpoint
url_endpoing = "https://ejqzu03gh0.execute-api.us-east-2.amazonaws.com"

url = f"{url_endpoing}/predict"

# Change the phrase
body = {
    "person": {
        "age": 59,
        "job": "admin.",
        "marital": "married",
        "education": "secondary",
        "balance": 2343,
        "housing": "yes",
        "duration": 1042,
        "campaign": 1
    }
}

resp = requests.post(url, json=body) #json=body

print(f"status code: {resp.status_code}")
print(f"text: {resp.text}")