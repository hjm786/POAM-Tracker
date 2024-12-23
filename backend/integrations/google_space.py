import requests
from config_db import get_integration_config

def send_google_space_message(message):
    """
    Send a message to the configured Google Space Team Chat.
    """
    config = get_integration_config('google_space')
    if not config:
        raise ValueError("Google Space integration is not configured.")

    url = config['webhook_url']
    payload = {"text": message}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
    return response.json()
