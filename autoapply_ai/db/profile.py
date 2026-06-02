from autoapply_ai.db.client import get_client


def save_profile(
    user_id: str,
    profile_name: str,
    headline: str,
    location: str,
    about: str,
    skills: str,
    education: str,
    experience: str,
    github_url: str,
    linkedin_url: str,
):
    return (
        get_client()
        .table("profiles")
        .upsert(
            {
                "user_id": user_id,
                "profile_name": profile_name,
                "headline": headline,
                "location": location,
                "about": about,
                "skills": skills,
                "education": education,
                "experience": experience,
                "github_url": github_url,
                "linkedin_url": linkedin_url,
            }
        )
        .execute()
    )


def get_profile(user_id: str):
    res = (
        get_client()
        .table("profiles")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if res.data:
        return res.data[0]

    return None