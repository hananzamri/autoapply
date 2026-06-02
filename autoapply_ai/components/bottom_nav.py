"""autoapply/components/bottom_nav.py — Fixed bottom navigation bar."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, BORDER, GOLD, GOLD_LIGHT, TEXT_MUTED, MAX_W, NAV_H, PAGE_PAD
)


def _tab(icon: str, label: str, tab: str, route: str, on_click) -> rx.Component:
    """Single nav tab with gold active indicator."""
    active = State.active_tab == tab
    return rx.link(
        rx.vstack(
            # Active bar at top
            rx.box(
                width="28px",
                height="2px",
                background=rx.cond(active, GOLD, "transparent"),
                border_radius="0 0 3px 3px",
                transition="background 0.25s",
            ),
            # Icon
            rx.icon(
                icon,
                size=21,
                color=rx.cond(active, GOLD, TEXT_MUTED),
            ),
            # Label
            rx.text(
                label,
                font_size="11px",
                font_weight=rx.cond(active, "600", "400"),
                color=rx.cond(active, GOLD, TEXT_MUTED),
                letter_spacing="-0.01em",
            ),
            spacing="1",
            align="center",
            padding_top="4px",
            padding_bottom="6px",
        ),
        href=route,
        on_click=on_click,
        text_decoration="none",
        flex="1",
        display="flex",
        justify_content="center",
        align_items="center",
        cursor="pointer",
        transition="opacity 0.2s",
        _hover={"opacity": "0.75"},
    )


def bottom_nav() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                _tab("bar-chart-2", "Tracker",  "tracker", "/",       State.set_tab_tracker),
                _tab("plus-circle", "New Apply", "apply",   "/apply",  State.set_tab_apply),
                _tab("activity",    "Live Feed", "feed",    "/feed",   State.set_tab_feed),
                _tab("folder-open", "Assets",    "assets",  "/assets", State.set_tab_assets),
                width="100%",
                spacing="0",
            ),
            max_width=MAX_W,
            margin="0 auto",
            width="100%",
        ),
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        height=NAV_H,
        background=BG,
        border_top=f"1px solid {BORDER}",
        z_index="200",
        display="flex",
        align_items="center",
        padding_x=PAGE_PAD,
        backdrop_filter="blur(12px)",
    )
