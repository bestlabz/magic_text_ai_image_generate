"""Split Magic Write hook modules."""

from ._load_local_env import _load_local_env
from .get_magic_write_training_dataset import get_magic_write_training_dataset
from .MagicWriteModel import MagicWriteModel
from ._clamp_number import _clamp_number
from ._clean_hex import _clean_hex
from ._http_get import _http_get
from ._load_cached_google_font_families import _load_cached_google_font_families
from .fetch_google_font_families import fetch_google_font_families
from ._rotate_hex_color import _rotate_hex_color
from ._variant_from_preset import _variant_from_preset
from ._make_rng import _make_rng
from ._resolve_generation_seed import _resolve_generation_seed
from ._shuffle_copy import _shuffle_copy
from ._pick_unused_font import _pick_unused_font
from ._pick_unused_font_with_global_fallback import _pick_unused_font_with_global_fallback
from ._font_pool_for_style import _font_pool_for_style
from ._randomize_style_font import _randomize_style_font
from ._design_signature import _design_signature
from ._style_visual_signature import _style_visual_signature
from ._apply_random_design import _apply_random_design
from ._normalize_font_families import _normalize_font_families
from ._font_kind import _font_kind
from ._balanced_font_families import _balanced_font_families
from ._apply_text_transform import _apply_text_transform
from ._adaptive_modern_layout import _adaptive_modern_layout
from ._font_family_style import _font_family_style
from ._styles_for_font_families import _styles_for_font_families
from ._intent_terms import _intent_terms
from ._style_search_text import _style_search_text
from ._local_style_library import _local_style_library
from ._style_candidates import _style_candidates
from ._ml_tokens import _ml_tokens
from .load_magic_write_ml_model import load_magic_write_ml_model
from .predict_magic_write_styles import predict_magic_write_styles
from ._ml_style_candidates import _ml_style_candidates
from ._font_cache_path import _font_cache_path
from ._download_google_font import _download_google_font
from ._system_font_path import _system_font_path
from ._load_font import _load_font
from ._line_width import _line_width
from ._fit_text_box import _fit_text_box
from ._konva_text import _konva_text
from ._text_lines import _text_lines
from ._split_display_lines import _split_display_lines
from ._layer_text import _layer_text
from ._composition_text_object import _composition_text_object
from ._polish_export_text_shadow import _polish_export_text_shadow
from ._modern_text_style_for_index import _modern_text_style_for_index
from ._modern_text_signature import _modern_text_signature
from ._assign_generation_text_ids import _assign_generation_text_ids
from ._modern_text_objects import _modern_text_objects
from ._fit_export_text_object_to_canvas import _fit_export_text_object_to_canvas
from ._text_visual_height_for_child import _text_visual_height_for_child
from ._tighten_composition_children import _tighten_composition_children
from ._use_single_font_family_per_group import _use_single_font_family_per_group
from ._remove_duplicate_text_children import _remove_duplicate_text_children
from ._dedupe_repeated_phrase_text import _dedupe_repeated_phrase_text
from ._normalize_repeated_child_text import _normalize_repeated_child_text
from ._modern_palette_value import _modern_palette_value
from ._hex_luminance import _hex_luminance
from ._strengthen_transparent_text_contrast import _strengthen_transparent_text_contrast
from ._sanitize_script_shadows import _sanitize_script_shadows
from ._sanitize_composition_shadow_extent import _sanitize_composition_shadow_extent
from ._compact_composition_vertical_gaps import _compact_composition_vertical_gaps
from ._composition_alpha_bbox import _composition_alpha_bbox
from ._scale_child_geometry import _scale_child_geometry
from ._shift_child_geometry import _shift_child_geometry
from ._fit_composition_children_to_canvas import _fit_composition_children_to_canvas
from ._modern_design_choices import _modern_design_choices
from ._apply_modern_composition_design import _apply_modern_composition_design
from ._composition_text_for_kind import _composition_text_for_kind
from ._modern_composition_variant import _modern_composition_variant
from ._modern_composition_groups import _modern_composition_groups
from ._font_families_from_magic_write import _font_families_from_magic_write
from ._draw_text_with_spacing import _draw_text_with_spacing
from ._modern_line_width import _modern_line_width
from ._draw_centered_line import _draw_centered_line
from ._fit_font_size_for_lines import _fit_font_size_for_lines
from ._trim_transparent_preview import _trim_transparent_preview
from ._draw_arc_text import _draw_arc_text
from ._render_modern_preview_data_uri import _render_modern_preview_data_uri
from ._draw_text_object_on_layer import _draw_text_object_on_layer
from ._render_group_preview_data_uri import _render_group_preview_data_uri
from .render_preview_data_uri import render_preview_data_uri
from ._normalize_output_format import _normalize_output_format
from ._normalize_generation_mode import _normalize_generation_mode
from ._is_bold_font_weight import _is_bold_font_weight
from ._konva_font_style import _konva_font_style
from ._konva_text_node import _konva_text_node
from ._konva_node_from_internal import _konva_node_from_internal
from ._konva_stage_object import _konva_stage_object
from ._fabric_shadow import _fabric_shadow
from ._fabric_char_spacing import _fabric_char_spacing
from ._fabric_text_object import _fabric_text_object
from ._fabric_text_objects_from_internal import _fabric_text_objects_from_internal
from ._fabric_canvas_object import _fabric_canvas_object
from ._canvas_shadow import _canvas_shadow
from ._canvas_font_css import _canvas_font_css
from ._canvas_text_element import _canvas_text_element
from ._canvas_json_object import _canvas_json_object
from ._canva_shadow import _canva_shadow
from ._canva_text_element import _canva_text_element
from ._canva_design_object import _canva_design_object
from ._format_magic_write_objects import _format_magic_write_objects
from .generate_magic_write import generate_magic_write
from .save_preview_images import save_preview_images
from .magic_write import magic_write

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")) and _name not in globals():
        globals()[_name] = getattr(_core, _name)

__all__ = [
    "_load_local_env",
    "get_magic_write_training_dataset",
    "MagicWriteModel",
    "_clamp_number",
    "_clean_hex",
    "_http_get",
    "_load_cached_google_font_families",
    "fetch_google_font_families",
    "_rotate_hex_color",
    "_variant_from_preset",
    "_make_rng",
    "_resolve_generation_seed",
    "_shuffle_copy",
    "_pick_unused_font",
    "_pick_unused_font_with_global_fallback",
    "_font_pool_for_style",
    "_randomize_style_font",
    "_design_signature",
    "_style_visual_signature",
    "_apply_random_design",
    "_normalize_font_families",
    "_font_kind",
    "_balanced_font_families",
    "_apply_text_transform",
    "_adaptive_modern_layout",
    "_font_family_style",
    "_styles_for_font_families",
    "_intent_terms",
    "_style_search_text",
    "_local_style_library",
    "_style_candidates",
    "_ml_tokens",
    "load_magic_write_ml_model",
    "predict_magic_write_styles",
    "_ml_style_candidates",
    "_font_cache_path",
    "_download_google_font",
    "_system_font_path",
    "_load_font",
    "_line_width",
    "_fit_text_box",
    "_konva_text",
    "_text_lines",
    "_split_display_lines",
    "_layer_text",
    "_composition_text_object",
    "_polish_export_text_shadow",
    "_modern_text_style_for_index",
    "_modern_text_signature",
    "_assign_generation_text_ids",
    "_modern_text_objects",
    "_fit_export_text_object_to_canvas",
    "_text_visual_height_for_child",
    "_tighten_composition_children",
    "_use_single_font_family_per_group",
    "_remove_duplicate_text_children",
    "_dedupe_repeated_phrase_text",
    "_normalize_repeated_child_text",
    "_modern_palette_value",
    "_hex_luminance",
    "_strengthen_transparent_text_contrast",
    "_sanitize_script_shadows",
    "_sanitize_composition_shadow_extent",
    "_compact_composition_vertical_gaps",
    "_composition_alpha_bbox",
    "_scale_child_geometry",
    "_shift_child_geometry",
    "_fit_composition_children_to_canvas",
    "_modern_design_choices",
    "_apply_modern_composition_design",
    "_composition_text_for_kind",
    "_modern_composition_variant",
    "_modern_composition_groups",
    "_font_families_from_magic_write",
    "_draw_text_with_spacing",
    "_modern_line_width",
    "_draw_centered_line",
    "_fit_font_size_for_lines",
    "_trim_transparent_preview",
    "_draw_arc_text",
    "_render_modern_preview_data_uri",
    "_draw_text_object_on_layer",
    "_render_group_preview_data_uri",
    "render_preview_data_uri",
    "_normalize_output_format",
    "_normalize_generation_mode",
    "_is_bold_font_weight",
    "_konva_font_style",
    "_konva_text_node",
    "_konva_node_from_internal",
    "_konva_stage_object",
    "_fabric_shadow",
    "_fabric_char_spacing",
    "_fabric_text_object",
    "_fabric_text_objects_from_internal",
    "_fabric_canvas_object",
    "_canvas_shadow",
    "_canvas_font_css",
    "_canvas_text_element",
    "_canvas_json_object",
    "_canva_shadow",
    "_canva_text_element",
    "_canva_design_object",
    "_format_magic_write_objects",
    "generate_magic_write",
    "save_preview_images",
    "magic_write",
]
