import requests
import time
import string

BASE_URL = "https://api.mail.tm"

def get_token(email, password):
    response = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })
    response.raise_for_status()
    return response.json()['token']

def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages", headers=headers)
    response.raise_for_status()
    return response.json()["hydra:member"]

def get_message_detail(token, message_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages/{message_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def main():
  
    email = "xxxxxx@ptct.net"
    password = "my_password"
  
    token = get_token(email, password)

    print(f"\nTemporary email address: {email}")
    print("Waiting for messages... (Ctrl+C to stop)")

    try:
        while True:
            messages = get_messages(token)
            if messages:
                print(f"\n📥 {len(messages)} message(s) received!\n")
                for msg in messages:
                    detail = get_message_detail(token, msg["id"])
                    print(f"From: {detail['from']['address']}")
                    print(f"Subject: {detail['subject']}")
                    print(f"Text: {detail['text']}\n{'-'*40}")
                break
            else:
                print("No messages yet. Checking again in 5 seconds...")
                time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
