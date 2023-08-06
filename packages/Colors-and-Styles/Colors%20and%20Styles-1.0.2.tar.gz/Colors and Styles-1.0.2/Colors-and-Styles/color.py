class Color:

    class RGB:
        """As a string, an `RGB` value returns an ANSI color code.
`RGB` requires 4 arguments:

| Parameter      | Description                                                                                                       |
|----------------|-------------------------------------------------------------------------------------------------------------------|
| `red`          | The red value of the RGB.                                                                                         |
| `green`        | The green value of the RGB.                                                                                       |
| `blue`         | The blue value of the RGB.                                                                                        |
| `isForeground` | Returns a foreground ANSI color code as a string if `True`. Else returns a background ANSI color code. (Optional) |
"""

        def __init__(self,
                     red: int,
                     green: int,
                     blue: int,
                     isForeground: bool = True) -> None:
            self.red = red
            self.green = green
            self.blue = blue
            self.isForeground = isForeground

        def __str__(self) -> str:
            return f"\033[38;2;{self.red};{self.green};{self.blue}" if self.isForeground else f"\033[48;2;{self.red};{self.green};{self.blue}m"

    class Foreground:
        """`Foreground` has 8 class variables: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, and `RESET`. They are assigned to their respective ANSI color codes. To use these color codes, simply concatenate them with a string like so:

```python
print(f"{Color.Foreground.RED}This text is red.{Color.Foreground.RESET}")
```"""
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        RESET = "\033[39m"

    class Background:
        """`Background` has 9 class variables: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, and `RESET`. They are assigned to their respective ANSI color codes. To use these color codes, simply concatenate them with a string like so:

```python
print(f"{Color.Background.GREEN}This text is green.{Color.Background.RESET}")
```"""
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[103m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"
        RESET = "\033[49m"
