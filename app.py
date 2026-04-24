import streamlit as st
import time
import sys
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root & Background ── */
:root {
    --bg:         #080c14;
    --surface:    #0d1420;
    --surface2:   #121a2a;
    --border:     #1e2d45;
    --accent:     #00d4ff;
    --accent2:    #7b61ff;
    --accent3:    #00ff9d;
    --text:       #e2eaf5;
    --muted:      #5a7090;
    --danger:     #ff4d6d;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 40% at 20% 0%, rgba(0,212,255,.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 80% 100%, rgba(123,97,255,.07) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Main container ── */
.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1200px !important;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    border: 1px solid rgba(0,212,255,.25);
    background: rgba(0,212,255,.06);
    padding: 0.3rem 0.9rem;
    border-radius: 2px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2.8rem, 5vw, 4.2rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    line-height: 1.05 !important;
    margin: 0 !important;
    background: linear-gradient(135deg, #e2eaf5 0%, var(--accent) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.9rem;
    letter-spacing: 0.05em;
}

/* ── Agent pipeline strip ── */
.pipeline-strip {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2.5rem 0 2rem;
    flex-wrap: wrap;
    row-gap: 0.5rem;
}
.pipe-node {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 1rem;
    border: 1px solid var(--border);
    background: var(--surface);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    transition: all .25s;
    position: relative;
    white-space: nowrap;
}
.pipe-node.active {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(0,212,255,.07);
    box-shadow: 0 0 18px rgba(0,212,255,.15);
}
.pipe-node.done {
    border-color: var(--accent3);
    color: var(--accent3);
    background: rgba(0,255,157,.05);
}
.pipe-node .icon { font-size: 1rem; }
.pipe-arrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--border);
    padding: 0 0.2rem;
}

/* ── Input card ── */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] input {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color .2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,.1) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; }

/* ── Button ── */
[data-testid="stButton"] > button,
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #00d4ff18 0%, #7b61ff30 100%) !important;
    border: 1px solid #00d4ff55 !important;
    color: #00d4ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.68rem 1.8rem !important;
    border-radius: 3px !important;
    transition: all .3s cubic-bezier(.4,0,.2,1) !important;
    cursor: pointer !important;
    box-shadow: 0 0 20px rgba(0,212,255,.12), inset 0 1px 0 rgba(255,255,255,.05) !important;
    text-shadow: 0 0 12px rgba(0,212,255,.6) !important;
}
[data-testid="stButton"] > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #00d4ff28 0%, #7b61ff45 100%) !important;
    border-color: #00d4ffaa !important;
    box-shadow: 0 0 30px rgba(0,212,255,.3), 0 0 60px rgba(123,97,255,.15), inset 0 1px 0 rgba(255,255,255,.08) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
    text-shadow: 0 0 16px rgba(0,212,255,.9) !important;
}
[data-testid="stButton"] > button:active,
[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 0 14px rgba(0,212,255,.2) !important;
}

/* ── Result cards ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-bottom: 1.2rem;
    overflow: hidden;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1.2rem;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
}
.result-icon {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.result-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500;
}
.result-body {
    padding: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    color: #8baac8;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
}
.result-body::-webkit-scrollbar { width: 4px; }
.result-body::-webkit-scrollbar-track { background: transparent; }
.result-body::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* Final report gets special treatment */
.report-body {
    padding: 1.4rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    line-height: 1.8;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

/* Feedback card */
.feedback-body {
    padding: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    color: #a8c5a0;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Status / logs ── */
.log-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    padding: 0.2rem 0;
    border-left: 2px solid var(--border);
    padding-left: 0.75rem;
    margin: 0.2rem 0;
}
.log-line.ok  { color: var(--accent3); border-color: var(--accent3); }
.log-line.run { color: var(--accent);  border-color: var(--accent); }
.log-line.err { color: var(--danger);  border-color: var(--danger); }

/* ── Metrics row ── */
.metrics-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.metric-box {
    flex: 1;
    min-width: 130px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val {
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.metric-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, rgba(0,212,255,.12), rgba(123,97,255,.18)) !important;
    border: 1px solid transparent !important;
    border-image: linear-gradient(135deg, #00d4ff, #7b61ff) 1 !important;
    color: #e2eaf5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2.2rem !important;
    border-radius: 3px !important;
    transition: all .25s ease !important;
    box-shadow: 0 0 22px rgba(0,212,255,.08), inset 0 0 12px rgba(123,97,255,.06) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,.22), rgba(123,97,255,.28)) !important;
    box-shadow: 0 0 32px rgba(0,212,255,.22), 0 0 18px rgba(123,97,255,.18) !important;
    transform: translateY(-1px) !important;
}

/* ── Streamlit expander overrides ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--muted) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 2px !important;
}
[data-testid="stProgress"] > div {
    background: var(--surface2) !important;
    border-radius: 2px !important;
    height: 3px !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Toast / info box ── */
[data-testid="stInfo"] {
    background: rgba(0,212,255,.06) !important;
    border: 1px solid rgba(0,212,255,.2) !important;
    border-radius: 4px !important;
    color: var(--accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}
[data-testid="stSuccess"] {
    background: rgba(0,255,157,.06) !important;
    border: 1px solid rgba(0,255,157,.2) !important;
    border-radius: 4px !important;
    color: var(--accent3) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}
[data-testid="stError"] {
    background: rgba(255,77,109,.06) !important;
    border: 1px solid rgba(255,77,109,.2) !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a result card ──────────────────────────────────────────────
def result_card(icon, title, color, content, body_class="result-body"):
    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <div class="result-icon" style="background:rgba({color},.12);color:rgb({color});">{icon}</div>
            <span class="result-title" style="color:rgb({color});">{title}</span>
        </div>
        <div class="{body_class}">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⬡ Multi-Agent System · v1.0</div>
    <h1>ResearchMind</h1>
    <p class="hero-sub">Search Agent → Reader Agent → Writer Chain → Critic Chain</p>
</div>
""", unsafe_allow_html=True)


# ── Pipeline strip ─────────────────────────────────────────────────────────────
def pipeline_strip(active_step=None, done_steps=None):
    done_steps = done_steps or []
    steps = [
        ("🔍", "Search Agent"),
        ("📄", "Reader Agent"),
        ("✍️", "Writer Chain"),
        ("🔎", "Critic Chain"),
    ]
    html = '<div class="pipeline-strip">'
    for i, (icon, label) in enumerate(steps):
        cls = "pipe-node"
        if i in done_steps:
            cls += " done"
        elif i == active_step:
            cls += " active"
        html += f'<div class="{cls}"><span class="icon">{icon}</span>{label}</div>'
        if i < len(steps) - 1:
            html += '<span class="pipe-arrow">──▶</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False
if "results" not in st.session_state:
    st.session_state.results = {}
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0


# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">// Research Topic</div>', unsafe_allow_html=True)

with st.form(key="research_form", clear_on_submit=False):
    col1, col2 = st.columns([5, 1], gap="small")
    with col1:
        topic = st.text_input(
            label="topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025 ...",
            label_visibility="collapsed",
            key="topic_input",
        )
    with col2:
        st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)
        run_btn = st.form_submit_button("▶ RUN", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ── Pipeline execution ──────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.error("Please enter a research topic first.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.results = {}

        # Import pipeline
        try:
            # Add the directory containing pipeline.py to path if needed
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from pipeline import run_research_pipeline
        except ImportError as e:
            st.error(f"Could not import pipeline: {e}")
            st.stop()

        progress_ph  = st.empty()
        strip_ph     = st.empty()
        status_ph    = st.empty()
        log_ph       = st.empty()

        def log(msg, kind="info"):
            cls = {"info": "", "ok": "ok", "run": "run", "err": "err"}.get(kind, "")
            log_ph.markdown(f'<div class="log-line {cls}">{msg}</div>', unsafe_allow_html=True)

        start = time.time()

        # ── We monkey-patch pipeline internals to capture step outputs live ──
        # Run the full pipeline; capture intermediate states via stdout redirect

        import io
        from contextlib import redirect_stdout

        step_map    = {}
        done_steps  = []

        # Step 1: search
        strip_ph.markdown(pipeline_strip.__doc__ or "")  # placeholder
        with strip_ph:
            pipeline_strip(active_step=0, done_steps=[])
        progress_ph.progress(0.05)
        log("🔍 Search Agent initialising...", "run")

        try:
            # Run step by step using the same helpers from pipeline
            from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

            # ── STEP 1: Search ──────────────────────────────────────────────
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            step_map["search_results"] = search_result["messages"][-1].content
            done_steps.append(0)
            progress_ph.progress(0.28)
            with strip_ph:
                pipeline_strip(active_step=1, done_steps=done_steps)
            log("✅ Search Agent complete", "ok")

            # ── STEP 2: Reader ──────────────────────────────────────────────
            log("📄 Reader Agent scraping top URL...", "run")
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{step_map['search_results'][:800]}"
                )]
            })
            step_map["scraped_content"] = reader_result["messages"][-1].content
            done_steps.append(1)
            progress_ph.progress(0.52)
            with strip_ph:
                pipeline_strip(active_step=2, done_steps=done_steps)
            log("✅ Reader Agent complete", "ok")

            # ── STEP 3: Writer ──────────────────────────────────────────────
            log("✍️ Writer Chain drafting report...", "run")
            research_combined = (
                f"SEARCH RESULTS:\n{step_map['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{step_map['scraped_content']}"
            )
            step_map["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined,
            })
            done_steps.append(2)
            progress_ph.progress(0.76)
            with strip_ph:
                pipeline_strip(active_step=3, done_steps=done_steps)
            log("✅ Writer Chain complete", "ok")

            # ── STEP 4: Critic ──────────────────────────────────────────────
            log("🔎 Critic reviewing report...", "run")
            step_map["feedback"] = critic_chain.invoke({"report": step_map["report"]})
            done_steps.append(3)
            progress_ph.progress(1.0)
            with strip_ph:
                pipeline_strip(active_step=None, done_steps=done_steps)
            log("✅ All agents complete", "ok")

            st.session_state.results  = step_map
            st.session_state.elapsed  = round(time.time() - start, 1)
            st.session_state.pipeline_done = True
            time.sleep(0.3)
            st.rerun()

        except Exception as exc:
            log(f"❌ Error: {exc}", "err")
            st.error(f"Pipeline error: {exc}")


# ── Results display ─────────────────────────────────────────────────────────────
if st.session_state.pipeline_done and st.session_state.results:
    res = st.session_state.results

    pipeline_strip(active_step=None, done_steps=[0, 1, 2, 3])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Metrics
    report_str   = str(res.get("report", ""))
    scraped_str  = str(res.get("scraped_content", ""))
    search_str   = str(res.get("search_results", ""))
    word_count   = len(report_str.split())
    src_count    = report_str.lower().count("http") + search_str.lower().count("http")

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-box">
            <div class="metric-val">4</div>
            <div class="metric-lbl">Agents Run</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{st.session_state.elapsed}s</div>
            <div class="metric-lbl">Total Time</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{word_count:,}</div>
            <div class="metric-lbl">Report Words</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{max(src_count, 1)}+</div>
            <div class="metric-lbl">Sources Found</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Final Report (hero card) ───────────────────────────────────────────
    st.markdown("""
    <div class="result-card" style="border-color:#7b61ff55;margin-bottom:1.2rem;">
        <div class="result-header" style="background:#0f1528;">
            <div class="result-icon" style="background:rgba(123,97,255,.15);color:#7b61ff;font-size:1rem;">📝</div>
            <span class="result-title" style="color:#7b61ff;">Final Research Report</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        f'<div class="report-body" style="background:#0d1420;border:1px solid #1e2d45;'
        f'border-top:none;border-radius:0 0 4px 4px;padding:1.6rem;'
        f'font-family:\'Syne\',sans-serif;font-size:.88rem;line-height:1.85;'
        f'color:#e2eaf5;white-space:pre-wrap;word-break:break-word;">'
        f'{report_str}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── Critic Feedback ────────────────────────────────────────────────────
    result_card(
        "🔎", "Critic Chain — Quality Review",
        "0,255,157",
        str(res.get("feedback", "")),
        "feedback-body",
    )

    # ── Expandable raw outputs ─────────────────────────────────────────────
    with st.expander("🔍 Raw Search Results"):
        st.markdown(
            f'<div class="result-body" style="max-height:260px;">'
            f'{search_str}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("📄 Scraped Web Content"):
        st.markdown(
            f'<div class="result-body" style="max-height:260px;">'
            f'{scraped_str}</div>',
            unsafe_allow_html=True,
        )

    # ── Download button ────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    full_output = (
        f"RESEARCH REPORT — {st.session_state.get('topic_input', 'Topic')}\n"
        f"{'='*60}\n\n"
        f"{report_str}\n\n"
        f"{'='*60}\n"
        f"CRITIC FEEDBACK\n"
        f"{'='*60}\n\n"
        f"{res.get('feedback','')}\n"
    )
    st.download_button(
        label="⬇ DOWNLOAD REPORT (.txt)",
        data=full_output,
        file_name=f"research_report.txt",
        mime="text/plain",
    )

elif not st.session_state.pipeline_done:
    # Idle state hint
    pipeline_strip()
    st.markdown("""
    <div style="text-align:center;padding:3rem 0 2rem;color:#2a4060;
                font-family:'JetBrains Mono',monospace;font-size:0.75rem;
                letter-spacing:0.1em;">
        ENTER A TOPIC ABOVE AND PRESS RUN TO START THE PIPELINE
    </div>
    """, unsafe_allow_html=True)