"""
Shared plotting/theme defaults.
"""
from pathlib import Path

FIG_WIDTH = 14
FIG_HEIGHT = 8
DPI = 300

TITLE_SIZE = 26
SUBTITLE_SIZE = 15
BODY_SIZE = 11

COLORS = {
    "navy": "#143A5E",
    "blue": "#2A6F97",
    "green": "#3A9D5D",
    "gold": "#E3B341",
    "orange": "#D98C2B",
    "gray": "#666666",
    "light_gray": "#F4F6F8",
    "background": "#FFFFFF",
}

RESULTS_DIR = Path("results")
FIGURES_DIR = RESULTS_DIR / "figures"

def ensure_results():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    return FIGURES_DIR
