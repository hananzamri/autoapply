"""
autoapply/db/client.py
Supabase client + auth helpers (synchronous).
"""
from __future__ import annotations
import os
from dotenv import load_dotenv
load_dotenv()

from supabase import create_client, Client

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        _client = create_client(url, key)
    return _client


def supabase_login(email: str, password: str) -> dict | None:
    try:
        res = get_client().auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            return {"user_id": res.user.id, "email": res.user.email}
    except Exception as e:
        raise RuntimeError(str(e)) from e
    return None


def supabase_signup(email: str, password: str) -> dict | None:
    try:
        res = get_client().auth.sign_up({"email": email, "password": password})
        if res.user:
            return {"user_id": res.user.id, "email": res.user.email}
    except Exception as e:
        raise RuntimeError(str(e)) from e
    return None


def supabase_logout() -> None:
    try:
        get_client().auth.sign_out()
    except Exception:
        pass
