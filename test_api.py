import boto3
import requests
from requests_aws4auth import AWS4Auth

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    "us-west-2",
    "execute-api",
    session_token=credentials.token
)

url = "https://5f7l8kpt21.execute-api.us-west-2.amazonaws.com/inventory"

response = requests.post(
    url,
    auth=auth,
    headers={"Content-Type": "application/json"},
    json={
        "item": "Final Low Stock Test",
	"quantity": 2,
	"unit": "units",
	"minimum_stock": 5
    }
)

print(response.status_code)
print(response.text)
