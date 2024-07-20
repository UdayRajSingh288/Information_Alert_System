import requests

url = "https://mail-sender-api1.p.rapidapi.com/"


headers = {
	"x-rapidapi-key": "a483jdvbhjbjvkjjknj3ac3c2dc8fa",
	"x-rapidapi-host": "mail-sender-api1.p.rapidapi.com",
	"Content-Type": "application/json"
}


def send_email(st, t, b):
	payload = {
	"sendto": st,
	"name": "Information Alert System",
	"replyTo": "noreply@InfoAlertSystem.com",
	"ishtml": "false",
	"title": t,
	"body": b
	}
	response = requests.post(url, json=payload, headers=headers)
	print(response.json())

if __name__ == '__main__':
	send_email('captainswing817@gmail.com', 'Test', 'Hi :)')