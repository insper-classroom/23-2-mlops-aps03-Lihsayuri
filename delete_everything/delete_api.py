import boto3
import os
from dotenv import load_dotenv
import random
import string


load_dotenv()

# Provide API Gateway name used previously
api_gateway_name = "predict-liviasm1"

api_gateway = boto3.client(
    "apigatewayv2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


response = api_gateway.get_apis(MaxResults="2000")
api_gateway_id = None
for item in response["Items"]:
    if item["Name"] == api_gateway_name:
        api_gateway_id = item["ApiId"]
        break

# Delete the API Gateway
if api_gateway_id:
    api_gateway.delete_api(ApiId=api_gateway_id)
    print(f"API Gateway '{api_gateway_name}' deleted successfully.")
else:
    print(f"API Gateway '{api_gateway_name}' not found.")