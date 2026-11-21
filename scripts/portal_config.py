"""Read public navigation settings only; no credentials or business data."""

import ipaddress
import os
import re
from dataclasses import dataclass
from urllib.parse import urlsplit

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


@dataclass(frozen=True)
class Service:
    slug: str
    title: str
    description: str
    setting: str



def read_setting(name):
    """Environment variables override optional Streamlit secrets, including blanks."""
    if name in os.environ:
        return os.environ[name]
    try:
        value = st.secrets.get(name, "")
    except (FileNotFoundError, StreamlitSecretNotFoundError):
        return ""
    return value if isinstance(value, str) else ""


def valid_app_url(value):
    """Accept absolute HTTP(S) URLs without credentials or ambiguous characters."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or any(c.isspace() or ord(c) < 32 or c in '\\<>\"\'`' for c in value):
        return None
    try:
        url = urlsplit(value)
        host = url.hostname
        if (url.scheme not in ("https", "http") or not host
                or url.username is not None or url.password is not None
                or url.port == 0 or url.netloc.endswith(":")):
            return None
        # Validate IPv6 literals separately from DNS names and IPv4.
        if ":" in host:
            ipaddress.IPv6Address(host)
        else:
            host = host.encode("idna").decode("ascii")
            if len(host) > 253 or any(not re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
                                      for label in host.rstrip(".").split(".")):
                return None
    except (ValueError, UnicodeError):
        return None
    return value
