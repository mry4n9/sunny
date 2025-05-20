import re

def sanitize_xml_string(text_input):
    """
    Removes characters that are illegal in XML v1.0.
    This includes most C0 control characters (except for tab, newline, carriage return)
    and all C1 control characters. Also removes NULL bytes explicitly.
    Replaces illegal characters with an empty string (i.e., removes them).
    """
    if text_input is None:
        return "" # Return empty string for None to avoid issues downstream
    
    # Attempt to convert to string if not already.
    # This handles cases where numbers or other types might be passed.
    if not isinstance(text_input, str):
        try:
            text_input = str(text_input)
        except Exception:
            return "" # If conversion fails, return empty string

    # Remove NULL bytes first as they are particularly problematic
    # and can cause issues with other string operations.
    text = text_input.replace('\x00', '')

    # XML 1.0 valid character ranges:
    # Tab (#x9), Newline (#xA), Carriage Return (#xD)
    # Unicode #x20 to #xD7FF
    # Unicode #xE000 to #xFFFD
    # Unicode #x10000 to #x10FFFF (supplementary characters)
    
    # Build a list of allowed character codes
    sanitized_chars = []
    for char_code in map(ord, text):
        if (char_code == 0x9 or  # Tab
            char_code == 0xA or  # Newline
            char_code == 0xD or  # Carriage Return
            (0x20 <= char_code <= 0xD7FF) or
            (0xE000 <= char_code <= 0xFFFD) or
            (0x10000 <= char_code <= 0x10FFFF)):
            sanitized_chars.append(chr(char_code))
        # else:
            # Character is invalid.
            # Option 1: Skip it (effectively remove it) - current implementation
            # Option 2: Replace with a placeholder like a space: sanitized_chars.append(' ')
            # Option 3: Replace with a Unicode replacement character: sanitized_chars.append('\uFFFD')
            pass # Current choice: remove invalid characters

    return "".join(sanitized_chars)