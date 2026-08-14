"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def generate_magic_write(
    text: str,
    count: int | None = 6,
    mood: str | None = None,
    model: str | None = LOCAL_MAGIC_WRITE_MODEL,
    timeout: int = 45,
    canvas_width: int = DEFAULT_CANVAS_WIDTH,
    canvas_height: int = DEFAULT_CANVAS_HEIGHT,
    modern: bool = False,
    all_fonts: bool = False,
    all_google_fonts: bool = False,
    font_families: list[str] | tuple[str, ...] | str | None = None,
    google_fonts_api_key: str | None = None,
    google_font_sort: str = "alpha",
    google_font_category: str | None = None,
    refresh_google_fonts: bool = False,
    randomize_fonts: bool = True,
    randomize_designs: bool = True,
    seed: int | None = None,
    output_format: str | None = None,
    output_type: str | None = None,
    canva_title: str | None = None,
    ml_model_path: str | os.PathLike[str] | None = None,
    generation_mode: str | None = None,
) -> dict[str, Any]:
    text = str(text or "").strip()
    if not text:
        raise ValueError("text is required")
    requested_count = int(_clamp_number(count, 1, 0, 10000)) if count is not None else None
    canvas_width = int(_clamp_number(canvas_width, DEFAULT_CANVAS_WIDTH, 160, 2000))
    canvas_height = int(_clamp_number(canvas_height, DEFAULT_CANVAS_HEIGHT, 160, 2000))
    model_name = LOCAL_MAGIC_WRITE_MODEL
    normalized_output_format = _normalize_output_format(output_format, output_type)
    resolved_generation_mode = _normalize_generation_mode(
        generation_mode,
        modern,
        ml_model_path,
        all_google_fonts,
        all_fonts,
        font_families,
    )
    effective_seed = _resolve_generation_seed(seed)
    rng = _make_rng(effective_seed)

    if requested_count == 0:
        return {
            "magic_write": [],
            "preview_image": [],
            "meta": {
                "model": model_name,
                "canvas_width": canvas_width,
                "canvas_height": canvas_height,
                "count": 0,
                "mode": resolved_generation_mode,
                "font_families": [],
                "child_font_families": [] if resolved_generation_mode == "modern_composition" else None,
                "randomize_fonts": randomize_fonts,
                "randomize_designs": randomize_designs,
                "seed": effective_seed,
                "output_format": normalized_output_format,
                "ml_model_path": str(ml_model_path) if ml_model_path else None,
                "google_font_sort": google_font_sort if all_google_fonts else None,
                "google_font_category": google_font_category if all_google_fonts else None,
            },
        }

    if resolved_generation_mode == "ml":
        styles = _ml_style_candidates(
            text,
            requested_count or 6,
            mood,
            ml_model_path,
            randomize_fonts,
            randomize_designs,
            rng,
        )
        objects = [_konva_text(text, style, z_index=index + 1, canvas_width=canvas_width, canvas_height=canvas_height)
                   for index, style in enumerate(styles)]
    elif resolved_generation_mode == "modern_text":
        objects = _modern_text_objects(
            text,
            requested_count,
            canvas_width=canvas_width,
            canvas_height=canvas_height,
            rng=rng,
            randomize_designs=randomize_designs,
        )
    elif resolved_generation_mode == "modern_composition":
        objects = _modern_composition_groups(
            text,
            requested_count,
            rng=rng,
            canvas_width=canvas_width,
            canvas_height=canvas_height,
            randomize_designs=randomize_designs,
        )
    elif all_google_fonts:
        google_families = fetch_google_font_families(
            api_key=google_fonts_api_key,
            sort=google_font_sort,
            category=google_font_category,
            refresh=refresh_google_fonts,
        )
        styles = _styles_for_font_families(
            google_families,
            count=requested_count,
            randomize_fonts=randomize_fonts,
            randomize_designs=randomize_designs,
            rng=rng,
        )
    elif all_fonts or font_families:
        styles = _styles_for_font_families(
            font_families,
            count=requested_count,
            randomize_fonts=randomize_fonts,
            randomize_designs=randomize_designs,
            rng=rng,
        )
    else:
        styles = _style_candidates(
            text,
            count=requested_count or 6,
            mood=mood,
            randomize_fonts=randomize_fonts,
            randomize_designs=randomize_designs,
            rng=rng,
        )
    if resolved_generation_mode in {"classic", "all_fonts", "all_google_fonts"}:
        objects = [_konva_text(text, style, z_index=index + 1, canvas_width=canvas_width, canvas_height=canvas_height)
                   for index, style in enumerate(styles)]
    _assign_generation_text_ids(objects, effective_seed)
    previews = [
        {
            "image": render_preview_data_uri(obj, canvas_width=canvas_width, canvas_height=canvas_height),
        }
        for obj in objects
    ]
    output_objects = _format_magic_write_objects(
        objects,
        normalized_output_format,
        canvas_width,
        canvas_height,
        canva_title=canva_title,
    )
    return {
        "magic_write": output_objects,
        "preview_image": previews,
        "meta": {
            "model": model_name,
            "canvas_width": canvas_width,
            "canvas_height": canvas_height,
            "count": len(objects),
            "mode": resolved_generation_mode,
            "font_families": _font_families_from_magic_write(
                objects,
                primary_per_group=resolved_generation_mode == "modern_composition",
            ),
            "child_font_families": (
                _font_families_from_magic_write(objects)
                if resolved_generation_mode == "modern_composition"
                else None
            ),
            "randomize_fonts": randomize_fonts,
            "randomize_designs": randomize_designs,
            "seed": effective_seed,
            "output_format": normalized_output_format,
            "ml_model_path": str(ml_model_path) if ml_model_path else None,
            "google_font_sort": google_font_sort if all_google_fonts else None,
            "google_font_category": google_font_category if all_google_fonts else None,
        },
    }


__all__ = ["generate_magic_write"]
