"""autoapply/components/layout.py — Base page layout with bottom nav."""
import reflex as rx
from autoapply_ai.styles import BG, MAX_W, PAGE_PAD, NAV_H
from autoapply_ai.components.bottom_nav import bottom_nav


def layout(*children) -> rx.Component:
    """Wrap any page content with the global shell + bottom nav."""
    return rx.box(
        # ── Scrollable content area ──────────────────────────────
        rx.box(
            *children,
            max_width=MAX_W,
            margin="0 auto",
            padding_x=PAGE_PAD,
            padding_top="32px",
            padding_bottom="100px",   # room above the nav
            min_height="100vh",
            width="100%",
            class_name="fade-in",
        ),
        # ── Fixed bottom nav ─────────────────────────────────────
        bottom_nav(),
        background=BG,
        min_height="100vh",
        width="100%",
        overflow_x="hidden",
    )
