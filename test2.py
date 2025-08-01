import requests

url = "https://ai-writingassistant.p.rapidapi.com/grammar_assistance"

payload = { "text": "We have scheduled a meeting in 2pm. Ensure that you will are there on time." }
headers = {
	"x-rapidapi-key": "2de6848ea7mshef489f2b9a7598ap1f7fe4jsna9db7c681545",
	"x-rapidapi-host": "ai-writingassistant.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())