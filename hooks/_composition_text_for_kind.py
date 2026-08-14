"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _composition_text_for_kind(text: str, kind: str) -> dict[str, Any]:
    normalized = text.lower()
    lines = _text_lines(text)
    display_lines = _split_display_lines(text, 2)
    display_first = display_lines[0] if display_lines else (lines[0] if lines else text)
    display_second = display_lines[1] if len(display_lines) > 1 else ""
    first = lines[0] if lines else text
    second = lines[1] if len(lines) > 1 else ""
    third = lines[2] if len(lines) > 2 else ""

    if kind in {"light_script", "neon_glow"}:
        return {"main": " ".join(display_lines)}
    if kind in {
        "retro_3d_block",
        "script_3d_swoop",
        "tall_3d_comic",
        "study_mode_script",
        "festival_ribbon_script",
        "chrome_loop_script",
        "gloss_burst_script",
        "preview_brush_sticker",
        "preview_glow_script",
        "preview_serif_luxe",
        "preview_script_block_mix",
        "preview_sale_stack",
        "preview_comic_offset",
        "preview_neon_stack",
        "preview_chrome_shadow",
    }:
        words = re.findall(r"[A-Za-z0-9'&]+", text)
        if len(words) >= 2:
            split_at = max(1, len(words) // 2)
            top = " ".join(words[:split_at])
            main = " ".join(words[split_at:])
        else:
            top = ""
            main = first
        if kind in {"preview_sale_stack", "preview_neon_stack", "preview_chrome_shadow"}:
            return {"script": top, "main": main.upper()}
        if kind == "preview_serif_luxe":
            return {"script": top, "main": main.upper() if top else first.upper()}
        if kind in {"retro_3d_block", "tall_3d_comic"}:
            return {"script": "", "main": " ".join(words).upper() if words else first.upper()}
        if kind == "study_mode_script":
            return {"script": top or display_first, "main": (main or display_second or display_first).upper()}
        if kind == "festival_ribbon_script":
            return {"script": top.upper() if top else "HAPPY", "main": main or first}
        return {"script": top, "main": main}
    if kind == "thank_you":
        if len(lines) >= 3 and second.strip() in {"&", "+", "and", "AND"}:
            return {"top": first.upper(), "middle": second.strip(), "main": third.upper()}
        if "thank" in normalized and "you" in normalized:
            return {"top": "THANK", "middle": "", "main": "YOU"}
        if len(lines) >= 2:
            return {"top": first.upper(), "middle": "", "main": second.upper()}
        return {"top": "", "middle": "", "main": first.upper()}
    if kind == "happy_birthday":
        if "birthday" in normalized:
            return {"script": "Happy", "main": "BIRTHDAY"}
        if len(lines) >= 2:
            return {"script": first, "main": "\n".join(line.upper() for line in lines[1:3])}
        return {"script": "", "main": first.upper()}
    if kind in {"graduation_varsity_stack", "graduation_script_block", "graduation_badge_shadow", "graduation_neon_label", "graduation_serif_split", "graduation_champ_stamp"}:
        year_match = re.search(r"\b(20\d{2}|19\d{2})\b", text)
        year = year_match.group(1) if year_match else ""
        prefix = re.sub(r"\b(20\d{2}|19\d{2})\b", "", text, flags=re.IGNORECASE)
        prefix = re.sub(r"\s+", " ", prefix).strip(" -")
        if not prefix:
            prefix = "Class Of"
        if "class" in normalized and "of" in normalized:
            script = "Class"
            main = f"OF {year}".strip()
        elif len(display_lines) >= 2:
            script = display_first
            main = display_second
        else:
            script = prefix
            main = year or first
        return {"script": script, "main": main.upper(), "year": year}
    if kind == "bride_groom":
        if "bride" in normalized or "groom" in normalized:
            return {"script": "Bride &", "main": "GROOM"}
        if len(lines) >= 3 and second.strip() == "&":
            return {"script": f"{first} &", "main": third}
        if len(lines) >= 2:
            return {"script": first, "main": second}
        return {"script": "", "main": first}
    if kind == "golden_hour":
        return {"main": "\n".join(line.upper() for line in display_lines)}
    if kind == "script_club":
        return {"script": " ".join(display_lines), "sub": ""}
    if kind == "xoxo":
        return {"main": " ".join(display_lines).upper()}
    if kind == "studio_badge":
        return {"main": "\n".join(display_lines).upper(), "badge": ""}
    if kind == "streaming_now":
        return {"script": display_first if display_second else "", "main": (display_second or display_first).upper()}
    if kind == "quarterly_targets":
        return {"sub": display_first.upper() if display_second else "", "main": (display_second or display_first).upper()}
    if kind == "quarter_roadmap":
        return {"serif": display_first if display_second else "", "main": (display_second or display_first).upper()}
    if kind == "neon_open":
        return {"main": "\n".join(display_lines)}
    if kind == "editorial_caps":
        return {"main": "\n".join(line.upper() for line in display_lines)}
    return {"script": first if len(lines) > 1 else "", "main": "\n".join(lines[1:]) if len(lines) > 1 else first}


__all__ = ["_composition_text_for_kind"]
