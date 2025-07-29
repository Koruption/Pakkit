ANSI_SEQUENCES = {
    # Cursor Movement
    "cursor_up": "\x1b[A",
    "cursor_down": "\x1b[B",
    "cursor_right": "\x1b[C",
    "cursor_left": "\x1b[D",
    "cursor_move_home": "\x1b[H",
    "cursor_move_to": lambda row, col: f"\x1b[{row};{col}H",

    # Cursor Save/Restore
    "cursor_save_position": "\x1b[s",
    "cursor_restore_position": "\x1b[u",

    # Screen Erase
    "clear_screen": "\x1b[2J",
    "clear_line": "\x1b[2K",
    "clear_line_right": "\x1b[K",
    "clear_line_left": "\x1b[1K",

    # Text Styles
    "style_reset": "\x1b[0m",
    "style_bold": "\x1b[1m",
    "style_italic": "\x1b[3m",
    "style_underline": "\x1b[4m",
    "style_inverse": "\x1b[7m",

    # Foreground Colors
    "fg_black": "\x1b[30m",
    "fg_red": "\x1b[31m",
    "fg_green": "\x1b[32m",
    "fg_yellow": "\x1b[33m",
    "fg_blue": "\x1b[34m",
    "fg_magenta": "\x1b[35m",
    "fg_cyan": "\x1b[36m",
    "fg_white": "\x1b[37m",
    "fg_bright_black": "\x1b[90m",
    "fg_bright_red": "\x1b[91m",
    "fg_bright_green": "\x1b[92m",
    "fg_bright_yellow": "\x1b[93m",
    "fg_bright_blue": "\x1b[94m",
    "fg_bright_magenta": "\x1b[95m",
    "fg_bright_cyan": "\x1b[96m",
    "fg_bright_white": "\x1b[97m",
    "fg_256": lambda n: f"\x1b[38;5;{n}m",
    "fg_truecolor": lambda r, g, b: f"\x1b[38;2;{r};{g};{b}m",

    # Background Colors
    "bg_black": "\x1b[40m",
    "bg_red": "\x1b[41m",
    "bg_green": "\x1b[42m",
    "bg_yellow": "\x1b[43m",
    "bg_blue": "\x1b[44m",
    "bg_magenta": "\x1b[45m",
    "bg_cyan": "\x1b[46m",
    "bg_white": "\x1b[47m",
    "bg_bright_black": "\x1b[100m",
    "bg_bright_red": "\x1b[101m",
    "bg_bright_green": "\x1b[102m",
    "bg_bright_yellow": "\x1b[103m",
    "bg_bright_blue": "\x1b[104m",
    "bg_bright_magenta": "\x1b[105m",
    "bg_bright_cyan": "\x1b[106m",
    "bg_bright_white": "\x1b[107m",
    "bg_256": lambda n: f"\x1b[48;5;{n}m",
    "bg_truecolor": lambda r, g, b: f"\x1b[48;2;{r};{g};{b}m",

    # Input Sequences
    "key_arrow_up": "\x1b[A",
    "key_arrow_down": "\x1b[B",
    "key_arrow_right": "\x1b[C",
    "key_arrow_left": "\x1b[D",
    "key_insert": "\x1b[2~",
    "key_delete": "\x1b[3~",
    "key_home": "\x1b[H",   # or \x1b[1~
    "key_end": "\x1b[F",    # or \x1b[4~
    "key_page_up": "\x1b[5~",
    "key_page_down": "\x1b[6~",
    "key_f1": "\x1bOP",
    "key_f2": "\x1bOQ",
    "key_f3": "\x1bOR",
    "key_f4": "\x1bOS",

    # Query
    "query_cursor_position": "\x1b[6n",

    # OSC
    "osc_set_title": lambda title: f"\x1b]0;{title}\x07",

    # Mouse Tracking
    "mouse_enable_basic": "\x1b[?1000h",
    "mouse_disable_basic": "\x1b[?1000l",
}
