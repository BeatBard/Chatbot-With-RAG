# legacy.py

import json
import os

# 1) Figure out where data_list.json is located
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'data_list.json')

# 2) Load the mapping from data_list.json
with open(json_path, 'r', encoding='utf-8') as f:
    data_list = json.load(f)

def fm_to_unicode(text: str) -> str:
    """
    Convert from FM-encoded Sinhala to standard Unicode using data_list.json.
    """
    for mapping in data_list:
        fm_val = mapping.get("fm", "")
        uni_val = mapping.get("uni", "")
        if fm_val and uni_val:
            text = text.replace(fm_val, uni_val)
    return text

def isi_to_unicode(text: str) -> str:
    """
    Convert from ISI-encoded Sinhala to standard Unicode using data_list.json.
    """
    for mapping in data_list:
        isi_val = mapping.get("isi", "")
        uni_val = mapping.get("uni", "")
        if isi_val and uni_val:
            text = text.replace(isi_val, uni_val)
    return text

def detect_legacy(text: str) -> str:
    """
    Simple heuristic to guess if text is likely 'fm' or 'isi' vs 'unicode'.
    Return 'fm', 'isi', or 'unicode'.
    """
    # Count how many characters are in the Sinhala Unicode block
    total_chars = len(text)
    if total_chars == 0:
        return "unicode"  # empty text, do nothing

    sinhala_unicode_count = sum(
        1 for ch in text if '\u0D80' <= ch <= '\u0DFF'
    )
    ratio = sinhala_unicode_count / total_chars

    # If ratio is quite high, likely it's already Unicode
    if ratio > 0.3:
        return "unicode"
    
    # Otherwise, guess 'fm' or 'isi'. You can do more advanced detection:
    # We'll do a naive guess: if we see "fm" pattern or "isi" pattern.
    # In real usage, adapt this to your actual text examples.
    fm_hints = ["fm", "wd", "%", "ldY", "jf"]  # etc. - partial guesses
    isi_hints = ["isi", "?", ">", "=", "rx"]   # etc. - partial guesses

    fm_score = sum(hint in text for hint in fm_hints)
    isi_score = sum(hint in text for hint in isi_hints)

    if fm_score >= isi_score:
        return "fm"
    else:
        return "isi"

def convert_to_unicode(text: str) -> str:
    """
    Automatically detect if text is 'fm', 'isi', or 'unicode',
    then convert to standard Unicode if needed.
    """
    style = detect_legacy(text)
    if style == "unicode":
        return text  # Already Unicode
    elif style == "fm":
        return fm_to_unicode(text)
    elif style == "isi":
        return isi_to_unicode(text)
