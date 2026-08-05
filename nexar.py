import os
import sys

import requests
from dotenv import load_dotenv

TOKEN_URL = "https://identity.nexar.com/connect/token"

# get temp access token
def get_access_token():
    # Read the .env file and place its values into the environment.
    load_dotenv()

    client_id = os.getenv("NEXAR_CLIENT_ID")
    client_secret = os.getenv("NEXAR_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing Nexar credentials. Check your .env file."
        )

    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "supply.domain",
            },
            headers={
                "User-Agent": "nexar-bom-tool/0.1",
            },
            timeout=30,
        )

        # Raise an exception for HTTP errors such as 400, 401, or 500.
        response.raise_for_status()

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "The connection to Nexar timed out."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Nexar. Check your internet connection."
        ) from error

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Nexar rejected the token request. "
            f"HTTP status: {response.status_code}"
        ) from error

    token_data = response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise RuntimeError(
            "Nexar responded, but no access token was returned."
        )

    expires_in = token_data.get("expires_in")
    scope = token_data.get("scope")

    # Print token info but not token itself
    print("Successfully authenticated with Nexar.")
    print(f"Token lifetime: {expires_in} seconds")
    print(f"Granted scope: {scope}")

    return access_token