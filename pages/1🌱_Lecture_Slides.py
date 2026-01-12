# ------------------------------------------------------------
# Lecture Slide Player (Multipage-ready) with Sharp Thumbnails
# - supports suffix slides like 013a.png when 013.png is missing
# ------------------------------------------------------------
import re
import io
import math
import requests
from PIL import Image
import streamlit as st

# ---------------- Page setup ----------------
st.set_page_config(page_title="Lecture Slide Player - Workshop", layout="wide")

# ------------ CONFIG ------------
GITHUB_OWNER  = "MK316"
GITHUB_REPO   = "gnu260112"
GITHUB_BRANCH = "main"
FOLDER_PATH   = "slides"

FILENAME_PREFIX = "260112."
FILENAME_EXT    = ".png"
START_INDEX     = 1
END_INDEX       = 21

# If a numbered slide is missing (e.g., 013.png), try these suffixes in order.
# Put "a" first since you deleted 013.png and only keep 013a.png.
SUFFIX_TRY_ORDER = ["a", ""]  # tries 013a.png then 013.png (keep "" if you might restore later)
# If you also use b/c: ["a","b","c",""]

THUMBS_PER_PAGE = 12
THUMB_COLS      = 6
THUMB_MAX_W     = 280
TIMEOUT         = 8

RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{FOLDER_PATH}"


def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def _get(url: str) -> bytes:
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r.content


@st.cache_data(show_spinner=False, ttl=3600)
def url_exists(url: str) -> bool:
    try:
        r = requests.get(url, stream=True, timeout=TIMEOUT)
        ok = r.status_code == 200
        r.close()
        return ok
    except Exception:
        return False


@st.cache_data(show_spinner=False, ttl=3600)
def discover_slides(raw_base: str, prefix: str, ext: str, start_i: int, end_i: int, suffix_order: list[str]):
    """
    Discover slides in strict numeric order:
      For each number i, choose the FIRST existing candidate among:
        prefix + i(3digits) + suffix + ext

    This allows 013a.png to act as the 13th slide when 013.png is deleted.
    """
    urls = []
    names = []

    for i in range(start_i, end_i + 1):
        num = f"{i:03d}"

        chosen = None
        chosen_name = None

        for suf in suffix_order:
            name = f"{prefix}{num}{suf}{ext}"
            url = f"{raw_base}/{name}"
            if url_exists(url):
                chosen = url
                chosen_name = name
                break

        if chosen:
            urls.append(chosen)
            names.append(chosen_name)
        else:
            # if a slide is missing, we still continue (you can change to st.error if you want strict)
            # This is useful if you intentionally have gaps.
            pass

    # Already in numeric order due to the loop; no need to sort
    return urls, names


@st.cache_data(show_spinner=False, ttl=3600)
def get_thumb_bytes(url: str, max_w: int = THUMB_MAX_W) -> bytes:
    raw = _get(url)
    im = Image.open(io.BytesIO(raw)).convert("RGBA")

    w, h = im.size
    if w > max_w:
        new_h = int(h * (max_w / w))
        im = im.resize((max_w, new_h), Image.LANCZOS)

    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[-1])
    im = bg

    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=92, method=6)
    return buf.getvalue()


# ---------- Discover slides ----------
slides, filenames = discover_slides(
    RAW_BASE,
    FILENAME_PREFIX,
    FILENAME_EXT,
    START_INDEX,
    END_INDEX,
    SUFFIX_TRY_ORDER
)

if not slides:
    st.error("⚠️ No slide images found in the folder.")
    st.stop()

# ---- Session state init ----
st.session_state.setdefault("slide_idx", 0)
st.session_state.setdefault("thumb_page", 1)
st.session_state.setdefault("fit_to_height", True)
st.session_state.setdefault("vh_percent", 88)
st.session_state.setdefault("display_width_px", 1000)
st.session_state.setdefault("thumbs_cache", {})  # url -> bytes


# --- Navigation callbacks ---
def go_prev():
    st.session_state.slide_idx = (st.session_state.slide_idx - 1) % len(slides)

def go_next():
    st.session_state.slide_idx = (st.session_state.slide_idx + 1) % len(slides)

def go_to_slide():
    num = st.session_state.slide_input
    if 1 <= num <= len(slides):
        st.session_state.slide_idx = num - 1

def go_first():
    st.session_state.slide_idx = 0
    st.session_state.slide_input = 1


# ===== Sidebar =====
with st.sidebar:
    st.subheader("Controls")

    st.markdown(
        f"<div style='text-align:right; font-weight:700; font-size:16px;'>"
        f"{st.session_state.slide_idx + 1} / {len(slides)}"
        f"</div>",
        unsafe_allow_html=True
    )

    st.toggle("Fit main slide to screen height", key="fit_to_height")
    if st.session_state.fit_to_height:
        st.slider("Height % of screen", 60, 95, key="vh_percent")
    else:
        st.slider("Slide width (px)", 700, 1400, key="display_width_px")

    st.number_input(
        "Go to Slide #",
        min_value=1,
        max_value=len(slides),
        step=1,
        key="slide_input",
        on_change=go_to_slide
    )

    st.button("⏮️ Go to Start (Slide 1)", use_container_width=True, on_click=go_first)


# ===== Main Slide =====
idx = st.session_state.slide_idx

if st.session_state.fit_to_height:
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center;">
            <img
                src="{slides[idx]}"
                alt="Slide {idx + 1}"
                style="
                    max-height: {st.session_state.vh_percent}vh;
                    width: auto;
                    height: auto;
                    object-fit: contain;
                    border: 1px solid #ccc;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
                "
            />
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.image(
        slides[idx],
        width=st.session_state.display_width_px,
        use_container_width=False
    )

st.caption(f"Slide {idx + 1} / {len(slides)}   ·   File: {filenames[idx]}")


# ===== Thumbnails =====
with st.expander("📑 Thumbnails", expanded=False):
    total = len(slides)
    pages = max(1, math.ceil(total / THUMBS_PER_PAGE))

    cols_top = st.columns(3)
    with cols_top[0]:
        st.caption(f"Total slides: {total}")
    with cols_top[1]:
        st.number_input("Thumbnail page", min_value=1, max_value=pages, step=1, key="thumb_page")
    with cols_top[2]:
        st.caption(f"Page size: {THUMBS_PER_PAGE}")

    start = (st.session_state.thumb_page - 1) * THUMBS_PER_PAGE
    end = min(start + THUMBS_PER_PAGE, total)
    page_urls = slides[start:end]

    cols = st.columns(min(THUMB_COLS, THUMBS_PER_PAGE), gap="small")

    for local_i, url in enumerate(page_urls):
        global_idx = start + local_i
        col = cols[local_i % len(cols)]

        with col:
            if url not in st.session_state.thumbs_cache:
                st.session_state.thumbs_cache[url] = get_thumb_bytes(url)

            if st.button(f"{global_idx + 1}", key=f"thumb_btn_{global_idx}", use_container_width=True):
                st.session_state.slide_idx = global_idx
                st.rerun()

            st.image(st.session_state.thumbs_cache[url], width=150)
