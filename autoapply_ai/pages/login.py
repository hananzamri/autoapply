"""autoapply/pages/login.py — Login & signup screen."""
import reflex as rx
from autoapply_ai.state import State
from autoapply_ai.styles import (
    BG, SURFACE, BORDER, GOLD, GOLD_LIGHT, GOLD_BG,
    WHITE, TEXT, TEXT_MUTED, TEXT_FAINT,
    ERROR, ERROR_BG, SUCCESS,
    INPUT_STYLE, BTN_GOLD,
)


def login() -> rx.Component:
    return rx.center(
        rx.vstack(
            # ── Brand mark ─────────────────────────────────────────
            rx.vstack(
                rx.box(
                    rx.text("A", font_size="26px", font_weight="800", color="#0A0A0A", line_height="1"),
                    width="56px", height="56px", border_radius="14px", background=GOLD,
                    display="flex", align_items="center", justify_content="center",
                    box_shadow=f"0 8px 28px {GOLD}35",
                ),
                rx.text("AutoApply", font_size="24px", font_weight="700", color=WHITE, letter_spacing="-0.03em"),
                rx.text(
                    rx.cond(State.is_signup, "Create your account to get started", "Welcome back — sign in to continue"),
                    font_size="14px", color=TEXT_MUTED,
                ),
                spacing="2", align="center", margin_bottom="28px",
            ),

            # ── Card ───────────────────────────────────────────────
            rx.box(
                # Error banner
                rx.cond(
                    State.auth_error != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("triangle_alert", size=15, color=ERROR),  # FIX: was "alert-triangle"
                            rx.text(State.auth_error, font_size="13px", color=ERROR),
                            spacing="2", align="center",
                        ),
                        background=ERROR_BG, border=f"1px solid {ERROR}40",
                        border_radius="8px", padding="10px 14px", margin_bottom="18px", width="100%",
                    ),
                    rx.box(),
                ),

                # Email
                rx.box(
                    rx.text("Email address", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="you@example.com", value=State.login_email, on_change=State.set_login_email, type="email", width="100%", style={**INPUT_STYLE, "height": "46px", "font_size": "14px"}),
                    margin_bottom="14px",
                ),

                # Password
                rx.box(
                    rx.text("Password", font_size="12px", font_weight="500", color=TEXT_MUTED, margin_bottom="6px"),
                    rx.input(placeholder="••••••••", value=State.login_password, on_change=State.set_login_password, type="password", width="100%", style={**INPUT_STYLE, "height": "46px", "font_size": "14px"}),
                    margin_bottom="22px",
                ),

                # Submit
                rx.button(
                    rx.cond(
                        State.auth_loading,
                        rx.hstack(rx.icon("loader", size=16, class_name="spin"), rx.text("Please wait…"), spacing="2", align="center"),
                        rx.hstack(rx.text(State.auth_btn_label), rx.icon("arrow_right", size=15), spacing="2", align="center"),  # FIX: was "arrow-right"
                    ),
                    on_click=rx.cond(State.is_signup, State.handle_signup, State.handle_login),
                    width="100%", height="46px", font_size="14px",
                    style=BTN_GOLD,
                    disabled=State.auth_loading,
                    cursor=rx.cond(State.auth_loading, "not-allowed", "pointer"),
                ),

                # Divider
                rx.box(
                    rx.hstack(
                        rx.box(height="1px", background=BORDER, flex="1"),
                        rx.text("or", font_size="12px", color=TEXT_FAINT, padding_x="12px"),
                        rx.box(height="1px", background=BORDER, flex="1"),
                        width="100%", align="center", margin_y="20px",
                    ),
                ),

                # Toggle login / signup
                rx.center(
                    rx.text(
                        State.auth_toggle_label,
                        font_size="13px", color=GOLD, cursor="pointer",
                        _hover={"color": GOLD_LIGHT, "text_decoration": "underline"},
                        on_click=State.toggle_auth_mode,
                    ),
                ),

                width="400px", padding="32px", background=SURFACE,
                border=f"1px solid {BORDER}", border_radius="18px",
                box_shadow="0 24px 64px rgba(0,0,0,0.6)",
            ),

            # Footer note
            rx.text("By continuing you agree to our Terms of Service.", font_size="11px", color=TEXT_FAINT, margin_top="20px"),

            spacing="0", align="center",
        ),
        background=BG, min_height="100vh", width="100%",
    )