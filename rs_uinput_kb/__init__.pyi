def type_text(
    text: str,
    min_char_delay: float = 0.05,
    max_char_delay: float = 0.1,
    min_dwell_time: int = 20,
    max_dwell_time: int = 60,
    min_shift_delay: int = 10,
    max_shift_delay: int = 30
) -> None:
    """
    Simulates hardware keystrokes using Linux's /dev/uinput.
    
    By default, this uses jittered delays to mimic natural human typing dynamics. 
    For instantaneous machine-speed typing, set all delays to 0.
    
    Args:
        text (str): The string of characters to type.
        min_char_delay (float): Minimum delay between keystrokes in seconds. Default 0.05.
        max_char_delay (float): Maximum delay between keystrokes in seconds. Default 0.1.
        min_dwell_time (int): Minimum time a key is physically held down in milliseconds. Default 20.
        max_dwell_time (int): Maximum time a key is physically held down in milliseconds. Default 60.
        min_shift_delay (int): Minimum hesitation before/after pressing shift in milliseconds. Default 10.
        max_shift_delay (int): Maximum hesitation before/after pressing shift in milliseconds. Default 30.
    """
    ...