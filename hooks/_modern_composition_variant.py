"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_composition_variant(
    text: str,
    template: dict[str, Any],
    index: int,
    rng: random.Random,
    canvas_width: int,
    canvas_height: int,
    used_fonts: set[str],
    used_designs: set[tuple[str, str]],
    used_palettes: set[str],
    used_effects: set[str],
    randomize_designs: bool,
) -> dict[str, Any]:
    kind = str(template.get("kind") or "luxury_names")
    data = _composition_text_for_kind(text, kind)
    margin = canvas_width * 0.08
    full_w = canvas_width - margin * 2
    z_base = index * 10 + 1

    def pick_font(kind_name: str, extra_pool: list[str] | None = None) -> str:
        pool = extra_pool or CANVA_FONT_GROUPS[kind_name]
        return _pick_unused_font_with_global_fallback(pool, rng, used_fonts)

    def script_font() -> str:
        return pick_font("script")

    def serif_font() -> str:
        return pick_font("serif")

    def display_font() -> str:
        strong_display = [
            "Bebas Neue",
            "Anton",
            "League Spartan",
            "Oswald",
            "Bungee",
            "Fredoka One",
            "Alfa Slab One",
            "Archivo Black",
            "Impact",
            "Chalkboard",
        ]
        return pick_font("display", strong_display)

    def clean_block_font() -> str:
        return pick_font("display", ["Anton", "Impact", "Archivo Black", "League Spartan", "Bebas Neue"])

    def sans_font() -> str:
        return pick_font("sans")

    group_font = display_font()

    def shared_font() -> str:
        return group_font

    children: list[dict[str, Any]] = []
    if kind == "retro_3d_block":
        colorways = [
            ("#FFD36A", "#FF6A2E", "#E73535", "#1C1230", "#183F38"),
            ("#FFE994", "#FF4E43", "#D62839", "#101820", "#2C8B6F"),
            ("#FFB02E", "#F4472E", "#7B1E5E", "#111111", "#2B1864"),
            ("#F8E7B5", "#EF3F4F", "#0C2340", "#151515", "#2EC4B6"),
        ]
        fill, warm, red_depth, ink, teal_depth = colorways[index % len(colorways)]
        main_text = data.get("main") or text.upper()
        box_x = margin * 0.45
        box_w = canvas_width - box_x * 2
        block_font = clean_block_font()
        children.append(_layer_text(main_text, {"fontFamily": block_font, "fontSize": 74, "fontWeight": "bold", "fill": fill, "stroke": ink, "strokeWidth": 2.8, "shadowColor": ink, "shadowBlur": 0.5, "shadowOffsetX": 0.8, "shadowOffsetY": 1.0, "letterSpacing": -0.2, "lineHeight": 0.78, "role": "main"}, z_base + 5, box_x, 142, box_w, 112))
    elif kind == "script_3d_swoop":
        colorways = [
            ("#FF6A35", "#FFC85B", "#082D4A", "#0A122C", "#23A6A8"),
            ("#F95E47", "#FFE07A", "#123A52", "#211437", "#2EC4B6"),
            ("#FF8842", "#FFD36A", "#23172F", "#031B36", "#159A9C"),
        ]
        fill, glow, ink, navy, teal = colorways[index % len(colorways)]
        main_text = " ".join([data.get("script", ""), data.get("main", "")]).strip() or text
        box_x = margin * 0.35
        box_w = canvas_width - box_x * 2
        children.append(_layer_text(main_text, {"fontFamily": script_font(), "fontSize": 82, "fontWeight": "bold", "fontStyle": "italic", "fill": fill, "stroke": ink, "strokeWidth": 2.6, "shadowColor": teal, "shadowBlur": 0.8, "shadowOffsetX": 2.0, "shadowOffsetY": 2.2, "letterSpacing": 0, "lineHeight": 0.76, "role": "main"}, z_base + 4, box_x, 130, box_w, 128))
    elif kind == "tall_3d_comic":
        main_text = data.get("main") or text.upper()
        box_x = margin * 0.55
        box_w = canvas_width - box_x * 2
        block_font = clean_block_font()
        children.append(_layer_text(main_text, {"fontFamily": block_font, "fontSize": 72, "fontWeight": "bold", "fill": "#FFD53F", "stroke": "#050505", "strokeWidth": 4.0, "shadowColor": "#050505", "shadowBlur": 0.5, "shadowOffsetX": 0.8, "shadowOffsetY": 1.0, "letterSpacing": -0.3, "lineHeight": 0.78, "role": "main"}, z_base + 5, box_x, 142, box_w, 114))
    elif kind == "study_mode_script":
        script = data.get("script") or "Study"
        main = data.get("main") or text.upper()
        children.append(_layer_text(script, {"fontFamily": script_font(), "fontSize": 62, "fontWeight": "bold", "fontStyle": "italic", "fill": "#FFF5D7", "stroke": "#0C3342", "strokeWidth": 1.4, "shadowColor": "#1D6B73", "shadowBlur": 0.6, "shadowOffsetX": 1.3, "shadowOffsetY": 1.4, "lineHeight": 0.78, "role": "script"}, z_base + 3, margin, 96, full_w, 78))
        children.append(_layer_text(main, {"fontFamily": clean_block_font(), "fontSize": 66, "fontWeight": "bold", "fill": "#F57B45", "stroke": "#0C3342", "strokeWidth": 2.8, "shadowColor": "#0C3342", "shadowBlur": 0.5, "shadowOffsetX": 3.0, "shadowOffsetY": 3.6, "letterSpacing": -0.2, "lineHeight": 0.78, "role": "main"}, z_base + 7, margin, 168, full_w, 106))
    elif kind == "festival_ribbon_script":
        script = data.get("script") or "HAPPY"
        main = data.get("main") or text
        children.append(_layer_text(script, {"fontFamily": sans_font(), "fontSize": 25, "fontWeight": "bold", "fill": "#F9B72E", "letterSpacing": 5.2, "lineHeight": 0.86, "role": "sub"}, z_base, margin, 100, full_w, 38))
        children.append(_layer_text(main, {"fontFamily": script_font(), "fontSize": 86, "fontWeight": "bold", "fontStyle": "italic", "fill": "#8E24C7", "stroke": "#FFFFFF", "strokeWidth": 1.6, "shadowColor": "#5A168E", "shadowBlur": 1.0, "shadowOffsetX": 2.0, "shadowOffsetY": 2.2, "lineHeight": 0.74, "role": "main"}, z_base + 4, margin, 132, full_w, 128))
    elif kind == "chrome_loop_script":
        main_text = " ".join([data.get("script", ""), data.get("main", "")]).strip() or text
        children.append(_layer_text(main_text, {"fontFamily": script_font(), "fontSize": 76, "fontWeight": "normal", "fontStyle": "italic", "fill": "#F6A07E", "stroke": "#083947", "strokeWidth": 2.2, "shadowColor": "#0E778A", "shadowBlur": 1.0, "shadowOffsetX": 1.8, "shadowOffsetY": 2.0, "lineHeight": 0.78, "role": "main"}, z_base + 4, margin, 132, full_w, 128))
    elif kind == "gloss_burst_script":
        main_text = " ".join([data.get("script", ""), data.get("main", "")]).strip() or text
        children.append(_layer_text(main_text, {"fontFamily": script_font(), "fontSize": 82, "fontWeight": "bold", "fontStyle": "italic", "fill": "#E32216", "stroke": "#FFFFFF", "strokeWidth": 1.3, "shadowColor": "#7A0505", "shadowBlur": 1.0, "shadowOffsetX": 2.0, "shadowOffsetY": 2.4, "lineHeight": 0.76, "role": "main"}, z_base + 3, margin, 144, full_w, 110))
    elif kind == "preview_brush_sticker":
        children.append(_layer_text(data.get("script") or data.get("main", text), {"fontFamily": script_font(), "fontSize": 58, "fontWeight": "bold", "fontStyle": "italic", "fill": "#FF6B6B", "stroke": "#FFFFFF", "strokeWidth": 3.0, "shadowColor": "#FFC3A6", "shadowBlur": 0, "shadowOffsetX": 4.0, "shadowOffsetY": 6.0, "letterSpacing": 0, "rotation": -4, "lineHeight": 0.78, "role": "script"}, z_base, margin, 122, full_w, 78))
        if data.get("main") and data.get("script"):
            children.append(_layer_text(data["main"], {"fontFamily": script_font(), "fontSize": 54, "fontWeight": "bold", "fontStyle": "italic", "fill": "#FF6B6B", "stroke": "#FFFFFF", "strokeWidth": 3.0, "shadowColor": "#FFC3A6", "shadowBlur": 0, "shadowOffsetX": 4.0, "shadowOffsetY": 6.0, "letterSpacing": 0, "rotation": -4, "lineHeight": 0.78, "role": "main"}, z_base + 1, margin, 180, full_w, 82))
    elif kind == "preview_glow_script":
        children.append(_layer_text(" ".join([data.get("script", ""), data.get("main", "")]).strip() or text, {"fontFamily": script_font(), "fontSize": 58, "fontWeight": "normal", "fontStyle": "italic", "fill": "#FFF8D8", "stroke": "#FFD66B", "strokeWidth": 1.2, "shadowColor": "#FFE58A", "shadowBlur": 24, "shadowOffsetX": 0, "shadowOffsetY": 0, "letterSpacing": 0, "rotation": -2, "lineHeight": 0.82, "role": "main"}, z_base, margin, 154, full_w, 96))
    elif kind == "preview_serif_luxe":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": serif_font(), "fontSize": 35, "fontWeight": "normal", "fontStyle": "italic", "fill": "#15422C", "letterSpacing": 0.4, "lineHeight": 0.86, "role": "script"}, z_base, margin, 126, full_w, 54))
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 56, "fontWeight": "bold", "fill": "#15422C", "stroke": "#F7E9C8", "strokeWidth": 0.8, "shadowColor": "#C99718", "shadowBlur": 1.2, "shadowOffsetX": 1.4, "shadowOffsetY": 2.2, "letterSpacing": 0.6, "lineHeight": 0.84, "role": "main"}, z_base + 1, margin, 168 if data.get("script") else 150, full_w, 112))
    elif kind == "preview_script_block_mix":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": script_font(), "fontSize": 38, "fontWeight": "bold", "fontStyle": "italic", "fill": "#AEB5C1", "rotation": -3, "letterSpacing": 0, "lineHeight": 0.82, "role": "script"}, z_base, margin, 126, full_w, 60))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 58, "fontWeight": "bold", "fill": "#FF4F61", "stroke": "#FFFFFF", "strokeWidth": 1.4, "shadowColor": "#AEB5C1", "shadowBlur": 0, "shadowOffsetX": -4.0, "shadowOffsetY": -3.0, "letterSpacing": 0.4, "lineHeight": 0.84, "role": "main"}, z_base + 1, margin, 174, full_w, 98))
    elif kind == "preview_sale_stack":
        if data.get("script"):
            children.append(_layer_text(data["script"].upper(), {"fontFamily": display_font(), "fontSize": 42, "fontWeight": "bold", "fill": "#F9C74F", "stroke": "#FFFFFF", "strokeWidth": 1.5, "shadowColor": "#FF4F61", "shadowBlur": 0, "shadowOffsetX": 3.0, "shadowOffsetY": 3.0, "letterSpacing": 1.0, "role": "script"}, z_base, margin, 122, full_w, 58))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 68, "fontWeight": "bold", "fill": "#FF4F61", "stroke": "#FFFFFF", "strokeWidth": 2.0, "shadowColor": "#7B2CBF", "shadowBlur": 0, "shadowOffsetX": 6.0, "shadowOffsetY": 7.0, "letterSpacing": 0.4, "lineHeight": 0.82, "role": "main"}, z_base + 1, margin, 168, full_w, 116))
    elif kind == "preview_comic_offset":
        children.append(_layer_text(" ".join([data.get("script", ""), data.get("main", "")]).strip().upper() or text.upper(), {"fontFamily": display_font(), "fontSize": 58, "fontWeight": "bold", "fill": "#20A9D6", "stroke": "#FFFFFF", "strokeWidth": 2.2, "shadowColor": "#FF4F61", "shadowBlur": 0, "shadowOffsetX": 5.0, "shadowOffsetY": 0, "letterSpacing": 0.8, "lineHeight": 0.84, "role": "main"}, z_base, margin, 154, full_w, 112))
    elif kind == "preview_neon_stack":
        if data.get("script"):
            children.append(_layer_text(data["script"].upper(), {"fontFamily": display_font(), "fontSize": 32, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#FF8AD7", "strokeWidth": 1.2, "shadowColor": "#FF4FB3", "shadowBlur": 15, "letterSpacing": 1.2, "role": "script"}, z_base, margin, 132, full_w, 46))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 62, "fontWeight": "bold", "fill": "#FF4FB3", "stroke": "#FF8AD7", "strokeWidth": 1.6, "shadowColor": "#FF4FB3", "shadowBlur": 20, "shadowOffsetX": 0, "shadowOffsetY": 0, "letterSpacing": 0.4, "lineHeight": 0.84, "role": "main"}, z_base + 1, margin, 176, full_w, 92))
    elif kind == "preview_chrome_shadow":
        children.append(_layer_text(" ".join([data.get("script", ""), data.get("main", "")]).strip().upper() or text.upper(), {"fontFamily": display_font(), "fontSize": 58, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#2D3552", "strokeWidth": 2.2, "shadowColor": "#BFC6D1", "shadowBlur": 0, "shadowOffsetX": 4.0, "shadowOffsetY": 5.0, "letterSpacing": 2.4, "lineHeight": 0.84, "role": "main"}, z_base, margin, 158, full_w, 106))
    elif kind == "light_script":
        children.append(_layer_text(data["main"], {"fontFamily": script_font(), "fontSize": 64, "fontWeight": "normal", "fontStyle": "italic", "fill": "#FFFFFF", "stroke": "#FFD37A", "strokeWidth": 1.3, "shadowColor": "#FFD37A", "shadowBlur": 18, "shadowOffsetX": 0, "shadowOffsetY": 0, "letterSpacing": 0, "lineHeight": 0.82, "role": "main"}, z_base, margin, 154, full_w, 96))
    elif kind == "neon_glow":
        children.append(_layer_text(data["main"], {"fontFamily": script_font(), "fontSize": 54, "fontWeight": "normal", "fontStyle": "italic", "fill": "#FFFFFF", "stroke": "#9A8CFF", "strokeWidth": 1.4, "shadowColor": "#8179FF", "shadowBlur": 18, "shadowOffsetX": 0, "shadowOffsetY": 0, "letterSpacing": 0, "lineHeight": 0.86, "role": "main"}, z_base, margin, 154, full_w, 100))
    elif kind == "thank_you":
        if data.get("top"):
            children.append(_layer_text(data["top"], {"fontFamily": shared_font(), "fontSize": 46, "fontWeight": "bold", "fill": "#FF5056", "letterSpacing": 1.0, "rotation": -3, "lineHeight": 0.88, "role": "top"}, z_base, margin, 136, full_w, 50))
        if data.get("middle"):
            children.append(_layer_text(data["middle"], {"fontFamily": shared_font(), "fontSize": 34, "fontWeight": "bold", "fill": "#FF5056", "stroke": "#FFFFFF", "strokeWidth": 1.0, "lineHeight": 0.86, "role": "middle"}, z_base + 1, margin, 172, full_w, 36))
        main_y = 202 if data.get("middle") else 184 if data.get("top") else 170
        children.append(_layer_text(data["main"], {"fontFamily": shared_font(), "fontSize": 44, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#FF5056", "strokeWidth": 2.0, "shadowColor": "#FF5056", "shadowBlur": 0, "shadowOffsetX": 1.2, "shadowOffsetY": 1.6, "letterSpacing": 0.6, "lineHeight": 0.88, "role": "main"}, z_base + 2, margin, main_y, full_w, 50))
    elif kind == "bride_groom":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": script_font(), "fontSize": 58, "fontWeight": "normal", "fontStyle": "italic", "fill": "#16462D", "lineHeight": 0.85, "role": "script"}, z_base, margin, 128, full_w, 86))
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 44, "fontWeight": "normal", "fill": "#16462D", "letterSpacing": 0.4, "lineHeight": 0.88, "role": "main"}, z_base + 1, margin, 200 if data.get("script") else 170, full_w, 80))
    elif kind == "happy_birthday":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": script_font(), "fontSize": 42, "fontWeight": "bold", "fill": "#111111", "stroke": "#FFFFFF", "strokeWidth": 1.2, "rotation": -4, "lineHeight": 0.9, "role": "script"}, z_base, margin, 128, full_w, 66))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 48, "fontWeight": "bold", "fill": "#050505", "letterSpacing": 0.2, "lineHeight": 0.9, "role": "main"}, z_base + 1, margin, 186 if data.get("script") else 162, full_w, 96))
    elif kind == "graduation_varsity_stack":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": serif_font(), "fontSize": 30, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#123A6F", "strokeWidth": 1.4, "shadowColor": "#0B2448", "shadowBlur": 0, "shadowOffsetX": 2.0, "shadowOffsetY": 2.2, "letterSpacing": 1.0, "rotation": -2, "lineHeight": 0.9, "role": "script"}, z_base, margin, 116, full_w, 48))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 64, "fontWeight": "bold", "fill": "#F6C84B", "stroke": "#123A6F", "strokeWidth": 2.8, "shadowColor": "#0B2448", "shadowBlur": 0, "shadowOffsetX": 5.0, "shadowOffsetY": 6.0, "letterSpacing": 1.0, "lineHeight": 0.84, "role": "main"}, z_base + 1, margin, 158, full_w, 112))
    elif kind == "graduation_script_block":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": script_font(), "fontSize": 52, "fontWeight": "bold", "fontStyle": "italic", "fill": "#FF4F61", "stroke": "#0C2340", "strokeWidth": 1.2, "shadowColor": "#0C2340", "shadowBlur": 0, "shadowOffsetX": 3.0, "shadowOffsetY": 3.6, "letterSpacing": 0, "rotation": -5, "lineHeight": 0.82, "role": "script"}, z_base, margin, 104, full_w, 82))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 58, "fontWeight": "bold", "fill": "#FFF4D0", "stroke": "#0C2340", "strokeWidth": 3.0, "shadowColor": "#FF4F61", "shadowBlur": 0, "shadowOffsetX": -3.5, "shadowOffsetY": 5.0, "letterSpacing": 0.8, "lineHeight": 0.84, "role": "main"}, z_base + 1, margin, 178, full_w, 104))
    elif kind == "graduation_badge_shadow":
        if data.get("script"):
            children.append(_layer_text(data["script"].upper(), {"fontFamily": sans_font(), "fontSize": 20, "fontWeight": "bold", "fill": "#35B8EA", "letterSpacing": 4.2, "lineHeight": 0.9, "role": "sub"}, z_base, margin, 116, full_w, 34))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 66, "fontWeight": "bold", "fill": "#FF6B35", "stroke": "#FFFFFF", "strokeWidth": 2.4, "shadowColor": "#173F8A", "shadowBlur": 0, "shadowOffsetX": 6.0, "shadowOffsetY": 7.0, "letterSpacing": 0.4, "lineHeight": 0.82, "role": "main"}, z_base + 1, margin, 156, full_w, 116))
    elif kind == "graduation_neon_label":
        children.append(_layer_text(f"{data.get('script', '').upper()} {data.get('main', '')}".strip(), {"fontFamily": display_font(), "fontSize": 38, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#FF4FB3", "strokeWidth": 1.6, "shadowColor": "#FF4FB3", "shadowBlur": 18, "shadowOffsetX": 0, "shadowOffsetY": 0, "letterSpacing": 1.0, "lineHeight": 0.86, "role": "main"}, z_base, margin, 164, full_w, 70))
    elif kind == "graduation_serif_split":
        if data.get("script"):
            children.append(_layer_text(data["script"].upper(), {"fontFamily": sans_font(), "fontSize": 24, "fontWeight": "bold", "fill": "#123A6F", "stroke": "#FFFFFF", "strokeWidth": 0.8, "shadowColor": "#A9B3C1", "shadowBlur": 1.6, "shadowOffsetX": 1.0, "shadowOffsetY": 2.0, "letterSpacing": 4.0, "lineHeight": 0.9, "role": "sub"}, z_base, margin, 128, full_w, 40))
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 52, "fontWeight": "bold", "fill": "#D6A816", "stroke": "#123A6F", "strokeWidth": 1.8, "shadowColor": "#A3832C", "shadowBlur": 1.0, "shadowOffsetX": 2.0, "shadowOffsetY": 3.0, "letterSpacing": 1.0, "lineHeight": 0.86, "role": "main"}, z_base + 1, margin, 178, full_w, 82))
    elif kind == "graduation_champ_stamp":
        if data.get("script"):
            children.append(_layer_text(data["script"].upper(), {"fontFamily": sans_font(), "fontSize": 22, "fontWeight": "bold", "fill": "#1F5BFF", "stroke": "#FFFFFF", "strokeWidth": 1.0, "letterSpacing": 3.2, "lineHeight": 0.9, "role": "sub"}, z_base, margin, 122, full_w, 34))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 58, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#1F5BFF", "strokeWidth": 3.0, "shadowColor": "#FF595E", "shadowBlur": 0, "shadowOffsetX": 4.0, "shadowOffsetY": 5.0, "letterSpacing": 1.2, "lineHeight": 0.84, "role": "main"}, z_base + 1, margin, 162, full_w, 100))
    elif kind == "golden_hour":
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 58, "fontWeight": "bold", "fill": "#D8A919", "shadowColor": "#BCA36B", "shadowBlur": 1.2, "shadowOffsetX": 2, "shadowOffsetY": 3, "letterSpacing": 0.2, "lineHeight": 0.83, "role": "main"}, z_base, margin, 136, full_w, 158))
    elif kind == "script_club":
        children.append(_layer_text(data["script"], {"fontFamily": script_font(), "fontSize": 50, "fontWeight": "normal", "fontStyle": "italic", "fill": "#5C84FF", "stroke": "#FFFFFF", "strokeWidth": 0.8, "rotation": -4, "lineHeight": 0.82, "role": "script"}, z_base, margin, 164, full_w, 70))
        if data.get("sub"):
            children.append(_layer_text(data["sub"], {"fontFamily": sans_font(), "fontSize": 10, "fontWeight": "bold", "fill": "#FFFFFF", "letterSpacing": 3.4, "role": "sub"}, z_base + 1, margin, 218, full_w, 24))
    elif kind == "xoxo":
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 50, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#D94E78", "strokeWidth": 2.2, "shadowColor": "#F4A3B8", "shadowBlur": 0, "shadowOffsetX": 3, "shadowOffsetY": 3, "letterSpacing": 1.6, "role": "main"}, z_base, margin, 162, full_w, 90))
    elif kind == "studio_badge":
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 38, "fontWeight": "normal", "fill": "#FFFFFF", "stroke": "#F6F6F6", "strokeWidth": 0.6, "letterSpacing": 0.4, "lineHeight": 0.9, "role": "main"}, z_base, margin, 132, full_w, 112))
        if data.get("badge"):
            children.append(_layer_text(data["badge"], {"fontFamily": sans_font(), "fontSize": 13, "fontWeight": "bold", "fill": "#FFFFFF", "stroke": "#D93C76", "strokeWidth": 3.5, "letterSpacing": 1.1, "role": "badge"}, z_base + 1, margin, 244, full_w, 32))
    elif kind == "streaming_now":
        if data.get("script"):
            children.append(_layer_text(data["script"], {"fontFamily": script_font(), "fontSize": 28, "fontWeight": "normal", "fill": "#2C8B6F", "lineHeight": 0.86, "role": "script"}, z_base, margin, 142, full_w, 42))
        children.append(_layer_text(data["main"], {"fontFamily": display_font(), "fontSize": 54, "fontWeight": "bold", "fill": "#F0B3E8", "stroke": "#2C8B6F", "strokeWidth": 1.4, "shadowColor": "#2C8B6F", "shadowBlur": 0, "shadowOffsetX": 0, "shadowOffsetY": 4, "letterSpacing": 0.4, "lineHeight": 0.82, "role": "main"}, z_base + 1, margin, 174, full_w, 82))
    elif kind == "quarterly_targets":
        if data.get("sub"):
            children.append(_layer_text(data["sub"], {"fontFamily": sans_font(), "fontSize": 21, "fontWeight": "bold", "fontStyle": "italic", "fill": "#8AA0A0", "letterSpacing": 1.8, "role": "sub"}, z_base, margin, 140, full_w, 38))
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 50, "fontWeight": "bold", "fill": "#173F8A", "letterSpacing": -0.8, "lineHeight": 0.85, "role": "main"}, z_base + 1, margin, 174 if data.get("sub") else 166, full_w, 78))
    elif kind == "quarter_roadmap":
        if data.get("serif"):
            children.append(_layer_text(data["serif"], {"fontFamily": serif_font(), "fontSize": 26, "fontWeight": "normal", "fill": "#42A4FF", "letterSpacing": 1.4, "role": "serif"}, z_base, margin, 148, full_w, 44))
        children.append(_layer_text(data["main"], {"fontFamily": sans_font(), "fontSize": 31, "fontWeight": "normal", "fill": "#2D3552", "letterSpacing": 1.7, "role": "main"}, z_base + 1, margin, 186 if data.get("serif") else 172, full_w, 52))
    elif kind == "neon_open":
        children.append(_layer_text(data["main"], {"fontFamily": script_font(), "fontSize": 45, "fontWeight": "normal", "fill": "#FFFFFF", "stroke": "#8B7DFF", "strokeWidth": 1.4, "shadowColor": "#8179FF", "shadowBlur": 13, "lineHeight": 0.9, "role": "main"}, z_base, margin, 150, full_w, 110))
    elif kind == "editorial_caps":
        children.append(_layer_text(data["main"], {"fontFamily": serif_font(), "fontSize": 45, "fontWeight": "normal", "fontStyle": "italic", "fill": "#B64040", "letterSpacing": 0.6, "lineHeight": 0.86, "role": "main"}, z_base, margin, 142, full_w, 120))
    else:
        children.append(_layer_text(data.get("script", text), {"fontFamily": script_font(), "fontSize": 52, "fontWeight": "normal", "fontStyle": "italic", "fill": "#B64040", "lineHeight": 0.82, "role": "script"}, z_base, margin, 130, full_w, 82))
        children.append(_layer_text(data.get("main", text), {"fontFamily": serif_font(), "fontSize": 30, "fontWeight": "normal", "fill": "#B64040", "lineHeight": 0.9, "role": "main"}, z_base + 1, margin, 196, full_w, 76))

    children = _normalize_repeated_child_text(children)
    children = _remove_duplicate_text_children(children)
    if kind not in MIXED_FONT_COMPOSITION_KINDS:
        children = _use_single_font_family_per_group(children)
    if kind in PREMIUM_REFERENCE_COMPOSITION_KINDS:
        palette_name = "reference_premium"
        effect_name = kind
    else:
        children, palette_name, effect_name = _apply_modern_composition_design(
            children,
            kind,
            index,
            rng,
            randomize_designs,
            used_designs,
            used_palettes,
            used_effects,
        )
        children = _tighten_composition_children(children, canvas_height)
    children = _strengthen_transparent_text_contrast(children)
    children = _sanitize_script_shadows(children)
    children = _sanitize_composition_shadow_extent(children)
    children = _compact_composition_vertical_gaps(children, canvas_width, canvas_height)
    children = _fit_composition_children_to_canvas(children, canvas_width, canvas_height)
    result = _composition_text_object(str(template.get("name") or kind), kind, children, index + 1, canvas_width, canvas_height)
    result["magicWritePalette"] = palette_name
    result["magicWriteEffect"] = effect_name
    return result


__all__ = ["_modern_composition_variant"]
