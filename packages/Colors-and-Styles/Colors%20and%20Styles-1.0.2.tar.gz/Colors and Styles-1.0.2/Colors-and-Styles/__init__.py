from .color import Color
from .style import Style

RESET_ALL = "\033[0m"


def clear():
    """Clears the terminal."""
    print("\033c", end="", flush=True)
