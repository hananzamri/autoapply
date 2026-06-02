"""
autoapply/db/history.py
Application CRUD via Supabase.
"""
from __future__ import annotations
from datetime import datetime
from autoapply_ai.db.client import get_client


def save_application(
    user_id: str,
    company: str,
    role: str,
    job_description: str,
    resume_text: str,
    cover_letter: str,
    score: float,
) -> str | None:
    """Insert a new application record; return its UUID or None."""
    try:
        res = (
            get_client()
            .table("applications")
            .insert({
                "user_id":         user_id,
                "company":         company,
                "role":            role,
                "job_description": job_description,
                "resume_text":     resume_text,
                "cover_letter":    cover_letter,
                "score":           round(score, 2),
                "status":          "submitted",
            })
            .execute()
        )
        if res.data:
            return res.data[0].get("id")
    except Exception as e:
        print(f"Error occurred while saving application: {e}")
    return None


def get_applications(user_id: str) -> list[dict]:
    """Return all applications for user, most recent first."""
    try:
        res = (
            get_client()
            .table("applications")
            .select("id,company,role,score,status,created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        rows = res.data or []
        # Humanise the timestamp
        for r in rows:
            r["time_ago"] = _time_ago(r.get("created_at", ""))
        return rows
    except Exception:
        return []


def get_application(app_id: str) -> dict | None:
    """Fetch a single application with all fields."""
    try:
        res = (
            get_client()
            .table("applications")
            .select("*")
            .eq("id", app_id)
            .single()
            .execute()
        )
        print("GET APPLICATION:", res.data)
        return res.data
    except Exception:
        return None


def update_status(app_id: str, status: str) -> bool:
    try:
        print("APP ID:", app_id)
        print("TYPE:", type(app_id))

        res = (
            get_client()
            .table("applications")
            .update({"status": status})
            .eq("id", int(app_id))
            .execute()
        )

        print("UPDATE RESULT:", res.data)

        return True

    except Exception as e:
        print("UPDATE ERROR:", e)
        return False


# ---- Helpers ----

def _time_ago(ts: str) -> str:
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        delta = now - dt
        s = int(delta.total_seconds())
        if s < 60:       return "just now"
        if s < 3600:     return f"{s//60}m ago"
        if s < 86400:    return f"{s//3600}h ago"
        if s < 604800:   return f"{s//86400}d ago"
        return f"{s//604800}w ago"
    except Exception:
        return ""
