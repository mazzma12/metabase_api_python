import os
from typing import Any

import requests
from typing_extensions import Literal

MB_API_KEY = os.getenv("MB_API_KEY", "mb_***")
MB_BASIC_AUTH_USERNAME = os.getenv("MB_BASIC_AUTH_USERNAME", "")
MB_BASIC_AUTH_PASSWORD = os.getenv("MB_BASIC_AUTH_PASSWORD", "")
MB_DOMAIN_NAME = os.getenv("MB_DOMAIN_NAME", "")


def _post(
    url: str,
    headers: dict[str, str],
    auth: requests.auth.HTTPBasicAuth,
    session: requests.Session,
    **kwargs,
) -> dict[str, Any]:
    """
    Fetch data from a given URL using the provided requests session, headers, and basic authentication.

    Args:
        url (str): The URL to fetch data from.
        headers (Dict[str, str]): The headers to include in the request.
        auth (requests.auth.HTTPBasicAuth): The basic authentication credentials.
        session (requests.Session): The requests session to use for fetching the data.

    Returns:
        Dict[str, Any]: The JSON response data as a dictionary.
    """
    response = session.post(url, headers=headers, auth=auth, **kwargs)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def process_data(
    res: dict[str, Any], column_field_name: Literal["name", "display_name"] = "name"
) -> list[dict[str, Any]]:
    """
    Process the data fetched from the URL into a list of dictionaries.

    Args:
        res (Dict[str, Any]): The response data to process.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the processed data.
    """
    cols = [col[column_field_name] for col in res["data"]["cols"]]
    items = [dict(zip(cols, row)) for row in res["data"]["rows"]]
    return items


def get_card_data(
    card_id: int,
    domain: str | None = None,
    api_key: str | None = None,
    parameters=None,
    column_field_name: Literal["name", "display_name"] = "name",
    data_format: str = "",
) -> list[dict[str, Any]]:
    """
    Main function to fetch and process data from the given domain and card ID.

    Args:
        domain (str): The domain for the API request.
        card_id (int): The card ID to query.
        api_key (str): The API key for authentication.
        username (str): The basic authentication username.
        password (str): The basic authentication password.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the processed data.
    """
    url = "/".join(
        filter(None, (f"https://{domain or MB_DOMAIN_NAME}/api/card/{card_id}/query", data_format))
    )
    headers = {
        "x-api-key": api_key or MB_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    auth = requests.auth.HTTPBasicAuth(MB_BASIC_AUTH_USERNAME, MB_BASIC_AUTH_PASSWORD)
    json_params = {"parameters": parameters} if parameters else None
    with requests.Session() as session:
        response_data = _post(url, headers, auth, session, json=json_params)
        items = process_data(response_data, column_field_name=column_field_name)
    return items


if __name__ == "__main__":
    # card_id = 922
    # items = get_card_data(card_id)
    # print(items )
    pass
