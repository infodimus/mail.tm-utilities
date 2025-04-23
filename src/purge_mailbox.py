import requests

BASE_URL = "https://api.mail.tm"
FLAG_FILE = "/tmp/mailtm_notified.flag"

# === CONFIGURE THESE VALUES ===
EMAIL_ADDRESS = "xxxxxxx@ptct.net"
EMAIL_PASSWORD = "strong_password"

# ==============================

def get_token(email, password):
    response = requests.post(f"{BASE_URL}/token", json={"address": email, "password": password})
    response.raise_for_status()
    return response.json()['token']

def purge_all_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/messages", headers=headers)
    response.raise_for_status ()
    messages = response.json().get("hydra:member", [])

    if not messages:
        print("Mailbox is already empty.")
        return

    print(f"Purging {len(messages)} message(s)...")
    for msg in messages:
        msg_id = msg["id"]
        del_response = requests.delete(f"{BASE_URL}/messages/{msg_id}", headers=headers)
        if del_response.status_code == 204:
            print(f"✅ Deleted message ID: {msg_id}")
        else:
            print(f"❌ Failed to delete message ID: {msg_id} (Status: {del_response.status_code})")


def main():
    try:
        token = get_token(EMAIL_ADDRESS, EMAIL_PASSWORD)
    except Exception as e:
        print(f"Failed to authenticate: {e}")
        return

    try:
        purge_all_messages(token)
    except Exception as e:
        print(f"Failed to fetch messages: {e}")
        return

    
if __name__ == "__main__":
    main()
