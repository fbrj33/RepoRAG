import base64
import os
import requests
import streamlit as st


# ============================================================
# CONFIG  (unchanged)
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RepoRAG",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COLORS  (cream base + coral/terracotta accent, matching mock)
# ============================================================

BG = "#FBF5F1"
SIDEBAR = "#F6ECE4"
CARD = "#FFFFFF"
BORDER = "#EAD9CE"
TEXT = "#241F1B"
MUTED = "#96897C"

ORANGE = "#3E55BD"
ORANGE_LIGHT = "#D1D8F6"
ORANGE_DARK = "#1C367E"

GREEN = "#1D3557"
GREEN_LIGHT = "#E4ECF5"

LAVENDER = "#E7E2F7"
LAVENDER_TEXT = "#5B4E9E"
MINT = "#DCEEE4"
MINT_TEXT = "#276749"


# ============================================================
# HTML HELPER  (unchanged)
# ============================================================

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")


def get_logo_base64():
    """Read the logo image from disk and return a base64 data URI."""
    if not os.path.exists(LOGO_PATH):
        return None
    with open(LOGO_PATH, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{encoded}"


def render_html(html):
    """
    Render HTML safely.

    Streamlit's markdown parser treats any line that begins with
    4+ spaces as an indented code block. textwrap.dedent() only
    strips a *common* leading-whitespace prefix, which breaks as
    soon as an f-string interpolates a value on its own line — so
    stray 4-space-indented lines survive and get rendered as raw
    text. Stripping every line individually is the reliable fix.
    """
    lines = [line.strip() for line in html.strip("\n").splitlines()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,500;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background: {BG} !important;
    min-height: 100vh;
}}

header[data-testid="stHeader"] {{
    background: transparent !important;
}}

[data-testid="stDecoration"] {{
    display: none;
}}

/* decorative blobs, bottom-right + top-left, behind everything */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: -180px;
    right: -160px;
    width: 520px;
    height: 520px;
    background: radial-gradient(circle at 30% 30%, {ORANGE_LIGHT} 0%, rgba(246,220,209,0) 70%);
    border-radius: 46% 54% 61% 39% / 40% 44% 56% 60%;
    z-index: 0;
    pointer-events: none;
}}

[data-testid="stAppViewContainer"]::after {{
    content: "";
    position: fixed;
    bottom: -220px;
    right: -140px;
    width: 620px;
    height: 620px;
    background: radial-gradient(circle at 60% 40%, {ORANGE_LIGHT} 0%, rgba(246,220,209,0) 72%);
    border-radius: 60% 40% 44% 56% / 50% 60% 40% 50%;
    z-index: 0;
    pointer-events: none;
}}

.stApp {{
    background: {BG};
    color: {TEXT};
    min-height: 100vh;
}}

.main .block-container {{
    max-width: 900px;
    padding-top: 1.2rem;
    padding-bottom: 6rem;
    position: relative;
    z-index: 1;
}}

* {{
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

h1, h2, h3, h4 {{
    font-family: "Source Serif 4", Georgia, serif !important;
    color: {TEXT} !important;
    font-weight: 600 !important;
}}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {{
    background: {SIDEBAR};
    border-right: 1px solid {BORDER};
}}

section[data-testid="stSidebar"] > div {{
    padding: 1.4rem 1.1rem;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 3px;
}}

.logo-symbol {{
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: {ORANGE_DARK};
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 17px;
    font-family: "Source Serif 4", serif;
}}

.logo-symbol-img {{
    width: 34px;
    height: 34px;
    object-fit: contain;
    flex-shrink: 0;
}}

.logo-text {{
    font-family: "Source Serif 4", serif;
    font-size: 20px;
    font-weight: 600;
    color: {TEXT};
}}

.logo-subtitle {{
    margin-left: 44px;
    color: {MUTED};
    font-size: 11px;
    margin-bottom: 20px;
}}

/* decorative nav menu */
.nav-menu {{
    margin: 14px 0 22px 0;
}}

.nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    border-radius: 10px;
    color: {MUTED};
    font-size: 13.5px;
    font-weight: 600;
    margin-bottom: 3px;
}}

.nav-item .nav-icon {{
    width: 16px;
    text-align: center;
    color: inherit;
}}

.nav-item.active {{
    background: {ORANGE_LIGHT};
    color: {ORANGE_DARK};
}}

.sidebar-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    color: {MUTED};
    margin: 18px 0 8px 2px;
    text-transform: uppercase;
}}

.repo-form-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 14px 14px 6px 14px;
}}

.repo-form-card-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12.5px;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 10px;
}}

.repo-sidebar-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px;
    margin-top: 10px;
}}

.repo-sidebar-name {{
    font-size: 13px;
    font-weight: 600;
    color: {TEXT};
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.repo-sidebar-url {{
    font-size: 10px;
    color: {MUTED};
    margin-top: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.indexed {{
    display: inline-block;
    margin-top: 9px;
    padding: 3px 9px;
    border-radius: 20px;
    background: {GREEN_LIGHT};
    color: {GREEN};
    font-size: 10px;
    font-weight: 650;
}}

.status-online {{
    color: {GREEN};
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.status-offline {{
    color: {ORANGE_DARK};
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.pipeline-list {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-top: 4px;
}}

.pipeline-item {{
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 11.5px;
    color: {TEXT};
    padding: 3px 0;
}}

.pipeline-num {{
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    border-radius: 6px;
    background: {ORANGE_LIGHT};
    color: {ORANGE_DARK};
    font-size: 9.5px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}}


/* ==========================================================
   TOP BAR  (status pill, top-right)
   ========================================================== */

.topbar {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-bottom: 6px;
    margin-bottom: 6px;
}}

.api-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: {CARD};
    border: 1px solid {BORDER};
    padding: 6px 13px;
    border-radius: 20px;
    color: {MUTED};
    font-size: 11.5px;
    font-weight: 600;
}}

.online-dot {{
    width: 7px;
    height: 7px;
    background: {GREEN};
    border-radius: 50%;
}}

.offline-dot {{
    width: 7px;
    height: 7px;
    background: {ORANGE};
    border-radius: 50%;
}}


/* ==========================================================
   WELCOME / HERO
   ========================================================== */

.hero {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
    padding: 10px 0 6px;
}}

.hero-left {{
    flex: 1;
    min-width: 0;
}}

.badge-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: {CARD};
    border: 1px solid {BORDER};
    padding: 7px 15px;
    border-radius: 20px;
    color: {TEXT};
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 22px;
}}

.hero-title {{
    font-family: "Source Serif 4", serif;
    font-size: 44px;
    line-height: 1.15;
    font-weight: 600;
    letter-spacing: -0.5px;
    color: {TEXT};
    margin-bottom: 16px;
}}

.hero-title .accent {{
    color: {ORANGE};
    font-style: italic;
}}

.hero-description {{
    max-width: 480px;
    color: {MUTED};
    font-size: 14.5px;
    line-height: 1.7;
}}

.hero-graphic {{
    flex-shrink: 0;
    width: 230px;
    height: 230px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.hero-graphic-ring {{
    position: absolute;
    width: 210px;
    height: 130px;
    border: 1.5px solid {ORANGE_LIGHT};
    border-radius: 50%;
    transform: rotate(-18deg);
}}

.hero-graphic-letter {{
    font-family: "Source Serif 4", serif;
    font-size: 150px;
    font-weight: 700;
    color: {ORANGE};
    opacity: 0.9;
}}

.hero-graphic-img {{
    width: 170px;
    height: 170px;
    object-fit: contain;
}}

.hero-sparkle {{
    position: absolute;
    color: {ORANGE};
    font-size: 20px;
}}

.hero-sparkle.s1 {{ top: 6px; right: 18px; font-size: 26px; }}
.hero-sparkle.s2 {{ bottom: 30px; left: 6px; font-size: 14px; }}


/* ==========================================================
   EXAMPLE CARDS
   ========================================================== */

.example-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 18px 16px;
    margin-bottom: 10px;
    height: 148px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: border-color 0.15s ease, transform 0.15s ease;
}}

.example-card:hover {{
    border-color: {ORANGE};
    transform: translateY(-1px);
}}

.example-icon {{
    width: 38px;
    height: 38px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    margin-bottom: 12px;
}}

.example-title {{
    font-size: 13.5px;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 4px;
}}

.example-question {{
    font-size: 12px;
    color: {MUTED};
    line-height: 1.4;
}}

.example-arrow {{
    color: {ORANGE};
    font-size: 15px;
    margin-top: 8px;
}}


/* ==========================================================
   ACTIVE REPOSITORY CARDS
   ========================================================== */

.repo-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 22px;
}}

.repo-card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.repo-title {{
    font-size: 15px;
    font-weight: 650;
    color: {TEXT};
}}

.repo-url {{
    font-size: 11px;
    color: {MUTED};
    margin-top: 3px;
}}

.repo-ready {{
    background: {GREEN_LIGHT};
    color: {GREEN};
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
}}


/* ==========================================================
   METRICS
   ========================================================== */

.metric {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 11px 14px;
}}

.metric-number {{
    font-family: "Source Serif 4", serif;
    font-size: 19px;
    font-weight: 600;
    color: {TEXT};
}}

.metric-label {{
    color: {MUTED};
    font-size: 10px;
    margin-top: 2px;
}}


/* ==========================================================
   CHAT
   ========================================================== */

.user-message {{
    display: flex;
    justify-content: flex-end;
    margin: 22px 0 20px;
}}

.user-bubble {{
    max-width: 75%;
    background: {ORANGE};
    color: white;
    padding: 12px 17px;
    border-radius: 18px 18px 4px 18px;
    font-size: 14.5px;
    line-height: 1.55;
}}

.assistant-row {{
    display: flex;
    gap: 12px;
    margin-bottom: 30px;
}}

.assistant-avatar {{
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: {GREEN_LIGHT};
    color: {GREEN};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    font-family: "Source Serif 4", serif;
}}

.assistant-content {{
    flex: 1;
    min-width: 0;
}}

.assistant-name {{
    font-size: 12px;
    font-weight: 650;
    color: {MUTED};
    margin-bottom: 8px;
}}

.answer-box {{
    color: {TEXT};
    font-size: 14.5px;
    line-height: 1.75;
}}


/* ==========================================================
   SOURCES
   ========================================================== */

.sources-heading {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: {MUTED};
    margin: 4px 0 9px 42px;
}}

.source {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-left: 3px solid {GREEN};
    border-radius: 8px;
    padding: 11px 13px;
    margin: 0 0 7px 42px;
}}

.source-file {{
    color: {ORANGE_DARK};
    font-size: 12px;
    font-weight: 650;
}}

.source-info {{
    color: {MUTED};
    font-size: 10px;
    margin-top: 4px;
}}


/* ==========================================================
   INPUT
   ========================================================== */

.input-label {{
    color: {TEXT};
    font-size: 12px;
    font-weight: 650;
    margin-bottom: 7px;
}}

.input-hint {{
    color: {MUTED};
    font-size: 10px;
    margin-top: 5px;
}}

.stTextArea textarea,
.stTextInput input {{
    background: {CARD} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 14px !important;
}}

.stTextArea textarea:focus,
.stTextInput input:focus {{
    border-color: {ORANGE} !important;
    box-shadow: 0 0 0 1px {ORANGE} !important;
}}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {{
    border-radius: 10px;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid {BORDER};
    background: {CARD};
    color: {TEXT};
}}

.stButton > button:hover {{
    border-color: {ORANGE};
    color: {ORANGE_DARK};
    background: {ORANGE_LIGHT};
}}

section[data-testid="stSidebar"] div[data-testid="stButton"] button {{
    background: {ORANGE};
    color: white;
    border: none;
}}

section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
    background: {ORANGE_DARK};
    color: white;
}}


/* ==========================================================
   EXPANDER
   ========================================================== */

div[data-testid="stExpander"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {{
    text-align: center;
    color: {MUTED};
    font-size: 10px;
    margin-top: 50px;
    padding-top: 18px;
    border-top: 1px solid {BORDER};
    max-width: 220px;
    margin-left: auto;
    margin-right: auto;
}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE  (unchanged)
# ============================================================

if "repository_id" not in st.session_state:
    st.session_state.repository_id = None

if "repository_url" not in st.session_state:
    st.session_state.repository_url = None

if "index_data" not in st.session_state:
    st.session_state.index_data = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# API  (unchanged backend calls)
# ============================================================

def check_api():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=3,
        )
        return response.status_code == 200

    except requests.RequestException:
        return False


def index_repository(repo_url):
    try:
        response = requests.post(
            f"{API_URL}/repositories/index",
            json={"repo_url": repo_url},
            timeout=300,
        )

        if response.status_code != 200:

            try:
                error = response.json().get(
                    "detail",
                    "Unknown error",
                )
            except Exception:
                error = response.text

            st.error(error)
            return None

        return response.json()

    except requests.RequestException as exc:

        st.error(
            f"Could not connect to FastAPI: {exc}"
        )

        return None


def ask_repository(repository_id, question):
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={
                "repository_id": repository_id,
                "question": question,
            },
            timeout=300,
        )

        if response.status_code != 200:

            try:
                error = response.json().get(
                    "detail",
                    "Unknown error",
                )
            except Exception:
                error = response.text

            st.error(error)
            return None

        return response.json()

    except requests.RequestException as exc:

        st.error(
            f"Could not connect to FastAPI: {exc}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    logo_data_uri = get_logo_base64()

    if logo_data_uri:
        logo_symbol_html = f'<img src="{logo_data_uri}" class="logo-symbol-img" />'
    else:
        logo_symbol_html = '<div class="logo-symbol">R</div>'

    render_html(
        f"""
        <div class="logo">
            {logo_symbol_html}
            <div class="logo-text">RepoRAG</div>
        </div>
        <div class="logo-subtitle">Codebase intelligence</div>
        """
    )

    # decorative nav menu
    

    

    repo_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/owner/repo",
        label_visibility="collapsed",
    )

    connect_clicked = st.button(
        "  Connect repository",
        use_container_width=True,
    )

    render_html("</div>")

    if connect_clicked:

        if not repo_url.strip():

            st.warning("Enter a repository URL.")

        else:

            with st.spinner("Cloning and indexing..."):

                result = index_repository(repo_url.strip())

            if result:

                st.session_state.repository_id = result["repository_id"]
                st.session_state.repository_url = result["repository_url"]
                st.session_state.index_data = result
                st.session_state.messages = []

                st.success("Repository ready.")


    # Active repository

    if st.session_state.index_data:

        data = st.session_state.index_data

        repo_name = data["repository_url"].rstrip("/").split("/")[-1]

        render_html('<div class="sidebar-label">Active repository</div>')

        render_html(
            f"""
            <div class="repo-sidebar-card">
                <div class="repo-sidebar-name">{repo_name}</div>
                <div class="repo-sidebar-url">{data["repository_url"]}</div>
                <div class="indexed">● Indexed</div>
            </div>
            """
        )

        render_html('<div class="sidebar-label">Index</div>')

        c1, c2 = st.columns(2)

        with c1:
            render_html(
                f"""
                <div class="metric">
                    <div class="metric-number">{data["files"]}</div>
                    <div class="metric-label">files</div>
                </div>
                """
            )

        with c2:
            render_html(
                f"""
                <div class="metric">
                    <div class="metric-number">{data["chunks"]}</div>
                    <div class="metric-label">chunks</div>
                </div>
                """
            )


    # Pipeline

    render_html('<div class="sidebar-label">Pipeline</div>')

    steps = [
        "Repository loader",
        "Code-aware splitting",
        "Semantic embeddings",
        "Chroma vector search",
        "BM25 keyword search",
        "Cross-encoder reranking",
        "Ollama generation",
    ]

    pipeline_html = '<div class="pipeline-list">'
    for i, step in enumerate(steps, start=1):
        pipeline_html += (
            f'<div class="pipeline-item">'
            f'<div class="pipeline-num">{i:02d}</div>'
            f'<div>{step}</div>'
            f'</div>'
        )
    pipeline_html += "</div>"

    render_html(pipeline_html)


    # System

    render_html('<div class="sidebar-label">System</div>')

    if check_api():
        render_html('<div class="status-online"><span class="online-dot"></span> FastAPI connected</div>')
    else:
        render_html('<div class="status-offline"><span class="offline-dot"></span> FastAPI offline</div>')


# ============================================================
# TOP BAR  (status pill, top-right only)
# ============================================================

api_online = check_api()

if api_online:
    status_html = '<span class="online-dot"></span> API connected'
else:
    status_html = '<span class="offline-dot"></span> API offline'

render_html(
    f"""
    <div class="topbar">
        <div class="api-pill">{status_html}</div>
    </div>
    """
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.repository_id:

    logo_data_uri = get_logo_base64()

    if logo_data_uri:
        hero_graphic_inner = f'<img src="{logo_data_uri}" class="hero-graphic-img" />'
    else:
        hero_graphic_inner = '<div class="hero-graphic-letter">R</div>'

    render_html(
        f"""
        <div class="hero">
            <div class="hero-left">
                <div class="badge-pill">✦ Repository Assistant</div>
                <div class="hero-title">What do you want to<br><span class="accent">know?</span></div>
                <div class="hero-description">
                    Connect a GitHub repository and ask questions about its
                    architecture, implementation, configuration, database,
                    authentication, and code.
                </div>
            </div>
            <div class="hero-graphic">
                <div class="hero-graphic-ring"></div>
                <span class="hero-sparkle s1">✦</span>
                <span class="hero-sparkle s2">✦</span>
                {hero_graphic_inner}
            </div>
        </div>
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    columns = st.columns(4)

    examples = [
        ("Understand", "How is the application structured?", "▤", ORANGE_LIGHT, ORANGE_DARK),
        ("Find", "Where is the database configured?", "⌕", "#FBE7CF", "#B5691E"),
        ("Explain", "How does get_db work?", "&lt;/&gt;", LAVENDER, LAVENDER_TEXT),
        ("Explore", "Ask anything about the codebase.", "💡", MINT, MINT_TEXT),
    ]

    for column, (title, question, icon, icon_bg, icon_color) in zip(columns, examples):

        with column:

            render_html(
                f"""
                <div class="example-card">
                    <div>
                        <div class="example-icon" style="background:{icon_bg};color:{icon_color};">{icon}</div>
                        <div class="example-title">{title}</div>
                        <div class="example-question">{question}</div>
                    </div>
                    <div class="example-arrow">→</div>
                </div>
                """
            )


# ============================================================
# ACTIVE REPOSITORY
# ============================================================

else:

    data = st.session_state.index_data

    repo_name = data["repository_url"].rstrip("/").split("/")[-1]


    # --------------------------------------------------------
    # Repository header
    # --------------------------------------------------------

    render_html(
        f"""
        <div class="repo-card">
            <div class="repo-card-header">
                <div>
                    <div class="repo-title">{repo_name}</div>
                    <div class="repo-url">{data["repository_url"]}</div>
                </div>
                <div class="repo-ready">Ready</div>
            </div>
        </div>
        """
    )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        render_html(
            f"""
            <div class="metric">
                <div class="metric-number">{data["files"]}</div>
                <div class="metric-label">files indexed</div>
            </div>
            """
        )

    with c2:
        render_html(
            f"""
            <div class="metric">
                <div class="metric-number">{data["chunks"]}</div>
                <div class="metric-label">code chunks</div>
            </div>
            """
        )

    with c3:
        render_html(
            """
            <div class="metric">
                <div class="metric-number">Hybrid</div>
                <div class="metric-label">retrieval</div>
            </div>
            """
        )


    # --------------------------------------------------------
    # Chat history
    # --------------------------------------------------------

    for message in st.session_state.messages:

        if message["role"] == "user":

            render_html(
                f"""
                <div class="user-message">
                    <div class="user-bubble">{message["content"]}</div>
                </div>
                """
            )

        else:

            result = message["result"]

            render_html(
                """
                <div class="assistant-row">
                    <div class="assistant-avatar">R</div>
                    <div class="assistant-content">
                        <div class="assistant-name">RepoRAG</div>
                        <div class="answer-box">
                """
            )

            st.markdown(result["answer"])

            render_html(
                """
                        </div>
                    </div>
                </div>
                """
            )

            sources = result.get("sources", [])

            if sources:

                render_html(
                    f'<div class="sources-heading">Sources · {len(sources)}</div>'
                )

                for source in sources:

                    file_path = source.get("file", "Unknown")
                    source_type = source.get("type", "unknown")
                    name = source.get("name") or "unnamed"
                    start = source.get("start_line", "?")
                    end = source.get("end_line", "?")

                    render_html(
                        f"""
                        <div class="source">
                            <div class="source-file">{file_path}</div>
                            <div class="source-info">
                                {source_type} · {name} · lines {start}–{end}
                            </div>
                        </div>
                        """
                    )


    # --------------------------------------------------------
    # Input area
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    render_html('<div class="input-label">Ask about your repository</div>')

    question = st.text_area(
        "Ask",
        placeholder="Ask RepoRAG anything about the codebase...",
        height=90,
        label_visibility="collapsed",
        key="question_input",
    )

    render_html(
        """
        <div class="input-hint">
            Semantic search + BM25 + cross-encoder reranking find the most
            relevant code before the LLM generates an answer.
        </div>
        """
    )

    send_col, clear_col = st.columns([5, 1])

    with send_col:
        ask_button = st.button("Send  →", use_container_width=True)

    with clear_col:
        clear_button = st.button("Clear", use_container_width=True)


    # --------------------------------------------------------
    # Clear chat
    # --------------------------------------------------------

    if clear_button:
        st.session_state.messages = []
        st.rerun()


    # --------------------------------------------------------
    # Ask
    # --------------------------------------------------------

    if ask_button:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            user_question = question.strip()

            with st.spinner("Searching the repository..."):

                result = ask_repository(
                    st.session_state.repository_id,
                    user_question,
                )

            if result:

                st.session_state.messages.append(
                    {"role": "user", "content": user_question}
                )

                st.session_state.messages.append(
                    {"role": "assistant", "result": result}
                )

                st.rerun()


    # --------------------------------------------------------
    # Retrieved context
    # --------------------------------------------------------

    if st.session_state.messages:

        last_result = None

        for message in reversed(st.session_state.messages):

            if message["role"] == "assistant":
                last_result = message["result"]
                break

        if last_result:

            context = last_result.get("context")

            if context:

                with st.expander("View retrieved context"):
                    st.code(context, language="text")


# ============================================================
# FOOTER
# ============================================================

render_html('<div class="footer">RepoRAG · AI-powered codebase understanding</div>')