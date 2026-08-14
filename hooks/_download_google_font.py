"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _download_google_font(family: str, bold: bool = False, italic: bool = False) -> Path | None:
    global _google_font_network_ok
    if not _google_font_network_ok:
        return None

    family_key = re.sub(r"[^a-zA-Z0-9]+", "_", family).strip("_").lower() or "font"
    variants = []
    if bold and italic:
        variants.extend(["700italic", "italic", "700", "regular"])
    elif bold:
        variants.extend(["700", "regular"])
    elif italic:
        variants.extend(["italic", "regular"])
    else:
        variants.append("regular")

    for variant in variants:
        cache_path = PRIMARY_FONT_CACHE_DIR / f"{family_key}__{variant}.ttf"
        if cache_path.exists():
            return cache_path
        missing_path = cache_path.with_suffix(".missing")
        if missing_path.exists():
            continue

        query = family if variant == "regular" else f"{family}:{variant}"
        css_url = "https://fonts.googleapis.com/css?family=" + urllib.parse.quote(query)
        try:
            css = _http_get(css_url, timeout=8, headers={"User-Agent": GOOGLE_FONT_UA}).decode("utf-8", "ignore")
            match = GOOGLE_FONT_URL_RE.search(css)
            if not match:
                PRIMARY_FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                missing_path.touch()
                continue
            font_bytes = _http_get(match.group(1), timeout=15, headers={"User-Agent": GOOGLE_FONT_UA})
            PRIMARY_FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(font_bytes)
            return cache_path
        except urllib.error.HTTPError as exc:
            if exc.code in {400, 404}:
                PRIMARY_FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                missing_path.touch()
                continue
            print(f"warning: couldn't download Google font {family!r} ({variant}): {exc}", file=sys.stderr)
            return None
        except urllib.error.URLError as exc:
            print(f"warning: couldn't download Google font {family!r} ({variant}): {exc}", file=sys.stderr)
            _google_font_network_ok = False
            return None
        except OSError as exc:
            print(f"warning: couldn't download Google font {family!r} ({variant}): {exc}", file=sys.stderr)
            return None
    return None


__all__ = ["_download_google_font"]
