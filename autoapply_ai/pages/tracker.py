"""autoapply/pages/tracker.py — Applications dashboard."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, SURFACE, SURFACE_2, BORDER, BORDER_2,
    GOLD, GOLD_BG, GOLD_LIGHT,
    WHITE, TEXT, TEXT_MUTED, TEXT_FAINT,
    SUCCESS, SUCCESS_BG, ERROR, ERROR_BG, BLUE, BLUE_BG,
    CARD, BTN_GOLD, BTN_OUTLINE, BTN_GHOST,
)
from autoapply_ai.components.layout import layout


# ── Stat card ────────────────────────────────────────────────

def stat_card(icon: str, value, label: str, sub: str, icon_color: str, sub_color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=17, color=icon_color),
                    background=f"{icon_color}18",
                    padding="9px",
                    border_radius="9px",
                ),
                rx.spacer(),
                rx.box(
                    rx.text(sub, font_size="11px", color=sub_color, font_weight="500"),
                    background=f"{sub_color}14",
                    padding="3px 10px",
                    border_radius="20px",
                ),
                width="100%", align="center",
            ),
            rx.text(
                value,
                font_size="38px", font_weight="700",
                color=WHITE, letter_spacing="-0.03em",
                line_height="1.1",
            ),
            rx.text(label, font_size="13px", color=TEXT_MUTED),
            spacing="2", align="start",
        ),
        **CARD,
        flex="1",
        min_width="0",
        cursor="default",
        transition="border-color 0.2s",
        _hover={"border_color": BORDER_2},
    )


# ── Status badge ─────────────────────────────────────────────

def status_badge(status) -> rx.Component:
    return rx.cond(
        status == "interviewing",
        rx.box(
            rx.text("Interviewing", font_size="10px", font_weight="600", color=BLUE),
            background=BLUE_BG, border=f"1px solid {BLUE}60",
            padding="3px 10px", border_radius="20px", white_space="nowrap",
        ),
        rx.cond(
            status == "offer",
            rx.box(
                rx.text("Offer ✓", font_size="10px", font_weight="600", color=SUCCESS),
                background=SUCCESS_BG, border=f"1px solid {SUCCESS}60",
                padding="3px 10px", border_radius="20px", white_space="nowrap",
            ),
            rx.cond(
                status == "rejected",
                rx.box(
                    rx.text("Rejected", font_size="10px", font_weight="600", color=ERROR),
                    background=ERROR_BG, border=f"1px solid {ERROR}60",
                    padding="3px 10px", border_radius="20px", white_space="nowrap",
                ),
                rx.box(
                    rx.text(
                        status, font_size="10px", font_weight="600",
                        color=TEXT_MUTED, text_transform="capitalize",
                    ),
                    background=SURFACE_2, border=f"1px solid {BORDER}",
                    padding="3px 10px", border_radius="20px", white_space="nowrap",
                ),
            ),
        ),
    )


# ── Application row ──────────────────────────────────────────
def app_row(item) -> rx.Component:
    return rx.box(
        rx.hstack(

            # Company Avatar
            rx.box(
                rx.text(
                    item["company"][0],
                    font_size="15px",
                    font_weight="700",
                    color=GOLD,
                ),
                width="44px",
                height="44px",
                border_radius="12px",
                background=GOLD_BG,
                border=f"1px solid {GOLD}30",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),

            # Company + Role
            rx.vstack(
                rx.text(
                    item["role"],
                    font_size="14px",
                    font_weight="600",
                    color=WHITE,
                ),

                rx.text(
                    item["company"],
                    font_size="12px",
                    color=TEXT_MUTED,
                ),

                rx.text(
                    item["time_ago"],
                    font_size="11px",
                    color=TEXT_FAINT,
                ),

                spacing="0",
                align="start",
                flex="1",
            ),

            rx.spacer(),

            # Right side controls
            rx.vstack(

                status_badge(item["status"]),

                rx.select(
                    [
                        "submitted",
                        "interviewing",
                        "offer",
                        "rejected",
                    ],
                    value=item["status"],
                    on_change=lambda status: State.update_app_status(
                        item["id"],
                        status,
                    ),
                    size="1",
                    width="130px",
                ),

                spacing="2",
                align="end",
            ),

            width="100%",
            align="center",
        ),

        padding="16px",
        border_bottom=f"1px solid {BORDER}",

        transition="all 0.15s ease",

        _hover={
            "background": SURFACE_2,
        },

        _last={
            "border_bottom": "none",
        },

        width="100%",
    )

# ── Empty state ──────────────────────────────────────────────

def empty_applications() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box(
                rx.icon("inbox", size=42, color=TEXT_FAINT),
                background=SURFACE_2,
                padding="20px",
                border_radius="50%",
            ),
            rx.text(
                "No applications yet",
                font_size="16px", font_weight="600", color=TEXT_MUTED,
            ),
            rx.text(
                "Click New Apply to start your first AI-powered application",
                font_size="13px", color=TEXT_FAINT, text_align="center",
                max_width="280px",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=16),
                    rx.text("New Application"),
                    spacing="2",
                    align="center",
                ),
                on_click=rx.redirect("/apply"),
                style=BTN_GOLD,
                padding="10px 22px",
                margin_top="4px",
            ),
            spacing="3", align="center",
        ),
        padding="52px 20px",
    )


# ── Page ─────────────────────────────────────────────────────

def tracker() -> rx.Component:
    return layout(
        # ── Header ───────────────────────────────────────────
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text("Hi, ", font_size="26px", font_weight="700", color=WHITE),
                    rx.link(
                        rx.text(State.display_name, font_size="26px", font_weight="700", color=GOLD),
                        href="/profile",
                    ),
                    rx.text("👋", font_size="22px"),
                    spacing="1", align="center",
                ),
                rx.text(
                    "Here's your application command centre",
                    font_size="14px", color=TEXT_MUTED,
                ),
                spacing="1", align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("log-out", size=15),
                    rx.text("Logout", font_size="13px"),
                    spacing="2", align="center",
                ),
                on_click=State.logout,
                style=BTN_GHOST,
                padding="9px 16px",
            ),
            width="100%",
            align="center",
            margin_bottom="28px",
        ),

        # ── Stat cards ───────────────────────────────────────
        rx.hstack(
            stat_card(
                "send",       State.total_applied,    "Applications Sent",
                "+2 this week", GOLD,    GOLD,
            ),
            stat_card(
                "calendar",   State.total_interviews, "Interviews",
                "In progress",  BLUE,    BLUE,
            ),
            stat_card(
                "award",      State.total_offers,     "Offers",
                "Pending reply", SUCCESS, SUCCESS,
            ),
            spacing="4",
            width="100%",
            margin_bottom="28px",
            wrap="wrap",
        ),

        # ── Recent applications ──────────────────────────────
        rx.box(
            # Section header
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Recent Applications",
                        font_size="16px", font_weight="600", color=WHITE,
                    ),
                    rx.text(
                        State.total_applied.to_string() + " total",
                        font_size="12px", color=TEXT_MUTED,
                    ),
                    spacing="0",
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=15),
                        rx.text("New", font_size="13px"),
                        spacing="1", align="center",
                    ),
                    on_click=rx.redirect("/apply"),
                    style=BTN_OUTLINE,
                    padding="8px 16px",
                ),
                width="100%",
                align="center",
                margin_bottom="0",
                padding="16px 16px 0 16px",
            ),

            # List
            rx.cond(
                State.loading_apps,
                rx.center(
                    rx.hstack(
                        rx.icon("loader", size=18, color=TEXT_MUTED, class_name="spin"),
                        rx.text("Loading…", color=TEXT_MUTED, font_size="13px"),
                        spacing="2", align="center",
                    ),
                    padding="48px",
                ),
                rx.cond(
                    State.has_applications,
                    rx.vstack(
                        rx.foreach(State.applications, app_row),
                        spacing="0",
                        width="100%",
                        padding_top="8px",
                    ),
                    empty_applications(),
                ),
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="14px",
            overflow="hidden",
        ),
    )
