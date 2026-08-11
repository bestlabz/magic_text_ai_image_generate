import base64
import json
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image

from magic_write import MagicWriteModel, save_preview_images


PROJECT_DIR = Path(__file__).resolve().parent
ML_MODEL_PATH = PROJECT_DIR / "magic_write_ml_model.pkl"


@st.cache_resource
def load_model(canvas_width: int, canvas_height: int) -> MagicWriteModel:
    return MagicWriteModel(canvas_width=canvas_width, canvas_height=canvas_height)


def image_bytes_from_data_uri(data_uri: str) -> bytes:
    if "," not in data_uri:
        return b""
    return base64.b64decode(data_uri.split(",", 1)[1])


def preview_tile_bytes(image_data: bytes, width: int = 720, height: int = 360) -> bytes:
    image = Image.open(BytesIO(image_data)).convert("RGBA")
    alpha_bbox = image.getchannel("A").getbbox()
    if alpha_bbox:
        image = image.crop(alpha_bbox)

    max_image_width = width - 72
    max_image_height = height - 72
    scale = min(max_image_width / image.width, max_image_height / image.height)
    resized_size = (
        max(1, int(round(image.width * scale))),
        max(1, int(round(image.height * scale))),
    )
    image = image.resize(resized_size, Image.Resampling.LANCZOS)

    tile = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_tile_background(tile)
    x = (width - image.width) // 2
    y = (height - image.height) // 2
    tile.alpha_composite(image, (x, y))

    output = BytesIO()
    tile.save(output, format="PNG", optimize=True)
    return output.getvalue()


def draw_tile_background(tile: Image.Image) -> None:
    tile.paste((0, 0, 0, 0), (0, 0, tile.width, tile.height))


def build_generation_kwargs(
    generation_mode: str,
    output_format: str,
    mood: str,
    seed_enabled: bool,
    seed: int,
    randomize_fonts: bool,
    randomize_designs: bool,
) -> dict:
    kwargs = {
        "generation_mode": generation_mode,
        "output_format": output_format,
        "randomize_fonts": randomize_fonts,
        "randomize_designs": randomize_designs,
    }

    if mood.strip():
        kwargs["mood"] = mood.strip()

    if seed_enabled:
        kwargs["seed"] = seed

    if generation_mode == "ml":
        kwargs["ml_model_path"] = str(ML_MODEL_PATH)

    return kwargs


st.set_page_config(page_title="Magic Write", page_icon="T", layout="wide")


def clear_generated_result() -> None:
    st.session_state.result = None


st.title("Magic Write")

with st.sidebar:
    st.header("Generator")
    text = st.text_area(
        "Text",
        value="Sparkle",
        height=100,
        key="text_input",
        on_change=clear_generated_result,
    )
    count = st.number_input(
        "Variants",
        min_value=1,
        max_value=10000,
        value=12,
        step=1,
        key="variant_count",
        on_change=clear_generated_result,
    )

    st.header("Canvas")
    canvas_width = st.number_input(
        "Width",
        min_value=160,
        max_value=2000,
        value=420,
        step=20,
        key="canvas_width",
        on_change=clear_generated_result,
    )
    canvas_height = st.number_input(
        "Height",
        min_value=160,
        max_value=2000,
        value=420,
        step=20,
        key="canvas_height",
        on_change=clear_generated_result,
    )

    st.header("JSON")
    output_label = st.selectbox(
        "Type",
        ["Fabric", "Konva", "Canvas"],
        key="json_type",
        on_change=clear_generated_result,
    )

    generation_mode = "ml"
    output_format = output_label.lower()
    mood = ""
    seed_enabled = False
    seed = 12345
    randomize_fonts = True
    randomize_designs = True

    generate_clicked = st.button("Generate", type="primary", use_container_width=True)

if "result" not in st.session_state:
    st.session_state.result = None

if st.session_state.result is not None:
    result_meta = st.session_state.result.get("meta", {}) if isinstance(st.session_state.result, dict) else {}
    if not isinstance(result_meta, dict) or result_meta.get("output_format") != output_format:
        st.session_state.result = None

if generate_clicked:
    if not text.strip():
        st.error("Enter text to generate.")
    elif generation_mode == "ml" and not ML_MODEL_PATH.exists():
        st.error(f"ML model file not found: {ML_MODEL_PATH}")
    else:
        try:
            model = load_model(int(canvas_width), int(canvas_height))
            st.session_state.result = model.generate(
                text.strip(),
                count=int(count),
                modern=generation_mode != "classic",
                **build_generation_kwargs(
                    generation_mode=generation_mode,
                    output_format=output_format,
                    mood=mood,
                    seed_enabled=seed_enabled,
                    seed=int(seed),
                    randomize_fonts=randomize_fonts,
                    randomize_designs=randomize_designs,
                ),
            )
        except Exception as exc:
            st.exception(exc)

result = st.session_state.result

if result is None:
    st.info("Choose options and generate text styles.")
else:
    meta = result.get("meta", {})
    st.caption(
        f"{meta.get('count', 0)} variants | "
        f"{meta.get('mode', 'unknown')} | "
        f"{meta.get('output_format', 'unknown')} | "
        f"seed {meta.get('seed', 'none')}"
    )

    preview_tab, json_tab, meta_tab = st.tabs(["Previews", "JSON", "Meta"])

    with preview_tab:
        previews = result.get("preview_image") or []
        if not previews:
            st.warning("No preview images were generated.")
        else:
            columns = st.columns(4)
            for index, preview in enumerate(previews, start=1):
                image_data = image_bytes_from_data_uri(str(preview.get("image", "")))
                with columns[(index - 1) % len(columns)]:
                    st.image(
                        preview_tile_bytes(image_data),
                        caption=f"Variant {index}",
                        use_container_width=True,
                    )

            if st.button("Save preview PNGs"):
                output_paths = save_preview_images(result, PROJECT_DIR / "preview_output")
                st.success(f"Saved {len(output_paths)} images to {PROJECT_DIR / 'preview_output'}")

    with json_tab:
        json_text = json.dumps(result.get("magic_write", []), indent=2)
        st.download_button(
            "Download JSON",
            data=json_text,
            file_name="magic_write.json",
            mime="application/json",
        )
        st.code(json_text, language="json")

    with meta_tab:
        st.json(meta)
