import requests

# Replace with your actual VPS IP and port
url = "http://138.199.209.143:8000/grammar_assistance"

# Replace with your actual text input
data = {
    "text": "I would like to buy some fishes , 2 tonans please! Make them as saltiii as posibel\nI would like to buy some fishes , 2 tonans please! Make them as saltiii as posibel\nI would like to buy some fishes , 2 tonans please! Make them as saltiii as posibel\nI would like to buy some fishes , 2 tonans please! Make them as saltiii as posibel\nI would like to buy some fishes , 2 tonans please! Make them as saltiii as posibel\nI would like to buy some fishes , 2 tonans please! Make them as saltiii as posibel"
}

# Send a POST request to the endpoint
response = requests.post(url, json=data , headers={"Authorization" : "test"})

print(response.status_code)
try: 
    print(response.json())
except Exception as e: 
    print(e)

# Print the response
# if response.status_code == 200:
#     print("Response JSON:")
#     print(response.json())
# else:
#     print(f"Request failed with status code {response.status_code}")
