import requests

# Replace with your actual VPS IP and port
url = "http://138.199.209.143:8000/grammar_assistance"

# Replace with your actual text input
data = {
    "text": "This is an example of a grammatically incorrect sentence."
}

# Send a POST request to the endpoint
response = requests.post(url, json=data , headers={"Authorization" : "test"})

print(response.json())

# Print the response
# if response.status_code == 200:
#     print("Response JSON:")
#     print(response.json())
# else:
#     print(f"Request failed with status code {response.status_code}")
