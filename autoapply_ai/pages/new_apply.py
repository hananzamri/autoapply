"""autoapply/pages/new_apply.py — New application intake form."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, SURFACE, SURFACE_2, SURFACE_3, BORDER, BORDER_2,
    GOLD, GOLD_BG, GOLD_BG2, GOLD_LIGHT, GOLD_DARK,
    WHITE, TEXT, TEXT_MUTED, TEXT_FAINT,
    SUCCESS, SUCCESS_BG, BLUE, BLUE_BG,
    CARD, INPUT_STYLE, BTN_GOLD, BTN_OUTLINE, BTN_GHOST,
    ERROR, ERROR_BG,
)
from autoapply_ai.components.layout import layout


# ── AI Insight card ──────────────────────────────────────────

def ai_insight_card() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("zap", size=16, color=GOLD),
                background=GOLD_BG,
                padding="8px",
                border_radius="9px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    "AI Insight",
                    font_size="13px", font_weight="600", color=WHITE,
                ),
                rx.text(
                    "AutoApply will extract keywords, skills, and cultural signals "
                    "from the JD and tailor your documents automatically.",
                    font_size="12px", color=TEXT_MUTED, line_height="1.6",
                ),
                spacing="1", align="start",
            ),
            spacing="3", align="start",
        ),
        background=GOLD_BG2,
        border=f"1px solid {GOLD}30",
        border_radius="12px",
        padding="14px",
        margin_top="4px",
    )


# ── Feature hint cards ───────────────────────────────────────

def hint_card(icon: str, title: str, desc: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(icon, size=18, color=color),
                background=f"{color}15",
                padding="10px",
                border_radius="10px",
            ),
            rx.text(title, font_size="13px", font_weight="600", color=WHITE),
            rx.text(desc, font_size="11px", color=TEXT_MUTED, line_height="1.5", text_align="center"),
            spacing="2", align="center",
        ),
        **CARD,
        flex="1",
        text_align="center",
        min_width="0",
    )


# ── Page ─────────────────────────────────────────────────────

def new_apply() -> rx.Component:
    return layout(
        # ── Header ───────────────────────────────────────────
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("sparkles", size=18, color=GOLD),
                    background=GOLD_BG,
                    padding="10px",
                    border_radius="10px",
                ),
                rx.vstack(
                    rx.text(
                        "New Application",
                        font_size="22px", font_weight="700",
                        color=WHITE, letter_spacing="-0.02em",
                    ),
                    rx.text(
                        "AI will extract keywords, tailor your résumé, and score your application",
                        font_size="13px", color=TEXT_MUTED,
                    ),
                    spacing="0", align="start",
                ),
                spacing="3", align="center",
            ),
            margin_bottom="24px",
            align="start",
        ),

        # ── Error banner ─────────────────────────────────────
        rx.cond(
            State.form_error != "",
            rx.box(
                rx.hstack(
                    rx.icon("alert-circle", size=15, color=ERROR),
                    rx.text(State.form_error, font_size="13px", color=ERROR),
                    spacing="2", align="center",
                ),
                background=ERROR_BG,
                border=f"1px solid {ERROR}40",
                border_radius="10px",
                padding="12px 16px",
                margin_bottom="16px",
                width="100%",
            ),
            rx.box(),
        ),

        # ── Two-column main grid ──────────────────────────────
        rx.grid(
            # LEFT: Core Details + Resume
            rx.box(
                rx.text(
                    "Core Details",
                    font_size="13px", font_weight="600",
                    color=TEXT_MUTED, letter_spacing="0.05em",
                    text_transform="uppercase", margin_bottom="14px",
                ),

                # Company
                rx.box(
                    rx.text("Company", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(
                        placeholder="e.g. Google, Stripe, Figma",
                        value=State.company,
                        on_change=State.set_company,
                        style={**INPUT_STYLE, "height": "44px"},
                    ),
                    margin_bottom="12px",
                ),

                # Role
                rx.box(
                    rx.text("Role", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(
                        placeholder="e.g. Senior Product Designer",
                        value=State.role,
                        on_change=State.set_role,
                        style={**INPUT_STYLE, "height": "44px"},
                    ),
                    margin_bottom="18px",
                ),

                # Divider
                rx.box(height="1px", background=BORDER, margin_bottom="18px"),

                # Resume
                rx.text(
                    "Your Résumé",
                    font_size="13px", font_weight="600",
                    color=TEXT_MUTED, letter_spacing="0.05em",
                    text_transform="uppercase", margin_bottom="6px",
                ),
                rx.text(
                    "Paste your existing résumé text for AI tailoring",
                    font_size="12px", color=TEXT_FAINT, margin_bottom="10px",
                ),
                rx.upload(
                    id="resume_upload",
                    accept={
                        "application/pdf": [".pdf"],
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
                    },
                    multiple=False,
                ),

                rx.button(
                    "Upload Resume",
                    on_click=State.process_upload(
                        rx.upload_files(upload_id="resume_upload")
                    ),
                ),
                rx.cond(
                    State.resume_file_name != "",
                    rx.text("Uploaded: " + State.resume_file_name, font_size="12px", color=TEXT_MUTED),
                ),

                ai_insight_card(),

                **CARD,
                height="100%",
            ),

            # RIGHT: Job Description
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Job Description",
                            font_size="13px", font_weight="600",
                            color=TEXT_MUTED, letter_spacing="0.05em",
                            text_transform="uppercase",
                        ),
                        rx.text(
                            "Paste the full JD for best results",
                            font_size="12px", color=TEXT_FAINT,
                        ),
                        spacing="0", align="start",
                    ),
                    rx.spacer(),
                    rx.box(
                        rx.text("Paste Text", font_size="11px", color=TEXT_MUTED, font_weight="500"),
                        background=SURFACE_2,
                        border=f"1px solid {BORDER}",
                        padding="4px 10px",
                        border_radius="6px",
                    ),
                    width="100%", align="center", margin_bottom="12px",
                ),

                rx.text_area(
                    placeholder=(
                        "Paste the job description here…\n\n"
                        "We're looking for a Senior Product Designer to…\n"
                        "Requirements:\n• 5+ years of product design experience\n"
                        "• Strong proficiency in Figma\n• Experience with design systems…"
                    ),
                    value=State.job_description,
                    on_change=State.set_job_description,
                    style={
                        **INPUT_STYLE,
                        "min_height": "340px",
                        "resize": "vertical",
                        "font_size": "13px",
                        "line_height": "1.7",
                    },
                    flex="1",
                    margin_bottom="16px",
                ),

                # Action row
                rx.hstack(
                    rx.hstack(
                        rx.icon("info", size=14, color=TEXT_FAINT),
                        rx.text(
                            "High-precision scan uses 3 AI agents",
                            font_size="12px", color=TEXT_FAINT,
                        ),
                        spacing="2", align="center",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.hstack(
                            rx.icon("sparkles", size=15),
                            rx.text("Start AI Scan", font_size="14px"),
                            rx.icon("arrow-right", size=14),
                            spacing="2", align="center",
                        ),
                        on_click=State.start_pipeline,
                        style=BTN_GOLD,
                        padding="11px 22px",
                        height="44px",
                        box_shadow=f"0 4px 20px {GOLD}35",
                    ),
                    width="100%", align="center",
                ),

                **CARD,
                display="flex",
                flex_direction="column",
                height="100%",
            ),

            columns="2",
            spacing="4",
            margin_bottom="20px",
            width="100%",
        ),

        # ── Feature cards row ─────────────────────────────────
        rx.hstack(
            hint_card(
                "cpu", "Skill Extraction",
                "Identifies 20+ technical and soft skills from the job description",
                GOLD,
            ),
            hint_card(
                "building-2", "Culture Analysis",
                "Maps company values and team dynamics to your application style",
                BLUE,
            ),
            hint_card(
                "target", "ATS Optimisation",
                "Injects exact keywords to pass automated applicant tracking systems",
                SUCCESS,
            ),
            spacing="4", width="100%", wrap="wrap",
        ),
    )
