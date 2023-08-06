"""CVAT authentication utilities."""
import os
from getpass import getpass
from typing import Optional

from cvat_sdk import Client


def get_host() -> str:
    """Get the CVAT backend host."""
    cvat_host = os.getenv("CVAT_HOST")
    if cvat_host is None:
        cvat_host = input("CVAT Host: ")
    return cvat_host


def get_username() -> str:
    """Get the CVAT user."""
    username = os.getenv("CVAT_USERNAME")
    if username is None:
        username = input("CVAT User: ")
    return username


def get_password() -> str:
    """Get the CVAT password."""
    password = os.getenv("CVAT_PASSWORD")
    if password is None:
        password = getpass()
    return password


def get_org() -> str:
    """Get the CVAT organization name."""
    org = os.getenv("CVAT_ORG")
    if org is None:
        org = input("CVAT Org: ")
    return org


def get_client(
    username: Optional[str] = None,
    password: Optional[str] = None,
    org: Optional[str] = None,
) -> Client:
    """Get the CVAT SDK high-level client object."""
    if username is None:
        username = get_username()
    if password is None:
        password = get_password()
    if org is None:
        org = get_org()
    url = get_host().rstrip("/")
    client = Client(url=url, check_server_version=False)
    credentials = (username, password)
    client.login(credentials)
    client.api_client.set_default_header("x-organization", org)
    return client
