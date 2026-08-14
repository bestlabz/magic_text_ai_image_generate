# Magic Write Hooks Documentation

This project split the original large `magic_write.py` file into a `hooks/`
package. The public API still works through `magic_write.py`, but each main
function/class now also has its own hook file.

## Step-by-Step Flow

1. User code imports `magic_write.py`.
2. `magic_write.py` imports `hooks.magic_write_core` as the shared runtime.
3. `magic_write.py` re-exports everything from `hooks/__init__.py`.
4. `hooks/__init__.py` imports every individual hook module.
5. Each hook module loads shared constants, datasets, imports, and helpers from
   `hooks/magic_write_core.py`.
6. Public calls usually go through `magic_write(...)`, `generate_magic_write(...)`,
   or `MagicWriteModel.generate(...)`.
7. `generate_magic_write(...)` selects the generation mode, creates internal text
   objects, renders preview images, formats output JSON, and returns the result.

## Main Entry Files

| File | Purpose |
| --- | --- |
| `magic_write.py` | Backward-compatible root entry point. Existing imports like `import magic_write` keep working. |
| `hooks/__init__.py` | Package exporter. Imports all hook functions/classes and exposes them from `hooks`. |
| `hooks/magic_write_core.py` | Full shared implementation. Contains constants, datasets, helpers, and the real runtime used by all hooks. |
| `hooks/magic_write.py` | Public wrapper hook. Defines `magic_write(...)`, which calls `generate_magic_write(...)`. |
| `hooks/MagicWriteModel.py` | Model wrapper class used by Streamlit and other callers. |
| `hooks/generate_magic_write.py` | Main generation hook. Builds styles, previews, formatted JSON, and metadata. |

## Public Utility Hooks

| File | Purpose |
| --- | --- |
| `hooks/fetch_google_font_families.py` | Fetches or loads Google Font family names. |
| `hooks/get_magic_write_training_dataset.py` | Returns the reusable training/config dataset. |
| `hooks/load_magic_write_ml_model.py` | Loads the saved local ML model from disk. |
| `hooks/predict_magic_write_styles.py` | Predicts style labels from text using the ML model. |
| `hooks/render_preview_data_uri.py` | Renders a generated text object/group into a PNG data URI. |
| `hooks/save_preview_images.py` | Saves preview image data URIs as PNG files. |

## Input, Config, and Generic Helpers

| File | Purpose |
| --- | --- |
| `hooks/_load_local_env.py` | Loads `.env` values into environment variables. |
| `hooks/_clamp_number.py` | Clamps numeric values into allowed ranges. |
| `hooks/_clean_hex.py` | Validates and normalizes hex color strings. |
| `hooks/_http_get.py` | Performs HTTP GET requests with timeout and SSL handling. |
| `hooks/_make_rng.py` | Creates a seeded random generator. |
| `hooks/_resolve_generation_seed.py` | Chooses the effective generation seed. |
| `hooks/_shuffle_copy.py` | Returns a shuffled copy of a list. |
| `hooks/_rotate_hex_color.py` | Rotates or adjusts a color value for variation. |
| `hooks/_hex_luminance.py` | Calculates approximate color luminance. |

## Font Hooks

| File | Purpose |
| --- | --- |
| `hooks/_load_cached_google_font_families.py` | Reads cached Google Font metadata. |
| `hooks/_download_google_font.py` | Downloads Google Font files into the local cache. |
| `hooks/_font_cache_path.py` | Builds cache paths for downloaded fonts. |
| `hooks/_system_font_path.py` | Finds installed system fonts. |
| `hooks/_load_font.py` | Loads a PIL font object. |
| `hooks/_font_kind.py` | Classifies a font as script, serif, sans, display, mono, or decorative. |
| `hooks/_font_pool_for_style.py` | Selects a font pool for a style. |
| `hooks/_font_family_style.py` | Builds a style dictionary for a font family. |
| `hooks/_font_families_from_magic_write.py` | Extracts font family names from generated objects. |
| `hooks/_normalize_font_families.py` | Normalizes user-provided font family input. |
| `hooks/_balanced_font_families.py` | Balances font choices across font categories. |
| `hooks/_pick_unused_font.py` | Picks a font that has not been used yet. |
| `hooks/_pick_unused_font_with_global_fallback.py` | Picks an unused font with broader fallback support. |
| `hooks/_randomize_style_font.py` | Randomizes the font for a style. |
| `hooks/_styles_for_font_families.py` | Builds style candidates from selected font families. |

## Text and Layout Hooks

| File | Purpose |
| --- | --- |
| `hooks/_line_width.py` | Measures text line width. |
| `hooks/_modern_line_width.py` | Measures line width for modern preview rendering. |
| `hooks/_text_lines.py` | Splits text into display lines. |
| `hooks/_split_display_lines.py` | Creates balanced display line breaks. |
| `hooks/_apply_text_transform.py` | Applies case or text transformation rules. |
| `hooks/_adaptive_modern_layout.py` | Chooses modern text layout values based on text size. |
| `hooks/_fit_text_box.py` | Fits a single text object inside a text box. |
| `hooks/_fit_font_size_for_lines.py` | Reduces font size until lines fit within bounds. |
| `hooks/_fit_export_text_object_to_canvas.py` | Adjusts exported text objects to stay inside the canvas. |
| `hooks/_text_visual_height_for_child.py` | Estimates visual height for a child text layer. |
| `hooks/_tighten_composition_children.py` | Tightens spacing between composition child layers. |
| `hooks/_compact_composition_vertical_gaps.py` | Reduces excessive vertical gaps in compositions. |
| `hooks/_composition_alpha_bbox.py` | Finds visible alpha bounds for a rendered composition. |
| `hooks/_scale_child_geometry.py` | Scales child layer geometry. |
| `hooks/_shift_child_geometry.py` | Moves child layer geometry. |
| `hooks/_fit_composition_children_to_canvas.py` | Fits grouped composition layers into the canvas. |

## Classic and Modern Style Hooks

| File | Purpose |
| --- | --- |
| `hooks/_variant_from_preset.py` | Creates a style variant from a preset. |
| `hooks/_design_signature.py` | Builds a compact identity for a design. |
| `hooks/_style_visual_signature.py` | Builds a signature to avoid duplicate-looking styles. |
| `hooks/_apply_random_design.py` | Applies randomized color/effect choices to a style. |
| `hooks/_intent_terms.py` | Extracts intent/search terms from user text. |
| `hooks/_style_search_text.py` | Builds searchable text for a style preset. |
| `hooks/_local_style_library.py` | Scores and returns local style candidates. |
| `hooks/_style_candidates.py` | Creates classic style candidates for generation. |
| `hooks/_modern_text_style_for_index.py` | Creates a modern text style for a variant index. |
| `hooks/_modern_text_signature.py` | Builds a signature for modern text styles. |
| `hooks/_modern_text_objects.py` | Builds modern single-text objects. |
| `hooks/_modern_design_choices.py` | Chooses modern composition palette/effect pairs. |
| `hooks/_modern_palette_value.py` | Resolves palette color modes to actual color values. |
| `hooks/_apply_modern_composition_design.py` | Applies palette/effect styling to composition layers. |

## ML Hooks

| File | Purpose |
| --- | --- |
| `hooks/_ml_tokens.py` | Tokenizes text for ML prediction. |
| `hooks/_ml_style_candidates.py` | Converts ML predictions into style candidates. |

## Composition Hooks

| File | Purpose |
| --- | --- |
| `hooks/_layer_text.py` | Creates one internal text layer. |
| `hooks/_composition_text_object.py` | Wraps child layers into a composition group. |
| `hooks/_composition_text_for_kind.py` | Splits input text into role-based parts for a template. |
| `hooks/_modern_composition_variant.py` | Builds one modern composition variant. |
| `hooks/_modern_composition_groups.py` | Builds all requested modern composition variants. |
| `hooks/_use_single_font_family_per_group.py` | Forces a group to use one font family when needed. |
| `hooks/_remove_duplicate_text_children.py` | Removes duplicated child text layers. |
| `hooks/_dedupe_repeated_phrase_text.py` | Removes repeated phrases from text content. |
| `hooks/_normalize_repeated_child_text.py` | Normalizes repeated text across composition children. |
| `hooks/_strengthen_transparent_text_contrast.py` | Improves contrast for transparent previews. |
| `hooks/_sanitize_script_shadows.py` | Cleans script shadow settings. |
| `hooks/_sanitize_composition_shadow_extent.py` | Limits shadow spread so compositions fit better. |
| `hooks/_polish_export_text_shadow.py` | Adjusts shadows for export formats. |

## Preview Rendering Hooks

| File | Purpose |
| --- | --- |
| `hooks/_draw_text_with_spacing.py` | Draws characters manually with letter spacing. |
| `hooks/_draw_centered_line.py` | Draws a centered preview line with optional shadow. |
| `hooks/_draw_arc_text.py` | Draws text along an arc. |
| `hooks/_draw_text_object_on_layer.py` | Draws one internal text object onto a PIL layer. |
| `hooks/_render_modern_preview_data_uri.py` | Renders modern single-text previews. |
| `hooks/_render_group_preview_data_uri.py` | Renders grouped composition previews. |
| `hooks/_trim_transparent_preview.py` | Crops transparent padding from preview images. |

## Output Format Hooks

| File | Purpose |
| --- | --- |
| `hooks/_normalize_output_format.py` | Normalizes output names such as `fabric`, `konva`, or `canvas`. |
| `hooks/_normalize_generation_mode.py` | Normalizes generation mode names. |
| `hooks/_assign_generation_text_ids.py` | Assigns stable IDs to generated objects. |
| `hooks/_format_magic_write_objects.py` | Routes internal objects into the requested export format. |
| `hooks/_is_bold_font_weight.py` | Detects bold font weights. |
| `hooks/_konva_font_style.py` | Builds Konva-compatible font style text. |
| `hooks/_konva_text.py` | Creates the internal Konva-like text object. |
| `hooks/_konva_text_node.py` | Converts internal text to a Konva text node. |
| `hooks/_konva_node_from_internal.py` | Converts internal objects/groups to Konva nodes. |
| `hooks/_konva_stage_object.py` | Wraps Konva nodes in stage/layer JSON. |
| `hooks/_fabric_shadow.py` | Converts internal shadow data to Fabric shadow JSON. |
| `hooks/_fabric_char_spacing.py` | Converts letter spacing to Fabric char spacing. |
| `hooks/_fabric_text_object.py` | Converts internal text to a Fabric text object. |
| `hooks/_fabric_text_objects_from_internal.py` | Flattens grouped text into Fabric text objects. |
| `hooks/_fabric_canvas_object.py` | Wraps Fabric text objects in a Fabric canvas JSON object. |
| `hooks/_canvas_shadow.py` | Converts shadow data for generic canvas JSON. |
| `hooks/_canvas_font_css.py` | Builds CSS font shorthand for canvas rendering. |
| `hooks/_canvas_text_element.py` | Converts internal text to a generic canvas element. |
| `hooks/_canvas_json_object.py` | Wraps generic canvas elements in canvas JSON. |
| `hooks/_canva_shadow.py` | Converts shadow data for Canva-style JSON. |
| `hooks/_canva_text_element.py` | Converts internal text to a Canva-style element. |
| `hooks/_canva_design_object.py` | Wraps Canva-style elements in a design document. |

## How to Use

Use the stable public API from the root module:

```python
import magic_write

result = magic_write.magic_write(
    "Sparkle",
    count=12,
    modern=True,
    generation_mode="modern_composition",
    output_format="fabric",
)
```

Or use the model wrapper:

```python
from magic_write import MagicWriteModel

model = MagicWriteModel()
result = model.generate("Sparkle", count=12)
```

## Notes for Editing

- Edit behavior in `hooks/magic_write_core.py` first, because all hooks share
  that runtime.
- The individual hook files are useful for locating one function/class quickly.
- Public callers should keep importing from `magic_write.py` unless there is a
  specific reason to import from `hooks`.
- Files starting with `_` are internal helpers and can change more easily than
  public hooks.
