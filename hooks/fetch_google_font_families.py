"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def fetch_google_font_families(
    api_key: str | None = None,
    sort: str = "alpha",
    category: str | None = None,
    refresh: bool = False,
    timeout: int = 30,
) -> list[str]:
    """Return the current Google Fonts family list.

    The official Google Fonts Developer API requires an API key. If a key is
    missing or the request fails, use the locally cached list first, then the
    bundled fallback list.
    """
    api_key = (api_key or GOOGLE_FONTS_API_KEY or "").strip()
    if not refresh:
        cached = _load_cached_google_font_families()
        if cached and not api_key:
            return cached

    if api_key:
        query = {"key": api_key, "sort": sort or "alpha"}
        if category:
            query["category"] = category
        url = GOOGLE_FONTS_API_URL + "?" + urllib.parse.urlencode(query)
        try:
            payload = json.loads(_http_get(url, timeout=timeout).decode("utf-8"))
            families = [
                str(item.get("family", "")).strip()
                for item in payload.get("items", [])
                if isinstance(item, dict) and item.get("family")
            ]
            families = _normalize_font_families(families)
            if families:
                PRIMARY_FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                GOOGLE_FONTS_CACHE_PATH.write_text(
                    json.dumps({"families": families, "sort": sort, "category": category}, indent=2),
                    encoding="utf-8",
                )
                return families
        except (OSError, urllib.error.URLError, RuntimeError, json.JSONDecodeError) as exc:
            print(f"warning: Google Fonts API fetch failed, using cached/bundled fonts: {exc}", file=sys.stderr)

    cached = _load_cached_google_font_families()
    return cached or CANVA_FONT_FAMILIES[:]


__all__ = ["fetch_google_font_families"]
