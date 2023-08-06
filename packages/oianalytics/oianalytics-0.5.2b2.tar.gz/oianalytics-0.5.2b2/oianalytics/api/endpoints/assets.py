from typing import Optional, List, Dict

import requests

from .. import _credentials

__all__ = ["get_asset_types", "get_assets", "update_single_asset_tags_and_values"]


def get_asset_types(
    page: Optional[int] = None,
    name: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/asset-types"
    response = requests.get(
        url=url,
        params={"page": page, "name": name},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_assets(
    asset_type_id: str,
    tag_value_id: Optional[List[str]] = None,
    query: Optional[int] = None,
    page: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/assets"
    response = requests.get(
        url=url,
        params={
            "page": page,
            "query": query,
            "assetTypeId": asset_type_id,
            "tagValueIds": tag_value_id,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def update_single_asset_tags_and_values(
    asset_id: str,
    tag_commands: Optional[List[Dict]] = None,
    value_commands: Optional[List[Dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Init commands
    if tag_commands is None:
        tag_commands = []

    if value_commands is None:
        value_commands = []

    # Build payload
    payload = [
        {
            "assetId": asset_id,
            "tagCommands": tag_commands,
            "staticDataValueCommands": value_commands,
        }
    ]

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/assets/tags-and-values"
    response = requests.put(url=url, json=payload, **api_credentials.auth_kwargs)

    # Output
    response.raise_for_status()
    return response.status_code
