"""autoapply/pages/profile.py — User profile editor."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, SURFACE, SURFACE_2, BORDER,
    GOLD, GOLD_BG, WHITE, TEXT_MUTED, TEXT_FAINT,
    CARD, INPUT_STYLE, BTN_GOLD, BTN_GHOST, SUCCESS,
)
from autoapply_ai.components.layout import layout


def profile() -> rx.Component:
    return rx.cond(
        State.is_logged_in,
        layout(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.box(rx.icon("user", size=18, color=GOLD), background=GOLD_BG, padding="10px", border_radius="10px"),
                    rx.vstack(
                        rx.text("My Profile", font_size="22px", font_weight="700", color=WHITE, letter_spacing="-0.02em"),
                        rx.text("Your personal details used to tailor applications", font_size="13px", color=TEXT_MUTED),
                        spacing="0", align="start",
                    ),
                    spacing="3", align="center",
                ),
                rx.box(height="1px", background=BORDER, width="100%"),

                # Form fields
                rx.box(
                    rx.text("Full Name", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="Your Name", value=State.profile_name, on_change=State.set_profile_name, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("Headline", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="e.g. Senior Product Designer · 5 yrs", value=State.headline, on_change=State.set_headline, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("Location", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="e.g. London, UK", value=State.location, on_change=State.set_location, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("About Me", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.text_area(placeholder="A short bio about yourself…", value=State.bio, on_change=State.set_bio, style={**INPUT_STYLE, "min_height": "100px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("Skills", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="e.g. Python, Figma, SQL, React", value=State.skills, on_change=State.set_skills, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("Education", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="e.g. BSc Computer Science, UCL 2022", value=State.education, on_change=State.set_education, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("Experience Summary", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="e.g. 4 years in product design at startups", value=State.experience, on_change=State.set_experience, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("GitHub URL", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="https://github.com/yourhandle", value=State.github_url, on_change=State.set_github_url, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="12px", width="100%",
                ),
                rx.box(
                    rx.text("LinkedIn URL", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="https://linkedin.com/in/yourhandle", value=State.linkedin_url, on_change=State.set_linkedin_url, style={**INPUT_STYLE, "height": "44px"}),
                    margin_bottom="20px", width="100%",
                ),

                # Save button
                rx.button(
                    rx.hstack(rx.icon("save", size=15), rx.text("Save Profile", font_size="14px"), spacing="2", align="center"),
                    on_click=State.save_profile,
                    style=BTN_GOLD, padding="11px 28px", width="100%",
                ),

                spacing="2", width="100%", align="start",
            ),
        ),
        rx.box(background=BG, min_height="100vh"),
    )