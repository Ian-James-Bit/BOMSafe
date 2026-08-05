import os
from typing import Any

from pathlib import Path

import requests
from dotenv import load_dotenv

TOKEN_URL = "https://identity.nexar.com/connect/token"
GRAPHQL_URL = "https://api.nexar.com/graphql"

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

#getting the GraphQL query text from the queries directory
QUERY_DIRECTORY = Path(__file__).parent / "queries"

def load_query(filename: str) -> str:
    query_path = QUERY_DIRECTORY / filename
    return query_path.read_text(encoding="utf-8")

PART_OFFERS_QUERY = load_query("part_offers.graphql")

"""
Send a GraphQL query to Nexar.

access_token: Temporary Nexar access token.
query: GraphQL query text.
variables: Values inserted into the GraphQL query.

Returns: The GraphQL response's data section.
"""
def execute_graphql(access_token: str,query: str,variables: dict[str, Any]):
    try:
        response = requests.post(
            GRAPHQL_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "User-Agent": "nexar-bom-tool/0.1",
            },
            json={
                "query": query,
                "variables": variables,
            },
            timeout=60,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"GraphQL request failed: {error}"
        ) from error

    response_data = response.json()

    # GraphQL can return HTTP 200 but still report query errors.
    if response_data.get("errors"):
        raise RuntimeError(
            f"GraphQL errors: {response_data['errors']}"
        )

    data = response_data.get("data")

    if data is None:
        raise RuntimeError(
            "Nexar returned no data."
        )

    return data

#Retrieve supplier offers for one manufacturer part number.
def get_part_offers(access_token: str,mpn: str):
    variables = {
        "queries": [
            {
                "mpn": mpn,
                "start": 0, #minimum index of the first hit to return.
                "limit": 1, #how many hits are returned per query.
            }
        ]
    }

    return execute_graphql(
        access_token=access_token,
        query=PART_OFFERS_QUERY,
        variables=variables,
    )