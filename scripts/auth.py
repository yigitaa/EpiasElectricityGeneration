# auth.py
import requests
from urllib.parse import urlencode

# CAS TGT endpoint
CAS_TGT_URL = "https://giris.epias.com.tr/cas/v1/tickets"

def get_tgt(username, password):
    """
    Fetch a Ticket Granting Ticket (TGT) from the CAS server.

    Args:
        username (str): CAS username.
        password (str): CAS password.

    Returns:
        str: The TGT if successful, otherwise None.
    """
    try:
        # request payload
        payload = {
            "username": username,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }

        # POST req.
        print("Fetching TGT...")
        response = requests.post(CAS_TGT_URL, data=urlencode(payload), headers=headers, timeout=10)
        response.raise_for_status()  # raise an error

        # extract tgt from response body
        tgt = response.text.strip()  # Remove any leading/trailing whitespace
        if tgt:
            print("TGT fetched successfully.")
            return tgt
        else:
            print("TGT not found in the response body.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TGT: {e}")
        return None