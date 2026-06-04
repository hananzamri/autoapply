from __future__ import annotations
import os
from dotenv import load_dotenv
load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")
        from supabase import create_client
        _client = create_client(url, key)
    return _client

def supabase_login(email, password):
    try:
        res = get_client().auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            return {"user_id": res.user.id, "email": res.user.email}
    except Exception as e:
        raise RuntimeError(str(e)) from e
    return None

def supabase_signup(email, password):
    try:
        res = get_client().auth.sign_up({"email": email, "password": password})
        if res.user:
            return {"user_id": res.user.id, "email": res.user.email}
    except Exception as e:
        raise RuntimeError(str(e)) from e
    return None

def supabase_logout():
    try:
        get_client().auth.sign_out()
    except Exception:
        pass
