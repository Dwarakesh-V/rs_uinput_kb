# rs_uinput_kb

A high-performance Python module written in Rust (via PyO3) for simulating hardware-level keystrokes on Linux. By interfacing directly with `/dev/uinput`, this library creates a virtual USB keyboard, making it virtually undetectable by software-level input hooks.

It features built-in humanization (randomized typing delays) and a powerful macro syntax for executing complex keystroke combinations, modifier holds, and special characters all from a single string.

## Features

* **Hardware-Level Emulation:** Bypasses X11/Wayland entirely. Types directly at the kernel level.
* **Humanized Typing:** Jittered delays between characters, randomized key-press dwell times, and varied shift-key hesitations.
* **Inline Macro Syntax:** Trigger special keys (`{enter}`, `{backspace}`) and modifier holds (`{ctrl down}c{ctrl up}`) directly within your text strings.
* **Blazing Fast:** Core logic written in safe Rust.

---

## Prerequisites

* **Linux OS** (Requires `/dev/uinput` support)
* **Python 3.7+**
* **Rust & Cargo** (for building)
* **Root/Sudo Access** (or configure `udev` rules so your user can write to `/dev/uinput`)

---

## Installation & Building

This project uses `maturin` to build the Rust code into a Python module.

1. Install `maturin` in your Python environment:
```bash
pip install maturin

```


2. Build and install the module directly into your current virtual environment:
```bash
maturin develop --release

```

---

## Usage Guide

**Important:** Because this script accesses `/dev/uinput`, you will likely need to run your Python script with `sudo` (e.g., `sudo python main.py`), unless you have set up specific user permissions for `uinput`.

### Basic Humanized Typing

By default, the function adds slight, randomized delays to mimic a real human typing.

```python
import rs_uinput_kb

# Types a simple string with natural human-like delays
rs_uinput_kb.type_text("Hello, world! I am typing like a human.")

```

### Instant / Machine-Speed Typing

If you want the text to appear instantaneously, set all delay parameters to `0`.

```python
import rs_uinput_kb

rs_uinput_kb.type_text(
    "This will appear instantly.",
    min_char_delay=0.0,
    max_char_delay=0.0,
    min_dwell_time=0,
    max_dwell_time=0,
    min_shift_delay=0,
    max_shift_delay=0,
    startup_delay_ms=200 # Only wait 200ms for OS recognition
)

```

### Advanced: Macros & Special Keys

The module supports an inline macro syntax using curly braces `{}`. This allows you to mix normal typing with special commands seamlessly.

```python
import rs_uinput_kb

# 1. Tapping Special Keys
# Types "User", presses Tab, types "Password", presses Enter
rs_uinput_kb.type_text("User{tab}Password{enter}")

# 2. Deleting Text
# Types a typo, then uses backspace to correct it
rs_uinput_kb.type_text("The wrong word{backspace}{backspace}{backspace}{backspace}right word.")

# 3. Holding Modifiers (e.g., Copy and Paste)
# Highlights all text, copies it, moves right, and pastes it
rs_uinput_kb.type_text("{ctrl down}a{ctrl up}{ctrl down}c{ctrl up}{right}{ctrl down}v{ctrl up}")

# 4. Escaping Brackets
# If you need to actually type a curly bracket, use double brackets
rs_uinput_kb.type_text("def my_function() {{ return True; }}")

```

**Supported Special Keys:**
`backspace`, `enter`, `tab`, `esc`, `space`, `up`, `down`, `left`, `right`, `shift`, `ctrl`, `alt`, `meta` (or `win`, `cmd`), `insert`, `delete`, `home`, `end`, `pageup`, `pagedown`, `capslock`, `f1` through `f12`.

---

## API Reference

### `rs_uinput_kb.type_text(text, kwargs)`

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `text` | `str` | **Required** | The string of characters and `{macros}` to type. |
| `min_char_delay` | `float` | `0.05` | Minimum wait time (in seconds) between pressing subsequent keys. |
| `max_char_delay` | `float` | `0.1` | Maximum wait time (in seconds) between pressing subsequent keys. |
| `min_dwell_time` | `int` | `20` | Minimum time (in milliseconds) a key is physically held down before release. |
| `max_dwell_time` | `int` | `60` | Maximum time (in milliseconds) a key is physically held down before release. |
| `min_shift_delay` | `int` | `10` | Minimum hesitation (in ms) before and after pressing the shift key for capital letters. |
| `max_shift_delay` | `int` | `30` | Maximum hesitation (in ms) before and after pressing the shift key for capital letters. |
| `startup_delay_ms` | `int` | `500` | Time (in ms) the script waits after creating the virtual `/dev/uinput` device before it starts typing. *Note: If this is too low, the OS might miss the first few keystrokes.* |

---

## Troubleshooting

* **`RuntimeError: Permission denied (os error 13)`**
Your user does not have permission to read/write `/dev/uinput`. Run your Python script with `sudo` or add a `udev` rule for the `uinput` group.
* **The first few characters are missing**
The Linux kernel takes a fraction of a second to recognize a newly plugged-in (or virtual) USB device. Increase the `startup_delay_ms` (e.g., to `800` or `1000`).