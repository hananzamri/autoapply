"""
autoapply/services/ai_service.py
All OpenRouter / LLM calls for the multi-agent pipeline.

FIX: API_KEY and HEADERS were built at import time, so the key was always
     an empty string on Reflex Cloud (env vars not yet loaded). Moved inside
     the _call() function so they're read fresh on every request.
"""
from __future__ import annotations
import os, json, re
import httpx

BASE_URL = "https://openrouter.ai/api/v1"
MODEL    = "anthropic/claude-3.5-haiku"


# ── low-level caller ─────────────────────────────────────────

async def _call(messages: list[dict], max_tokens: int = 2000) -> str:
    # Read key at call time, not at import time
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set — add it to Reflex Cloud env vars")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://autoapply.ai",
        "X-Title":       "AutoApply AI",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json={"model": MODEL, "messages": messages, "max_tokens": max_tokens},
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


def _extract_json(text: str) -> dict:
    """Pull the first JSON object from a response string."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {}


# ── Agent 1 — Analyzer ───────────────────────────────────────

async def analyze_job(company: str, role: str, jd: str) -> dict:
    prompt = f"""You are an expert ATS and job-description analyzer.

Analyze this job posting for **{role}** at **{company}** and respond ONLY with a valid JSON object (no markdown, no commentary):

{{
  "technical_skills": ["list", "of", "technical", "skills"],
  "soft_skills": ["communication", "..."],
  "ats_keywords": ["exactly", "as", "written", "in", "jd"],
  "responsibilities": ["key", "responsibilities"],
  "experience_level": "junior|mid|senior|lead",
  "culture_markers": ["data-driven", "fast-paced", "..."]
}}

Job Description:
{jd[:3000]}"""

    raw = await _call([{"role": "user", "content": prompt}], max_tokens=1000)
    result = _extract_json(raw)
    if not result:
        words = set(jd.lower().split())
        skills = [w for w in ["python","sql","react","typescript","figma","ai","ml",
                               "design","product","data","cloud","api","leadership",
                               "agile","ux","analytics"] if w in words]
        result = {"technical_skills": skills[:5], "ats_keywords": skills,
                  "soft_skills": [], "responsibilities": [], "experience_level": "mid"}
    return result


# ── Agent 2 — Writer ─────────────────────────────────────────

async def generate_resume(
    role: str, company: str, jd: str, base_resume: str, analysis: dict
) -> str:
    keywords = ", ".join(analysis.get("ats_keywords", [])[:10])
    prompt = f"""You are a senior resume writer specializing in ATS optimization.

Rewrite the resume below for the **{role}** position at **{company}**.

Rules:
- Weave in these ATS keywords naturally: {keywords}
- Keep all real experience, but reframe bullet points to match the JD
- Use strong action verbs (Led, Built, Designed, Optimized, Delivered…)
- Keep it concise — max 600 words
- Do NOT invent false experience
- Output plain text (no markdown headers, just clean sections)

Base Resume:
{base_resume[:2500]}

Job Description (key points):
{jd[:1500]}

Output the tailored resume text directly:"""

    return await _call([{"role": "user", "content": prompt}], max_tokens=1200)


async def generate_cover_letter(role: str, company: str, jd: str) -> str:
    prompt = f"""You are an expert cover letter writer.

Write a compelling, personalised cover letter for the **{role}** role at **{company}**.

Guidelines:
- 3 short paragraphs: opening hook, value proposition, strong close
- Reference specific things about {company} from the JD
- Sound human, confident, and enthusiastic — not generic
- Max 250 words

Job Description:
{jd[:1500]}

Write the cover letter (starting with "Dear Hiring Team"):"""

    return await _call([{"role": "user", "content": prompt}], max_tokens=600)


# ── Agent 3 — Critic ─────────────────────────────────────────

async def score_application(
    company: str, role: str, jd: str, resume: str, analysis: dict
) -> dict:
    keywords = analysis.get("ats_keywords", [])
    prompt = f"""You are a hiring manager and ATS expert evaluating a tailored job application.

Score this resume for the **{role}** at **{company}** out of 10.

Respond ONLY with JSON (no markdown):
{{
  "score": 8.5,
  "keyword_match": 87,
  "keyword_text": "one sentence about keyword alignment",
  "edge": "one sentence describing the applicant's competitive advantage"
}}

Job Keywords to check: {', '.join(keywords[:15])}

Resume (first 800 chars):
{resume[:800]}

Job Description (first 800 chars):
{jd[:800]}"""

    raw = await _call([{"role": "user", "content": prompt}], max_tokens=300)
    result = _extract_json(raw)

    score = float(result.get("score", 7.5))
    score = max(1.0, min(10.0, score))
    km    = int(result.get("keyword_match", 80))
    km    = max(0, min(100, km))

    return {
        "score":         score,
        "keyword_match": km,
        "keyword_text":  result.get("keyword_text") or f"Your resume hits {km}% of core competencies in the JD.",
        "edge":          result.get("edge") or f"Tailored application stands out against generic submissions for {role}.",
    }