import requests

# Replace with your actual VPS IP and port
url = "http://138.199.209.143:8000/grammar_assistance"

# Replace with your actual text input
data = {
    "text": "This is an example of a grammatically incorrect sentence."
}

# Send a POST request to the endpoint
response = requests.post(url, json=data , headers={"Authorization" : "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"})

print(response.json())

# Print the response
# if response.status_code == 200:
#     print("Response JSON:")
#     print(response.json())
# else:
#     print(f"Request failed with status code {response.status_code}")
