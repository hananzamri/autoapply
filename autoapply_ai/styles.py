# ============================================================
# AutoApply AI — Soft Light Theme
# Clean, professional, ATS-friendly
# ============================================================

# ---- Core Background ----
BG         = "#F6F7F9"
SURFACE    = "#FFFFFF"
SURFACE_2  = "#FAFBFC"
SURFACE_3  = "#F1F3F5"

# ---- Borders ----
BORDER     = "#E4E7EB"
BORDER_2   = "#D6DAE0"

# ---- Accent ----
GOLD       = "#B88A2A"
GOLD_LIGHT = "#D8AE53"
GOLD_DARK  = "#8C661A"

GOLD_BG    = "#FFF8E8"
GOLD_BG2   = "#F9F1D8"

# ---- Text ----
WHITE      = "#383838"

TEXT       = "#1F2937"
TEXT_MUTED = "#6B7280"
TEXT_FAINT = "#9CA3AF"

# ---- Semantic ----
SUCCESS    = "#2E8B57"
SUCCESS_BG = "#EEF8F2"

ERROR      = "#D14343"
ERROR_BG   = "#FFF1F1"

BLUE       = "#3B82F6"
BLUE_BG    = "#EFF6FF"

# ---- Layout ----
NAV_H      = "72px"
PAGE_PAD   = "32px"
MAX_W      = "1200px"

# ============================================================
# CARDS
# ============================================================

CARD = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "border_radius": "16px",
    "padding": "24px",
    "box_shadow": "0 1px 3px rgba(0,0,0,0.04)",
}

CARD_HOVER = {
    **CARD,
    "transition": "all 0.2s ease",
    "_hover": {
        "border_color": GOLD,
        "box_shadow": "0 6px 16px rgba(0,0,0,0.08)",
    },
}

# ============================================================
# INPUTS
# ============================================================

INPUT_STYLE = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "border_radius": "12px",
    "color": TEXT,
    "padding": "12px 14px",
    "width": "100%",
    "font_size": "15px",
    "_placeholder": {
        "color": TEXT_FAINT,
    },
    "_focus": {
        "border_color": GOLD,
        "outline": "none",
        "box_shadow": "0 0 0 3px rgba(184,138,42,0.15)",
    },
}

# ============================================================
# PRIMARY BUTTON
# ============================================================

BTN_GOLD = {
    "background": GOLD,
    "color": WHITE,
    "border": "none",
    "border_radius": "12px",
    "font_weight": "600",
    "padding": "10px 18px",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "_hover": {
        "background": GOLD_LIGHT,
    },
    "_active": {
        "transform": "scale(0.98)",
    },
}

# ============================================================
# OUTLINE BUTTON
# ============================================================

BTN_OUTLINE = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "color": TEXT,
    "border_radius": "12px",
    "font_weight": "500",
    "padding": "10px 18px",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "_hover": {
        "border_color": GOLD,
        "color": GOLD_DARK,
    },
}

# ============================================================
# GHOST BUTTON
# ============================================================

BTN_GHOST = {
    "background": "transparent",
    "color": TEXT_MUTED,
    "border_radius": "10px",
    "padding": "8px 12px",
    "cursor": "pointer",
    "_hover": {
        "background": SURFACE_3,
        "color": TEXT,
    },
}