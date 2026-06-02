"""autoapply/pages/assets.py — Generated résumé, cover letter, and AI insights."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, SURFACE, SURFACE_2, BORDER, BORDER_2,
    GOLD, GOLD_BG, GOLD_LIGHT, GOLD_DARK,
    WHITE, TEXT, TEXT_MUTED, TEXT_FAINT,
    SUCCESS, SUCCESS_BG, ERROR, ERROR_BG, BLUE, BLUE_BG,
    CARD, BTN_GOLD, BTN_OUTLINE, BTN_GHOST,
)
from autoapply_ai.components.layout import layout


# ── Score ring (conic-gradient) ───────────────────────────────

def score_ring() -> rx.Component:
    return rx.box(
        # Inner circle
        rx.box(
            rx.vstack(
                rx.text(
                    State.score_display,
                    font_size="30px", font_weight="800",
                    color=WHITE, letter_spacing="-0.03em",
                    line_height="1",
                ),
                rx.text("/ 10", font_size="13px", color=TEXT_MUTED, font_weight="500"),
                spacing="0", align="center",
            ),
            width="96px", height="96px",
            border_radius="50%",
            background=BG,
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        width="116px", height="116px",
        border_radius="50%",
        style={"background": State.score_ring_gradient},
        display="flex",
        align_items="center",
        justify_content="center",
        padding="10px",
        transition="background 1s ease",
    )


# ── Ready badge ───────────────────────────────────────────────

def ready_badge() -> rx.Component:
    return rx.cond(
        State.ready_to_apply,
        rx.box(
            rx.hstack(
                rx.icon("circle_circle", size=13, color=SUCCESS),
                rx.text(State.ready_label, font_size="12px", font_weight="600", color=SUCCESS),
                spacing="1", align="center",
            ),
            background=SUCCESS_BG, border=f"1px solid {SUCCESS}50",
            padding="5px 14px", border_radius="20px",
        ),
        rx.box(
            rx.hstack(
                rx.icon("circle_alert", size=13, color=GOLD),
                rx.text(State.ready_label, font_size="12px", font_weight="600", color=GOLD),
                spacing="1", align="center",
            ),
            background=GOLD_BG, border=f"1px solid {GOLD}50",
            padding="5px 14px", border_radius="20px",
        ),
    )


# ── Document card ─────────────────────────────────────────────

def resume_card() -> rx.Component:
    return rx.box(
        # Icon + label
        rx.hstack(
            rx.box(
                rx.icon("file_text", size=20, color=GOLD),
                background=GOLD_BG, padding="10px", border_radius="10px",
            ),
            rx.vstack(
                rx.text("Tailored Résumé", font_size="14px", font_weight="600", color=WHITE),
                rx.text("Text · AI-generated", font_size="11px", color=TEXT_MUTED),
                spacing="0", align="start",
            ),
            spacing="3", align="center", margin_bottom="12px",
        ),
        # Divider
        rx.box(height="1px", background=BORDER, margin_bottom="12px"),
        # Preview
        rx.cond(
            State.generated_resume != "",
            rx.box(
                rx.text(
                    State.generated_resume,
                    font_size="11px", color=TEXT_MUTED,
                    line_height="1.6",
                    overflow="hidden",
                    max_height="80px",
                    style={"display": "-webkit-box", "-webkit-line-clamp": "4",
                           "-webkit-box-orient": "vertical"},
                ),
                background=BG, padding="10px 12px",
                border_radius="8px", margin_bottom="12px",
            ),
            rx.box(
                rx.text("Run the AI pipeline to generate your résumé.", font_size="12px", color=TEXT_FAINT),
                background=SURFACE_2, padding="10px 12px",
                border_radius="8px", margin_bottom="12px",
            ),
        ),
        # Buttons
        rx.hstack(
            rx.button(
                rx.hstack(rx.icon("eye", size=14), rx.text("Preview"), spacing="1", align="center"),
                on_click=lambda: rx.window_alert(State.generated_resume),
                style=BTN_OUTLINE, padding="8px 14px", font_size="12px",
                disabled=State.generated_resume == "",
            ),
            rx.button(
                rx.hstack(rx.icon("copy", size=14), rx.text("Copy"), spacing="1", align="center"),
                on_click=rx.set_clipboard(State.generated_resume),
                style=BTN_GHOST, padding="8px 14px", font_size="12px",
                disabled=State.generated_resume == "",
            ),

            rx.button(
                "Download DOCX",
                on_click=State.download_resume_docx,
            ),
            spacing="2",
        ),
        **CARD,
        flex="1", min_width="0",
    )


def cover_letter_card() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("mail", size=20, color=BLUE),
                background=BLUE_BG, padding="10px", border_radius="10px",
            ),
            rx.vstack(
                rx.text("Cover Letter", font_size="14px", font_weight="600", color=WHITE),
                rx.text("Text · AI-generated", font_size="11px", color=TEXT_MUTED),
                spacing="0", align="start",
            ),
            spacing="3", align="center", margin_bottom="12px",
        ),
        rx.box(height="1px", background=BORDER, margin_bottom="12px"),
        rx.cond(
            State.generated_cover_letter != "",
            rx.box(
                rx.text(
                    State.generated_cover_letter,
                    font_size="11px", color=TEXT_MUTED,
                    line_height="1.6",
                    overflow="hidden",
                    max_height="80px",
                    style={"display": "-webkit-box", "-webkit-line-clamp": "4",
                           "-webkit-box-orient": "vertical"},
                ),
                background=BG, padding="10px 12px",
                border_radius="8px", margin_bottom="12px",
            ),
            rx.box(
                rx.text("Run the AI pipeline to generate your cover letter.", font_size="12px", color=TEXT_FAINT),
                background=SURFACE_2, padding="10px 12px",
                border_radius="8px", margin_bottom="12px",
            ),
        ),
        rx.hstack(
            rx.button(
                rx.hstack(rx.icon("eye", size=14), rx.text("Preview"), spacing="1", align="center"),
                on_click=lambda: rx.window_alert(State.generated_cover_letter),
                style=BTN_OUTLINE, padding="8px 14px", font_size="12px",
                disabled=State.generated_cover_letter == "",
            ),
            rx.button(
                rx.hstack(rx.icon("copy", size=14), rx.text("Copy"), spacing="1", align="center"),
                on_click=rx.set_clipboard(State.generated_cover_letter),
                style=BTN_GHOST, padding="8px 14px", font_size="12px",
                disabled=State.generated_cover_letter == "",
            ),
            rx.button(
                "Download DOCX",
                on_click=State.download_cover_letter_docx,
            ),
            spacing="2",
        ),
        **CARD,
        flex="1", min_width="0",
    )



# ── AI Insights ───────────────────────────────────────────────

def keyword_match_card() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("chart_column", size=16, color=GOLD),
                background=GOLD_BG, padding="8px", border_radius="8px",
            ),
            rx.text("Keyword Match", font_size="14px", font_weight="600", color=WHITE),
            spacing="2", align="center", margin_bottom="14px",
        ),
        # Percentage + bar
        rx.hstack(
            rx.text("Coverage", font_size="12px", color=TEXT_MUTED),
            rx.spacer(),
            rx.text(State.keyword_width, font_size="14px", font_weight="700", color=GOLD),
            width="100%", margin_bottom="8px",
        ),
        rx.box(
            rx.box(
                height="6px",
                background=f"linear-gradient(90deg, {GOLD_DARK}, {GOLD}, {GOLD_LIGHT})",
                border_radius="3px",
                width=State.keyword_width,
                transition="width 1.2s ease",
            ),
            height="6px",
            background=BORDER,
            border_radius="3px",
            overflow="hidden",
            margin_bottom="12px",
        ),
        rx.text(
            State.keyword_match_text,
            font_size="12px", color=TEXT_MUTED, line_height="1.6",
        ),
        **CARD,
        flex="1", min_width="0",
    )


def competitive_edge_card() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("zap", size=16, color=GOLD),
                background=GOLD_BG, padding="8px", border_radius="8px",
            ),
            rx.text("Competitive Edge", font_size="14px", font_weight="600", color=WHITE),
            spacing="2", align="center", margin_bottom="14px",
        ),
        rx.text(
            State.competitive_edge,
            font_size="13px", color=TEXT_MUTED, line_height="1.7",
        ),
        **CARD,
        flex="1", min_width="0",
    )


# ── Page ─────────────────────────────────────────────────────

def assets() -> rx.Component:
    return layout(
        # ── Header ───────────────────────────────────────────
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Generated Assets",
                    font_size="22px", font_weight="700",
                    color=WHITE, letter_spacing="-0.02em",
                ),
                rx.text(
                    rx.cond(
                        State.pipeline_company != "",
                        "Application for " + State.pipeline_role + " at " + State.pipeline_company,
                        "Run the AI pipeline to generate your assets",
                    ),
                    font_size="13px", color=TEXT_MUTED,
                ),
                spacing="0", align="start",
            ),
            rx.spacer(),
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon("circle_plus", size=15),
                        rx.text("New Application", font_size="13px"),
                        spacing="2", align="center",
                    ),
                    style=BTN_OUTLINE,
                    padding="9px 18px",
                ),
                href="/apply",
                on_click=State.set_tab_apply,
                text_decoration="none",
            ),
            width="100%", align="center", margin_bottom="24px",
        ),

        # ── Score + CTA banner ───────────────────────────────
        rx.cond(
            State.pipeline_done,
            rx.box(
                rx.hstack(
                    # Score ring
                    score_ring(),
                    # Score info
                    rx.vstack(
                        ready_badge(),
                        rx.text(
                            "Quality Score",
                            font_size="22px", font_weight="700",
                            color=WHITE, letter_spacing="-0.02em",
                        ),
                        rx.text(
                            "Your application scored " + State.score_display + "/10 "
                            "— optimised for ATS and human review",
                            font_size="13px", color=TEXT_MUTED, line_height="1.6",
                            max_width="340px",
                        ),
                        spacing="2", align="start",
                    ),
                    rx.spacer(),
                    spacing="5", align="center", width="100%",
                    wrap="wrap",
                ),
                **{
                    **CARD,
                    "background": f"linear-gradient(135deg, {GOLD_BG} 0%, {SURFACE} 100%)",
                    "border": f"1px solid {GOLD}30",
                },
                margin_bottom="24px",
            ),
            # Not complete yet
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.icon("loader", size=22, color=GOLD, class_name="spin"),
                        background=GOLD_BG, padding="12px", border_radius="50%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Waiting for pipeline…",
                            font_size="16px", font_weight="600", color=TEXT_MUTED,
                        ),
                        rx.text(
                            "Your assets will appear here once the AI pipeline completes.",
                            font_size="13px", color=TEXT_FAINT,
                        ),
                        spacing="0", align="start",
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("activity", size=15),
                                rx.text("View Pipeline"),
                                spacing="2", align="center",
                            ),
                            style=BTN_OUTLINE, padding="9px 18px",
                        ),
                        href="/feed",
                        on_click=State.set_tab_feed,
                        text_decoration="none",
                    ),
                    spacing="4", align="center", width="100%",
                ),
                **{
                    **CARD,
                },
                margin_bottom="24px",
            ),
        ),

        # ── Document cards ───────────────────────────────────
        rx.text(
            "Generated Documents",
            font_size="13px", font_weight="600",
            color=TEXT_MUTED, letter_spacing="0.05em",
            text_transform="uppercase", margin_bottom="12px",
        ),
        rx.hstack(
            resume_card(),
            cover_letter_card(),
            spacing="4", width="100%", wrap="wrap",
            margin_bottom="24px",
        ),

        # ── AI Insights ───────────────────────────────────────
        rx.cond(
            State.pipeline_done,
            rx.vstack(
                rx.text(
                    "AI Insights",
                    font_size="13px", font_weight="600",
                    color=TEXT_MUTED, letter_spacing="0.05em",
                    text_transform="uppercase", margin_bottom="12px",
                ),
                rx.hstack(
                    keyword_match_card(),
                    competitive_edge_card(),
                    spacing="4", width="100%", wrap="wrap",
                ),
                width="100%", spacing="0",
            ),
            rx.box(),
        ),
    )
