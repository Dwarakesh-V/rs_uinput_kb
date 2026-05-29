# rs_uinput

`rs_uinput` is a Python library backed by Rust that types text through Linux's `uinput` subsystem.

Instead of injecting keystrokes into a specific application, it creates a virtual keyboard device and sends real keyboard events through the Linux input stack.

## Example

```python
import rs_uinput

rs_uinput.type_text(
    text="Hello, world!",
    min_delay=0.05,
    max_delay=0.15
)
```

## How It Works

1. Python calls the Rust extension through PyO3.
2. Rust creates a virtual keyboard using `/dev/uinput`.
3. Each character is converted into the corresponding Linux key code.
4. Key press and key release events are sent through the kernel.
5. A random delay is applied between characters.

## How It Differs From pynput

`pynput` typically relies on higher-level desktop APIs (X11, Wayland compatibility layers, platform-specific event injection APIs, etc.).

`rs_uinput` operates at the Linux input-device layer by creating a virtual keyboard device.

```text
pynput
  ↓
Desktop API
  ↓
Application

rs_uinput
  ↓
Virtual Keyboard Device
  ↓
Linux Input Subsystem
  ↓
Application
```

Because it acts as an input device, applications receive the events through the normal Linux input pipeline rather than through a specific GUI automation API.

## How It Differs From Selenium

Selenium does not generate system-wide keyboard input.

Instead, Selenium controls a web browser through the browser's automation interface:

```text
Selenium
  ↓
Browser Driver
  ↓
Browser
```

This means Selenium can only interact with browser content that it controls.

`rs_uinput` generates keyboard events at the operating-system level, allowing text to be entered into any focused application that accepts keyboard input.

## Use Cases

- Desktop automation
- Automated testing
- Kiosk systems
- Accessibility tools
- Input simulation on Linux

## Requirements

- Linux
- Kernel `uinput` support
- Access to `/dev/uinput`
