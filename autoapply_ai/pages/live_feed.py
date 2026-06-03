"""autoapply/pages/live_feed.py — Real-time agent pipeline visualization."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, SURFACE, SURFACE_2, BORDER, BORDER_2,
    GOLD, GOLD_BG, GOLD_LIGHT,
    WHITE, TEXT, TEXT_MUTED, TEXT_FAINT,
    SUCCESS, SUCCESS_BG, ERROR, BLUE,
    CARD, BTN_GOLD, BTN_OUTLINE,
)
from autoapply_ai.components.layout import layout


def _agent_badge(status_var) -> rx.Component:
    return rx.cond(
        status_var == "complete",
        rx.box(rx.hstack(rx.icon("check", size=11, color=SUCCESS), rx.text("Complete", font_size="10px", font_weight="600", color=SUCCESS), spacing="1", align="center"), background=SUCCESS_BG, border=f"1px solid {SUCCESS}50", padding="3px 10px", border_radius="20px"),
        rx.cond(
            status_var == "processing",
            rx.box(rx.hstack(rx.box(width="6px", height="6px", border_radius="50%", background=GOLD, class_name="pulse-dot", flex_shrink="0"), rx.text("Processing", font_size="10px", font_weight="600", color=GOLD), spacing="1", align="center"), background=GOLD_BG, border=f"1px solid {GOLD}60", padding="3px 10px", border_radius="20px"),
            rx.box(rx.text("Waiting", font_size="10px", font_weight="600", color=TEXT_FAINT), background=SURFACE_2, border=f"1px solid {BORDER}", padding="3px 10px", border_radius="20px"),
        ),
    )


def _timeline_dot(status_var) -> rx.Component:
    return rx.box(
        rx.cond(
            status_var == "complete", rx.icon("check", size=13, color=SUCCESS),
            rx.cond(status_var == "processing", rx.icon("loader", size=13, color=GOLD, class_name="spin"), rx.icon("circle", size=10, color=TEXT_FAINT)),
        ),
        width="34px", height="34px", border_radius="50%",
        display="flex", align_items="center", justify_content="center",
        background=rx.cond(status_var == "complete", SUCCESS_BG, rx.cond(status_var == "processing", GOLD_BG, SURFACE_2)),
        border=rx.cond(status_var == "complete", f"2px solid {SUCCESS}", rx.cond(status_var == "processing", f"2px solid {GOLD}", f"2px solid {BORDER}")),
        flex_shrink="0", transition="all 0.3s ease",
    )


def _connector(status_var) -> rx.Component:
    return rx.box(width="2px", min_height="28px", background=rx.cond(status_var == "complete", SUCCESS, BORDER), margin_x="auto", transition="background 0.5s ease", flex="1")


def pipeline_card(icon, title, subtitle, status_var, msg_var, is_last=False, show_progress=False, progress_var=None) -> rx.Component:
    card_border = rx.cond(status_var == "processing", f"1px solid {GOLD}", rx.cond(status_var == "complete", f"1px solid {BORDER_2}", f"1px solid {BORDER}"))
    icon_color  = rx.cond(status_var == "complete", SUCCESS, rx.cond(status_var == "processing", GOLD, TEXT_FAINT))

    header = rx.hstack(
        rx.vstack(
            rx.hstack(rx.icon(icon, size=15, color=icon_color), rx.text(title, font_size="15px", font_weight="600", color=rx.cond(status_var == "waiting", TEXT_MUTED, WHITE)), spacing="2", align="center"),
            rx.text(subtitle, font_size="12px", color=TEXT_FAINT),
            spacing="0", align="start",
        ),
        rx.spacer(), _agent_badge(status_var), width="100%", align="center", margin_bottom="12px",
    )
    message_box = rx.box(rx.text(msg_var, font_size="12px", color=TEXT_MUTED, line_height="1.6"), background=BG, padding="10px 12px", border_radius="8px")

    if show_progress and progress_var is not None:
        progress_section = rx.cond(
            status_var != "waiting",
            rx.box(rx.box(rx.box(height="5px", background=rx.cond(status_var == "complete", SUCCESS, "transparent"), border_radius="3px", width=rx.cond(status_var == "complete", "100%", progress_var), class_name=rx.cond(status_var == "processing", "progress-shimmer", ""), transition="width 0.6s ease"), height="5px", background=BORDER, border_radius="3px", overflow="hidden"), margin_top="10px"),
            rx.box(),
        )
        inner = rx.box(header, message_box, progress_section, padding="16px", border_radius="13px", background=SURFACE, border=card_border, flex="1", transition="border-color 0.3s")
    else:
        inner = rx.box(header, message_box, padding="16px", border_radius="13px", background=SURFACE, border=card_border, flex="1", transition="border-color 0.3s")

    return rx.hstack(
        rx.vstack(_timeline_dot(status_var), _connector(status_var) if not is_last else rx.box(min_height="8px"), align="center", spacing="0", min_width="34px"),
        inner, align="start", spacing="3", width="100%", padding_bottom="0" if is_last else "4px",
    )


def skill_pill(skill) -> rx.Component:
    return rx.box(rx.text(skill, font_size="11px", font_weight="500", color=GOLD), background=GOLD_BG, border=f"1px solid {GOLD}30", padding="4px 12px", border_radius="20px", white_space="nowrap")


def live_feed() -> rx.Component:
    return rx.cond(
        State.is_logged_in,
        layout(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text("Agent Processing", font_size="22px", font_weight="700", color=WHITE, letter_spacing="-0.02em"),
                        rx.box(rx.hstack(rx.box(width="7px", height="7px", border_radius="50%", background=GOLD, class_name="pulse-dot"), rx.text("LIVE", font_size="10px", font_weight="700", color=GOLD), spacing="1", align="center"), background=GOLD_BG, border=f"1px solid {GOLD}50", padding="4px 10px", border_radius="20px", class_name="live-badge"),
                        spacing="3", align="center",
                    ),
                    rx.text(rx.cond(State.pipeline_company != "", "Building your application for " + State.pipeline_company + " — " + State.pipeline_role, "Start a new application to activate the pipeline"), font_size="13px", color=TEXT_MUTED),
                    spacing="1", align="start",
                ),
                rx.spacer(),
                rx.cond(
                    State.pipeline_done,
                    rx.button(rx.hstack(rx.icon("folder_open", size=15), rx.text("View Assets", font_size="13px"), spacing="2", align="center"), style=BTN_GOLD, padding="9px 18px", on_click=State.go_to_assets),  # FIX: folder-open
                    rx.box(),
                ),
                width="100%", align="center", margin_bottom="24px",
            ),
            rx.cond(
                State.analyzer_status == "complete",
                rx.box(rx.hstack(rx.icon("tag", size=13, color=TEXT_FAINT), rx.text("Extracted Skills:", font_size="12px", color=TEXT_FAINT, font_weight="500"), rx.foreach(State.extracted_skills, skill_pill), spacing="2", align="center", flex_wrap="wrap"), padding="12px 16px", background=SURFACE_2, border=f"1px solid {BORDER}", border_radius="10px", margin_bottom="20px"),
                rx.box(),
            ),
            rx.vstack(
                pipeline_card(icon="search", title="Analyzer", subtitle="Step 1 · Background Extraction", status_var=State.analyzer_status, msg_var=State.analyzer_msg),
                pipeline_card(icon="pen_tool", title="Writer", subtitle="Step 2 · Document Tailoring", status_var=State.writer_status, msg_var=State.writer_msg, show_progress=True, progress_var=State.writer_progress_pct),  # FIX: pen-tool
                pipeline_card(icon="square_check", title="Critic", subtitle="Step 3 · Quality Review", status_var=State.critic_status, msg_var=State.critic_msg, is_last=True),  # FIX: check-square
                spacing="0", width="100%",
            ),
            rx.cond(
                State.pipeline_done,
                rx.box(
                    rx.hstack(
                        rx.box(rx.icon("circle_check", size=22, color=SUCCESS), background=SUCCESS_BG, padding="10px", border_radius="10px"),  # FIX: check-circle
                        rx.vstack(rx.text("Pipeline complete!", font_size="15px", font_weight="600", color=WHITE), rx.text("Your résumé and cover letter are ready to download.", font_size="13px", color=TEXT_MUTED), spacing="0", align="start"),
                        rx.spacer(),
                        rx.link(rx.button(rx.hstack(rx.text("View Assets", font_size="14px"), rx.icon("arrow_right", size=15), spacing="2", align="center"), style=BTN_GOLD, padding="10px 22px"), href="/assets", on_click=State.set_tab_assets, text_decoration="none"),  # FIX: arrow-right
                        spacing="4", align="center", width="100%",
                    ),
                    background=SUCCESS_BG, border=f"1px solid {SUCCESS}40", border_radius="14px", padding="18px 20px", margin_top="20px", class_name="fade-in",
                ),
                rx.box(),
            ),
            rx.cond(
                State.pipeline_company == "",
                rx.box(
                    rx.vstack(
                        rx.box(rx.icon("activity", size=40, color=TEXT_FAINT), background=SURFACE_2, padding="20px", border_radius="50%"),
                        rx.text("No active pipeline", font_size="16px", font_weight="600", color=TEXT_MUTED),
                        rx.text("Go to New Apply and click Start AI Scan to run the pipeline.", font_size="13px", color=TEXT_FAINT, text_align="center", max_width="300px"),
                        rx.link(rx.button(rx.hstack(rx.icon("plus", size=15), rx.text("New Application"), spacing="2", align="center"), style=BTN_OUTLINE, padding="10px 22px"), href="/apply", on_click=State.set_tab_apply, text_decoration="none"),  # FIX: plus-circle
                        spacing="3", align="center",
                    ),
                    padding="60px 20px", text_align="center", background=SURFACE, border=f"1px solid {BORDER}", border_radius="14px", margin_top="20px",
                ),
                rx.box(),
            ),
        ),
        rx.box(background=BG, min_height="100vh"),
    )