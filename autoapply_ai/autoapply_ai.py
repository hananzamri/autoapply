"""autoapply/autoapply.py — App setup and page registration."""
from dotenv import load_dotenv
load_dotenv()

import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import BG, TEXT
from autoapply_ai.pages.login    import login
from autoapply_ai.pages.tracker  import tracker
from autoapply_ai.pages.new_apply import new_apply
from autoapply_ai.pages.live_feed import live_feed
from autoapply_ai.pages.assets   import assets
from autoapply_ai.pages.profile  import profile


# ── App instance ─────────────────────────────────────────────

app = rx.App(
    style={
        "font_family": "'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
        "background":  BG,
        "color":       TEXT,
        "-webkit-font-smoothing": "antialiased",
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
        "/custom.css",
    ],
)

# ── Pages ────────────────────────────────────────────────────

app.add_page(
    login,
    route="/login",
    title="AutoApply AI — Sign In",
)

app.add_page(
    tracker,
    route="/",
    title="AutoApply AI — Dashboard",
    on_load=State.guard_and_load,
)

app.add_page(
    new_apply,
    route="/apply",
    title="AutoApply AI — New Application",
    on_load=State.guard,
)

app.add_page(
    live_feed,
    route="/feed",
    title="AutoApply AI — Live Feed",
    on_load=State.guard,
)

app.add_page(
    assets,
    route="/assets",
    title="AutoApply AI — Assets",
    on_load=State.guard,
)
app.add_page(
    profile,
    route="/profile",
    title="My Profile",
    on_load=State.load_profile,
)