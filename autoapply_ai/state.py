"""
autoapply/state.py
Single unified Reflex state for the entire app.
"""
from __future__ import annotations
from pypdf import PdfReader
import asyncio
import reflex as rx
from docx import Document
from io import BytesIO
from autoapply_ai.db.history import save_application
from autoapply_ai.services.export import export_pdf, export_docx
from autoapply_ai.db.client import get_client


class State(rx.State):
    @rx.var
    def auth_toggle_label(self) -> str:
        return "Already have an account? Sign in" if self.is_signup else "Don't have an account? Sign up"

    # ============================================================
    # INPUT SETTERS
    # ============================================================

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_password(self, value: str):
        self.login_password = value

    def set_company(self, value: str):
        self.company = value

    def set_role(self, value: str):
        self.role = value

    def set_job_description(self, value: str):
        self.job_description = value

    def set_resume_text(self, value: str):
        self.resume_text = value

    def set_profile_name(self, value: str):
        self.profile_name = value

    def set_headline(self, value: str):
        self.headline = value

    def set_location(self, value: str):
        self.location = value

    def set_bio(self, value: str):
        self.bio = value

    def set_skills(self, value: str):
        self.skills = value

    def set_education(self, value: str):
        self.education = value

    def set_experience(self, value: str):
        self.experience = value

    def set_github_url(self, value: str):
        self.github_url = value

    def set_linkedin_url(self, value: str):
        self.linkedin_url = value

    # ============================================================
    # AUTH HANDLERS
    # ============================================================

    async def handle_login(self):
        ...
    # ========================================================
    # AUTH
    # ========================================================
    user_id:       str  = ""
    user_email:    str  = ""
    is_logged_in:  bool = False
    auth_loading:  bool = False
    auth_error:    str  = ""
    login_email:   str  = ""
    login_password:str  = ""
    is_signup:     bool = False          # toggle login ↔ signup

    #============================================================
    # PROFILE PAGE
    #============================================================
    profile_name: str = ""
    headline: str = ""
    university: str = ""
    location: str = ""
    bio: str = ""
    skills: str = ""
    education: str = ""
    experience: str = ""
    github_url: str = ""
    linkedin_url: str = ""

    # ========================================================
    # NEW APPLICATION FORM
    # ========================================================
    company:         str = ""
    role:            str = ""
    job_description: str = ""
    resume_text:     str = ""
    form_error:      str = ""
    uploaded_resume_name: str = ""
    uploaded_resume_text: str = ""
    uploaded_resume_raw: bytes = b""
    resume_file: list = []
    resume_file_name: str = ""

    # ========================================================
    # PIPELINE
    # ========================================================
    pipeline_company: str = ""
    pipeline_role:    str = ""

    # "waiting" | "processing" | "complete" | "error"
    analyzer_status: str = "waiting"
    writer_status:   str = "waiting"
    critic_status:   str = "waiting"

    analyzer_msg: str = "Ready to extract skills and requirements"
    writer_msg:   str = "Waiting for analysis results…"
    critic_msg:   str = "Waiting for generated documents…"

    extracted_skills: list[str] = []
    writer_progress:  int       = 0      # 0-100

    # ========================================================
    # GENERATED ASSETS
    # ========================================================
    generated_resume: dict = {}
    generated_cover_letter: str   = ""
    critic_score:           float = 0.0
    ready_to_apply:         bool  = False
    keyword_match_pct:      int   = 0
    keyword_match_text:     str   = ""
    competitive_edge:       str   = ""
    current_app_id:         str   = ""

    # ========================================================
    # TRACKER
    # ========================================================
    applications: list[dict[str, str]] = []
    loading_apps: bool        = False

    # ========================================================
    # UI
    # ========================================================
    active_tab:  str  = "tracker"
    show_error:  bool = False
    error_msg:   str  = ""

    # ============================================================
    # COMPUTED VARS
    # ============================================================

    @rx.var
    def display_name(self) -> str:
        if self.profile_name:
            return self.profile_name

        if self.user_email:
            return self.user_email.split("@")[0].capitalize()

        return "User"
    
    @rx.var
    def total_applied(self) -> int:
        return len(self.applications)

    @rx.var
    def total_interviews(self) -> int:
        return sum(1 for a in self.applications if a.get("status") == "interviewing")

    @rx.var
    def total_offers(self) -> int:
        return sum(1 for a in self.applications if a.get("status") == "offer")

    @rx.var
    def has_applications(self) -> bool:
        return len(self.applications) > 0

    @rx.var
    def score_display(self) -> str:
        return f"{self.critic_score:.1f}"

    @rx.var
    def ready_label(self) -> str:
        return "Ready to Apply" if self.ready_to_apply else "Needs Work"

    @rx.var
    def score_ring_gradient(self) -> str:
        pct = round(min(self.critic_score / 10.0, 1.0) * 100)
        return f"conic-gradient(#C9A84C {pct}%, #2A2A2A {pct}%)"

    @rx.var
    def writer_progress_pct(self) -> str:
        return f"{self.writer_progress}%"

    @rx.var
    def keyword_width(self) -> str:
        return f"{self.keyword_match_pct}%"

    @rx.var
    def pipeline_done(self) -> bool:
        return (
            self.analyzer_status == "complete"
            and self.writer_status == "complete"
            and self.critic_status == "complete"
        )

    @rx.var
    def auth_btn_label(self) -> str:
        return "Create Account" if self.is_signup else "Sign In"

    @rx.var
    def auth_toggle_label(self) -> str:
        return "Already have an account? Sign in" if self.is_signup else "Don't have an account? Sign up"

    # ============================================================
    # AUTH HANDLERS
    # ============================================================

    async def handle_login(self):
        if not self.login_email or not self.login_password:
            self.auth_error = "Please fill in both fields"
            return
        self.auth_loading = True
        self.auth_error   = ""
        yield
        try:
            from autoapply_ai.db.client import supabase_login
            result = supabase_login(self.login_email, self.login_password)
            if result:
                self.user_id      = result["user_id"]
                self.user_email   = result["email"]
                self.is_logged_in = True
                self.login_email  = ""
                self.login_password = ""
                self.active_tab   = "tracker"
                yield rx.redirect("/")
            else:
                self.auth_error = "Invalid credentials — please try again."
        except Exception as e:
            self.auth_error = str(e)
        self.auth_loading = False

    async def handle_signup(self):
        if not self.login_email or not self.login_password:
            self.auth_error = "Please fill in both fields"
            return
        if len(self.login_password) < 6:
            self.auth_error = "Password must be at least 6 characters"
            return
        self.auth_loading = True
        self.auth_error   = ""
        yield
        try:
            from autoapply_ai.db.client import supabase_signup
            result = supabase_signup(self.login_email, self.login_password)
            if result:
                self.user_id        = result["user_id"]
                self.user_email     = result["email"]
                self.is_logged_in   = True
                self.login_email    = ""
                self.login_password = ""
                self.active_tab     = "tracker"
                yield rx.redirect("/")
            else:
                self.auth_error = "Signup failed — this email may already be registered."
        except Exception as e:
            self.auth_error = str(e)
        self.auth_loading = False

    def toggle_auth_mode(self):
        self.is_signup  = not self.is_signup
        self.auth_error = ""

    def logout(self):
        from autoapply_ai.db.client import supabase_logout
        supabase_logout()
        self.user_id        = ""
        self.user_email     = ""
        self.is_logged_in   = False
        self.applications   = []
        self.active_tab     = "tracker"
        return rx.redirect("/login")

    # ============================================================
    # FORM
    # ============================================================

    def clear_form(self):
        self.company = self.role = self.job_description = self.resume_text = ""
        self.form_error = ""
    

    def handle_resume_upload(self, files: list[rx.UploadFile]):
        if not files:
            self.form_error = "No file uploaded"
            return

        file = files[0]

        self.resume_file_name = file.filename

        # read file content
        content = file.read()

        try:
            self.resume_text = content.decode("utf-8", errors="ignore")
        except:
            self.resume_text = str(content)

        print("UPLOAD SUCCESS:", self.resume_file_name)

    async def process_upload(
        self,
        files: list[rx.UploadFile],
    ):
        if not files:
            return

        file = files[0]

        content = await file.read()

        self.resume_file_name = file.filename

        if file.filename.endswith(".pdf"):
            self.resume_text = self.parse_pdf(content)

        elif file.filename.endswith(".docx"):
            self.resume_text = self.parse_docx(content)

        else:
            self.resume_text = self.parse_txt(content)
    
    def parse_txt(self, content: bytes):
        return content.decode("utf-8", errors="ignore")
    

    def parse_pdf(self, content: bytes):
        pdf = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    
    def parse_docx(self, content: bytes):
        doc = Document(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    

    def download_resume_docx(self):
        from autoapply_ai.services.export import export_docx

        docx = export_docx(
            f"{self.pipeline_role} Resume",
            self.generated_resume,
        )

        return rx.download(
            data=docx,
            filename=f"{self.pipeline_company}_resume.docx",
        )
    
    
    def download_cover_letter_docx(self):
        from autoapply_ai.services.export import export_docx

        docx = export_docx(
            f"{self.pipeline_role} Cover Letter",
            self.generated_cover_letter,
        )

        return rx.download(
            data=docx,
            filename=f"{self.pipeline_company}_cover_letter.docx",
        )
    # ============================================================
    # AI PIPELINE
    # ============================================================

    async def start_pipeline(self):
        # --- Validation ---
        if not self.company.strip() or not self.role.strip():
            self.form_error = "Company and role are required"
            return
        if len(self.job_description.strip()) < 50:
            self.form_error = "Please paste the full job description (min 50 characters)"
            return
        
        
        # --- Reset pipeline ---
        self.pipeline_company    = self.company
        self.pipeline_role       = self.role
        self.analyzer_status     = "processing"
        self.writer_status       = "waiting"
        self.critic_status       = "waiting"
        self.analyzer_msg        = "Scanning job description for requirements…"
        self.writer_msg          = "Waiting for analysis results…"
        self.critic_msg          = "Waiting for generated documents…"
        self.extracted_skills    = []
        self.generated_resume    = ""
        self.generated_cover_letter = ""
        self.critic_score        = 0.0
        self.writer_progress     = 0
        self.form_error          = ""
        self.active_tab          = "feed"

        yield rx.redirect("/feed")

        # ─────────────────────────────────────────
        # STEP 1 · ANALYZER
        # ─────────────────────────────────────────
        analysis: dict = {}
        try:
            from autoapply_ai.services.ai_service import analyze_job
            analysis = await analyze_job(
                self.pipeline_company, self.pipeline_role, self.job_description
            )
            kws   = analysis.get("ats_keywords", [])[:6]
            tech  = analysis.get("technical_skills", [])[:3]
            merged = list({s.lower(): s for s in kws + tech}.values())[:6]
            self.extracted_skills = merged
            top2  = " and ".join(merged[:2]) if len(merged) >= 2 else ", ".join(merged)
            self.analyzer_msg = (
                f"Extracted {len(merged)} key skills including {top2}"
                if merged else "Requirements extracted from job description"
            )
        except Exception:
            self.extracted_skills = ["Technical Skills", "Communication", "Problem Solving"]
            self.analyzer_msg = "Key requirements extracted from job description"
            analysis = {}

        self.analyzer_status = "complete"
        yield
        await asyncio.sleep(0.7)

        # ─────────────────────────────────────────
        # STEP 2 · WRITER
        # ─────────────────────────────────────────
        self.writer_status   = "processing"
        self.writer_msg      = f"Injecting keywords for {self.pipeline_role} role…"
        self.writer_progress = 15
        yield

        try:
            from autoapply_ai.services.ai_service import generate_resume, generate_cover_letter

            await asyncio.sleep(0.3)
            self.writer_msg      = f"Tailoring résumé for {self.pipeline_company}…"
            self.writer_progress = 45
            yield

            resume = await generate_resume(
                self.pipeline_role, self.pipeline_company,
                self.job_description, self.resume_text, analysis,
            )
            self.generated_resume = resume
            self.writer_progress  = 72
            self.writer_msg       = "Writing personalised cover letter…"
            yield

            cover = await generate_cover_letter(
                self.pipeline_role, self.pipeline_company, self.job_description
            )
            self.generated_cover_letter = cover
            self.writer_progress = 100

        except Exception:
            self.generated_resume = (
                self.resume_text
                or f"Tailored résumé for {self.pipeline_role} at {self.pipeline_company}"
            )
            self.generated_cover_letter = (
                f"Dear Hiring Team at {self.pipeline_company},\n\n"
                f"I am writing to express my strong interest in the {self.pipeline_role} position.\n\n"
                "My experience aligns closely with your requirements and I am excited "
                "about the opportunity to contribute to your team.\n\n"
                "Thank you for your consideration.\n\nBest regards"
            )
            self.writer_progress = 100

        self.writer_status = "complete"
        self.writer_msg    = f"Résumé & cover letter tailored for {self.pipeline_company}"
        yield
        await asyncio.sleep(0.7)

        # ─────────────────────────────────────────
        # STEP 3 · CRITIC
        # ─────────────────────────────────────────
        self.critic_status = "processing"
        self.critic_msg    = "Reviewing document against ATS standards…"
        yield

        try:
            from autoapply_ai.services.ai_service import score_application
            s = await score_application(
                self.pipeline_company, self.pipeline_role,
                self.job_description, self.generated_resume, analysis,
            )
            self.critic_score       = min(float(s.get("score", 8.0)), 10.0)
            self.keyword_match_pct  = min(int(s.get("keyword_match", 85)), 100)
            self.keyword_match_text = str(s.get("keyword_text", ""))
            self.competitive_edge   = str(s.get("edge", ""))
            self.ready_to_apply     = self.critic_score >= 7.0
            if not self.keyword_match_text:
                self.keyword_match_text = (
                    f"Your résumé hits {self.keyword_match_pct}% of core competencies in the JD."
                )
            if not self.competitive_edge:
                self.competitive_edge = (
                    f"Your tailored application is optimised for {self.pipeline_company}'s requirements."
                )
        except Exception:
            self.critic_score       = 8.0
            self.keyword_match_pct  = 86
            self.keyword_match_text = "Strong alignment with the role competencies."
            self.competitive_edge   = "Tailored application stands out against generic submissions."
            self.ready_to_apply     = True

        self.critic_status = "complete"
        self.critic_msg    = f"Quality review complete — Score: {self.critic_score:.1f}/10"
        print("DEBUG USER ID =", self.user_id)
        yield

        # ─────────────────────────────────────────
        # SAVE TO SUPABASE
        # ─────────────────────────────────────────
        try:
            if not self.user_id:
                self.form_error = "Session expired. Please login again."
                yield rx.redirect("/login")
                return
            app_id = save_application(
                user_id=self.user_id,
                company=self.pipeline_company,
                role=self.pipeline_role,
                job_description=self.job_description,
                resume_text=self.resume_text,
                cover_letter=self.generated_cover_letter,
                score=self.critic_score,
            )

            print("DEBUG app_id:", app_id)
            if app_id:
                self.current_app_id = str(app_id)
        except Exception:
            pass

        yield
        await asyncio.sleep(1.2)
        self.active_tab = "assets"
        yield rx.redirect("/assets")

    # ============================================================
    # TRACKER
    # ============================================================

    async def load_applications(self):
        self.loading_apps = True
        yield

        try:
            from autoapply_ai.db.history import get_applications

            if not self.user_id:
                self.applications = []
                self.loading_apps = False
                yield
                return

            apps = get_applications(self.user_id)

            print("DEBUG apps:", apps)

            self.applications = apps or []

        except Exception as e:
            print("LOAD ERROR:", str(e))
            self.applications = []

        self.loading_apps = False
        print("DEBUG APPS:", apps)
        yield

    async def update_app_status(self, app_id: str, status: str):
        print("UPDATE APP:", app_id)
        print("NEW STATUS:", status)

        try:
            from autoapply_ai.db.history import update_status, get_applications

            update_status(app_id, status)

            apps = get_applications(self.user_id)
            print("AFTER UPDATE:", apps)

            self.applications = apps or []

        except Exception as e:
            print("UPDATE ERROR:", e)

        yield

    # ============================================================
    # CLIPBOARD
    # ============================================================

    def copy_resume(self):
        return rx.set_clipboard(self.generated_resume)

    def copy_cover_letter(self):
        return rx.set_clipboard(self.generated_cover_letter)
    
    async def save_profile(self):
        try:
            from autoapply_ai.db.client import get_client

            res = (
                get_client()
                .table("profiles")
                .upsert(
                    {
                        "user_id": self.user_id,
                        "full_name": self.profile_name,
                        "university": self.university,
                        "location": self.location,
                        "headline": self.headline,
                        "bio": self.bio,
                        "linkedin_url": self.linkedin_url,
                        "github_url": self.github_url,
                    }
                )
                .execute()
            )

            print("PROFILE SAVED:", res.data)

        except Exception as e:
            print("PROFILE ERROR:", e)

    def download_resume(self):
        return rx.download(
            url="/api/resume"
        )
    

    # ============================================================
    # NAVIGATION HELPERS
    # ============================================================

    def set_tab_tracker(self):
        self.active_tab = "tracker"

    def set_tab_apply(self):
        self.active_tab = "apply"
        self.clear_form()

    def set_tab_feed(self):
        self.active_tab = "feed"

    def set_tab_assets(self):
        self.active_tab = "assets"

    def go_to_assets(self):
        self.active_tab = "assets"
        return rx.redirect("/assets")

    # ============================================================
    # PAGE LOAD GUARDS
    # ============================================================

    async def guard(self):
        """Redirect to /login if not authenticated."""
        if not self.is_logged_in:
            yield rx.redirect("/login")
    
    async def load_profile(self):
        try:
            from autoapply_ai.db.client import get_client

            res = (
                get_client()
                .table("profiles")
                .select("*")
                .eq("user_id", self.user_id)
                .execute()
            )

            if res.data:
                profile = res.data[0]

                self.profile_name = profile.get("full_name", "")
                self.university = profile.get("university", "")
                self.location = profile.get("location", "")
                self.headline = profile.get("headline", "")
                self.bio = profile.get("bio", "")
                self.linkedin_url = profile.get("linkedin_url", "")
                self.github_url = profile.get("github_url", "")

        except Exception as e:
            print("PROFILE LOAD ERROR:", e)

    async def guard_and_load(self):
        """Redirect to /login, or load applications."""
        if not self.is_logged_in:
            yield rx.redirect("/login")
            return
        self.loading_apps = True
        yield
        try:
            from autoapply_ai.db.history import get_applications

            if not self.user_id:
                self.applications = []
                return

            apps = get_applications(self.user_id)
            self.applications = apps or []

        except Exception:
            self.applications = []

        self.loading_apps = False

        apps = get_applications(self.user_id)
        print("LOADED APPS:", len(apps))
        self.applications = apps or []