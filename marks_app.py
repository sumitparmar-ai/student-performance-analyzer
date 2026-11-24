
"""
Student Marks Analyzer - Streamlit dashboard built on the NumPy logic of the original script.
Run with:  streamlit run marks_app.py
"""
 
import html
 
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
 
# ---------------------------------------------------------------- config
st.set_page_config(page_title="Marks Analyzer", page_icon="📊", layout="wide")
 
DEFAULT_STUDENTS = ["Rahul", "Aman", "Priya", "Rohit", "Sneha", "Karan", "Anjali", "Vikas", "Neha", "Arjun"]
SUBJECTS = ["Maths", "Science", "English", "Physics", "Chemistry"]
DEFAULT_MARKS = np.array([
    [89, 90, 88, 68, 76],
    [76, 88, 85, 46, 55],
    [80, 82, 90, 50, 60],
    [33, 45, 40, 20, 30],
    [32, 40, 35, 88, 25],
    [45, 50, 48, 25, 35],
    [40, 45, 42, 22, 32],
    [35, 40, 38, 18, 78],
    [30, 35, 32, 16, 24],
    [25, 30, 28, 14, 22],
])
 
BRAND, DANGER = "#4F46E5", "#DC2626"
 
 
def default_df() -> pd.DataFrame:
    return pd.DataFrame(DEFAULT_MARKS, index=DEFAULT_STUDENTS, columns=SUBJECTS)
 
 
# ---------------------------------------------------------------- icons (inline SVG)
def svg(path_d: str, color: str = "currentColor", size: int = 18) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f"{path_d}</svg>"
    )
 
 
I_CHART = '<path d="M3 3v18h18"/><path d="M7 16V9"/><path d="M12 16V5"/><path d="M17 16v-4"/>'
I_USERS = '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
I_CHECK = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/>'
I_TROPHY = '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>'
I_BOOK = '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'
I_PERCENT = '<line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>'
I_SUM = '<path d="M18 7V4H6l6 8-6 8h12v-3"/>'
I_MEDAL = '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>'
 
# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
 
:root {
    --bg: #F1F5F9; --card: #FFFFFF; --ink: #0F172A; --muted: #64748B;
    --line: #E2E8F0; --line-strong: #CBD5E1;
    --brand: #4F46E5; --brand-dark: #4338CA; --danger: #DC2626; --ok: #059669;
}
 
html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: var(--bg) !important; color: var(--ink) !important; }
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1160px; }
.stApp p, .stApp li, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: var(--ink); }
h1, h2, h3 { letter-spacing: -0.02em; font-weight: 700 !important; }
 
/* header */
.brand { display: flex; align-items: center; gap: 14px; margin-bottom: 1.2rem; }
.brand-mark { width: 46px; height: 46px; border-radius: 12px; background: var(--brand);
              display: flex; align-items: center; justify-content: center;
              box-shadow: 0 6px 16px rgba(79,70,229,.35); }
.brand h1 { font-size: 1.85rem; margin: 0; line-height: 1.1; color: var(--ink) !important; }
.brand p { margin: 2px 0 0 0; color: var(--muted) !important; font-size: .95rem; }
 
/* stat cards */
.stats { display: grid; grid-template-columns: repeat(var(--cols, 4), 1fr); gap: 14px; margin: .4rem 0 1.4rem 0; }
.stat { background: var(--card); border: 1px solid var(--line); border-radius: 14px;
        padding: 16px 18px; display: flex; align-items: center; gap: 14px; min-width: 0; }
.stat-ico { width: 42px; height: 42px; border-radius: 10px; background: #EEF2FF;
            display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-ico.green { background: #ECFDF5; }
.stat-ico.red { background: #FEF2F2; }
.stat-val { font-size: 1.3rem; font-weight: 700; color: var(--ink); line-height: 1.2;
            overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.stat-lbl { font-size: .82rem; color: var(--muted); }
@media (max-width: 900px) { .stats { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px) { .stats { grid-template-columns: 1fr; } }
 
/* sidebar */
section[data-testid="stSidebar"] { background: #0F172A !important; border-right: 0; }
section[data-testid="stSidebar"] * { color: #F8FAFC; }
.sb-head { display: flex; align-items: center; gap: 10px; margin: .3rem 0 1.1rem 0;
           font-weight: 700; font-size: 1.15rem; color: #F8FAFC; }
.sb-label { font-size: .78rem; font-weight: 600; letter-spacing: .04em; color: #94A3B8 !important;
            margin: 1rem 0 .5rem 0; }
.sb-row { display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 9px;
          background: rgba(255,255,255,.06); margin-bottom: 6px; }
.sb-rank { font-family: 'JetBrains Mono', monospace; font-size: .78rem; color: #A5B4FC !important; width: 26px; }
.sb-name { flex: 1; font-size: .9rem; font-weight: 500; color: #F8FAFC !important; }
.sb-pct { font-family: 'JetBrains Mono', monospace; font-size: .8rem; color: #CBD5E1 !important; }
.sb-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.sb-subj { display: inline-block; background: rgba(165,180,252,.16); color: #E0E7FF !important;
           border-radius: 999px; padding: 3px 10px; font-size: .78rem; margin: 0 6px 6px 0; }
 
/* tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; border-bottom: 0; margin-bottom: -1px; }
.stTabs [data-baseweb="tab"] { background: #E2E8F0; border-radius: 10px 10px 0 0; padding: 10px 22px; height: auto; }
.stTabs [data-baseweb="tab"] p { color: #475569 !important; font-weight: 600; font-size: .95rem; }
.stTabs [aria-selected="true"] { background: var(--card) !important; }
.stTabs [aria-selected="true"] p { color: var(--brand) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--brand) !important; height: 3px; }
.stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { background: var(--card); border: 1px solid var(--line);
    border-radius: 0 14px 14px 14px; padding: 1.6rem 1.8rem 1.8rem 1.8rem; }
.stTabs [data-baseweb="tab-panel"] h3 { margin-top: 0; font-size: 1.2rem; }
 
/* labels + inputs */
[data-testid="stWidgetLabel"] p { color: var(--ink) !important; font-weight: 600; font-size: .92rem; }
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div {
    background: #FFFFFF !important; border: 1px solid var(--line-strong) !important; border-radius: 10px !important; }
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
    border-color: var(--brand) !important; box-shadow: 0 0 0 3px rgba(79,70,229,.18) !important; }
.stNumberInput input, .stTextInput input { color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important; background: #FFFFFF !important; }
.stNumberInput button { background: #F1F5F9 !important; border: 0 !important; }
.stNumberInput button svg { fill: var(--ink) !important; color: var(--ink) !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: var(--ink) !important; }
div[data-baseweb="select"] svg { fill: var(--muted) !important; }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li, div[data-baseweb="menu"] {
    background: #FFFFFF !important; color: var(--ink) !important; }
div[data-baseweb="popover"] li:hover { background: #EEF2FF !important; }
 
/* buttons */
.stButton > button, .stDownloadButton > button {
    background: var(--brand) !important; border: 0 !important; border-radius: 10px !important;
    padding: .6rem 1.4rem !important; font-weight: 600 !important; }
.stButton > button *, .stDownloadButton > button * { color: #FFFFFF !important; }
.stButton > button:hover, .stDownloadButton > button:hover { background: var(--brand-dark) !important; }
 
/* topper cards */
.toppers { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-top: .6rem; }
.topper { border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; background: #F8FAFC; }
.topper-sub { font-size: .78rem; font-weight: 700; color: var(--brand) !important; letter-spacing: .03em; }
.topper-name { font-size: 1.1rem; font-weight: 700; margin: 4px 0 2px 0; color: var(--ink) !important; }
.topper-marks { font-size: .85rem; color: var(--muted) !important; }
 
/* chips / badges */
.chips { display: flex; gap: 8px; flex-wrap: wrap; margin: .2rem 0 1rem 0; }
.chip { background: #EEF2FF; color: #3730A3 !important; border-radius: 999px; padding: 4px 12px;
        font-size: .8rem; font-weight: 600; }
.chip.bad { background: #FEF2F2; color: #991B1B !important; }
.chip.good { background: #ECFDF5; color: #065F46 !important; }
.note { color: var(--muted) !important; font-size: .9rem; margin: -.2rem 0 1rem 0; }
</style>
""",
    unsafe_allow_html=True,
)
 
 
# ---------------------------------------------------------------- helpers
def stat_cards(cards, cols=4):
    """cards: list of (icon_path, value, label, tone) where tone is '', 'green' or 'red'."""
    colors = {"": "#4F46E5", "green": "#059669", "red": "#DC2626"}
    inner = "".join(
        f'<div class="stat"><div class="stat-ico {tone}">{svg(icon, colors[tone], 22)}</div>'
        f'<div style="min-width:0"><div class="stat-val">{html.escape(str(value))}</div>'
        f'<div class="stat-lbl">{html.escape(label)}</div></div></div>'
        for icon, value, label, tone in cards
    )
    st.markdown(f'<div class="stats" style="--cols:{cols}">{inner}</div>', unsafe_allow_html=True)
 
 
def chips(items, tone=""):
    inner = "".join(f'<span class="chip {tone}">{html.escape(i)}</span>' for i in items)
    st.markdown(f'<div class="chips">{inner}</div>', unsafe_allow_html=True)
 
 
def bar_chart(labels, values, rule, y_max, y_title, height=320):
    """Bar chart where bars below the pass line are red."""
    data = pd.DataFrame({"Label": labels, "Value": np.round(values, 2)})
    data["Status"] = np.where(data["Value"] >= rule, "At or above pass mark", "Below pass mark")
    bars = (
        alt.Chart(data)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Label:N", sort=None, title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Value:Q", scale=alt.Scale(domain=[0, y_max]), title=y_title),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(domain=["At or above pass mark", "Below pass mark"], range=[BRAND, DANGER]),
                legend=alt.Legend(orient="top", title=None),
            ),
            tooltip=["Label", "Value", "Status"],
        )
    )
    line = (
        alt.Chart(pd.DataFrame({"y": [rule]}))
        .mark_rule(strokeDash=[6, 4], color="#0F172A", strokeWidth=1.5)
        .encode(y="y:Q")
    )
    chart = (
        (bars + line)
        .properties(height=height, width="container")
        .configure_axis(labelColor="#334155", titleColor="#334155", gridColor="#E2E8F0", domainColor="#CBD5E1")
        .configure_legend(labelColor="#334155")
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(chart, theme=None)
 
 
# ---------------------------------------------------------------- state
if "df" not in st.session_state:
    st.session_state.df = default_df()
if "ver" not in st.session_state:
    st.session_state.ver = 0
 
df = st.session_state.df
 
# ---------------------------------------------------------------- header + settings
st.markdown(
    f"""
    <div class="brand">
        <div class="brand-mark">{svg(I_CHART, "#FFFFFF", 24)}</div>
        <div>
            <h1>Marks Analyzer</h1>
            <p>Student and subject performance, calculated with NumPy.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
 
col1, col2 = st.columns(2)
pass_mark = col1.number_input("Pass mark (%)", min_value=0, max_value=100, value=40, step=1)
max_marks = col2.number_input("Max marks per subject", min_value=1, max_value=1000, value=100, step=5)
 
# ---------------------------------------------------------------- calculations (same logic as the script)
students = list(df.index)
subjects = list(df.columns)
array = np.clip(df.to_numpy(dtype=float), 0, max_marks)
n_students, n_subjects = array.shape
 
total_marks = array.sum(axis=1)
average_marks = array.mean(axis=1)
highest_marks = array.max(axis=1)
lowest_marks = array.min(axis=1)
 
percentage = (total_marks / (n_subjects * max_marks)) * 100
passed = percentage >= pass_mark
rank = pd.Series(percentage).rank(ascending=False, method="min").astype(int).to_numpy()
 
subject_average = array.mean(axis=0)
subject_highest = array.max(axis=0)
subject_lowest = array.min(axis=0)
subject_toppers = np.argmax(array, axis=0)
subject_pass_rate = (array >= pass_mark / 100 * max_marks).mean(axis=0) * 100
 
summary = pd.DataFrame(
    {
        "Rank": rank,
        "Student": students,
        "Total": total_marks.astype(int),
        "Average": np.round(average_marks, 2),
        "Highest": highest_marks.astype(int),
        "Lowest": lowest_marks.astype(int),
        "Percentage": np.round(percentage, 2),
        "Result": np.where(passed, "✅ Pass", "❌ Fail"),
    }
).sort_values(["Rank", "Student"], kind="stable").reset_index(drop=True)
 
top_student = summary.iloc[0]
toughest = subjects[int(np.argmin(subject_average))]
 
# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown(
        f'<div class="sb-head">{svg(I_CHART, "#A5B4FC", 24)} Marks Analyzer</div>'
        '<div class="sb-label">RANKING</div>',
        unsafe_allow_html=True,
    )
    rows = "".join(
        f'<div class="sb-row"><span class="sb-rank">#{r.Rank}</span>'
        f'<span class="sb-name">{html.escape(str(r.Student))}</span>'
        f'<span class="sb-pct">{r.Percentage:.1f}%</span>'
        f'<span class="sb-dot" style="background:{"#34D399" if "Pass" in r.Result else "#F87171"}"></span></div>'
        for r in summary.itertuples()
    )
    subj_chips = "".join(f'<span class="sb-subj">{html.escape(str(s))}</span>' for s in subjects)
    st.markdown(rows + '<div class="sb-label">SUBJECTS</div>' + subj_chips, unsafe_allow_html=True)
 
# ---------------------------------------------------------------- top stats
stat_cards(
    [
        (I_USERS, n_students, "Total students", ""),
        (I_PERCENT, f"{percentage.mean():.1f}%", "Class average", ""),
        (I_CHECK, f"{passed.mean() * 100:.0f}%", f"Pass rate ({int(passed.sum())} of {n_students})", "green"),
        (I_TROPHY, top_student["Student"], f"Top performer ({top_student['Percentage']:.1f}%)", ""),
    ]
)
 
tab_over, tab_stu, tab_sub, tab_data = st.tabs(
    ["📊  Overview", "🎓  Students", "📚  Subjects", "🧮  Data"]
)
 
# ---------------------------------------------------------------- OVERVIEW
with tab_over:
    st.subheader("Percentage by student")
    st.markdown(
        f'<div class="note">Dashed line = pass mark ({pass_mark}%). Red bars are below it.</div>',
        unsafe_allow_html=True,
    )
    bar_chart(summary["Student"], summary["Percentage"], pass_mark, 100, "Percentage")
 
    st.subheader("Leaderboard")
    st.dataframe(
        summary,
        hide_index=True,
        column_config={
            "Percentage": st.column_config.ProgressColumn(
                "Percentage", min_value=0, max_value=100, format="%.1f%%"
            ),
        },
    )
    st.download_button(
        "Download report (CSV)",
        data=summary.to_csv(index=False),
        file_name="student_report.csv",
        mime="text/csv",
    )
 
# ---------------------------------------------------------------- STUDENTS
with tab_stu:
    st.subheader("Student report")
    pick = st.selectbox("Student", students)
    i = students.index(pick)
 
    stat_cards(
        [
            (I_SUM, f"{int(total_marks[i])} / {int(n_subjects * max_marks)}", "Total marks", ""),
            (I_CHART, f"{average_marks[i]:.2f}", "Average marks", ""),
            (I_PERCENT, f"{percentage[i]:.2f}%", "Percentage", ""),
            (
                I_CHECK if passed[i] else I_MEDAL,
                "Pass" if passed[i] else "Fail",
                f"Result (rank #{rank[i]} of {n_students})",
                "green" if passed[i] else "red",
            ),
        ]
    )
 
    pass_line = pass_mark / 100 * max_marks
    bar_chart(subjects, array[i], pass_line, max_marks, "Marks")
 
    best = subjects[int(np.argmax(array[i]))]
    worst = subjects[int(np.argmin(array[i]))]
    weak = [s for s, m in zip(subjects, array[i]) if m < pass_line]
    chips([f"Strongest: {best} ({int(highest_marks[i])})"], "good")
    chips([f"Weakest: {worst} ({int(lowest_marks[i])})"], "bad" if lowest_marks[i] < pass_line else "")
    if weak:
        st.markdown('<div class="note">Subjects below the pass mark:</div>', unsafe_allow_html=True)
        chips(weak, "bad")
    else:
        st.markdown('<div class="note">Passed every subject.</div>', unsafe_allow_html=True)
 
# ---------------------------------------------------------------- SUBJECTS
with tab_sub:
    st.subheader("Subject analysis")
    subject_table = pd.DataFrame(
        {
            "Subject": subjects,
            "Average": np.round(subject_average, 2),
            "Highest": subject_highest.astype(int),
            "Lowest": subject_lowest.astype(int),
            "Pass rate": np.round(subject_pass_rate, 1),
            "Topper": [students[k] for k in subject_toppers],
        }
    )
    st.dataframe(
        subject_table,
        hide_index=True,
        column_config={
            "Pass rate": st.column_config.ProgressColumn(
                "Pass rate", min_value=0, max_value=100, format="%.0f%%"
            ),
        },
    )
 
    st.subheader("Average marks per subject")
    bar_chart(subjects, subject_average, pass_mark / 100 * max_marks, max_marks, "Average marks")
    chips([f"Toughest subject: {toughest} ({subject_average[subjects.index(toughest)]:.1f} avg)"], "bad")
 
    st.subheader("Subject toppers")
    cards = "".join(
        f'<div class="topper"><div class="topper-sub">{html.escape(str(subjects[j]).upper())}</div>'
        f'<div class="topper-name">{html.escape(str(students[subject_toppers[j]]))}</div>'
        f'<div class="topper-marks">{int(array[subject_toppers[j], j])} marks</div></div>'
        for j in range(n_subjects)
    )
    st.markdown(f'<div class="toppers">{cards}</div>', unsafe_allow_html=True)
 
# ---------------------------------------------------------------- DATA
with tab_data:
    st.subheader("Edit the marks")
    st.markdown(
        '<div class="note">Double-click any cell to change a mark. Every chart and table updates instantly.</div>',
        unsafe_allow_html=True,
    )
    edited = st.data_editor(
        df,
        key=f"editor_{st.session_state.ver}",
        column_config={
            s: st.column_config.NumberColumn(s, min_value=0, max_value=int(max_marks), step=1)
            for s in subjects
        },
    )
    edited = edited.fillna(0)
    if not edited.equals(df):
        st.session_state.df = edited
        st.rerun()
 
    if st.button("Reset to original data"):
        st.session_state.df = default_df()
        st.session_state.ver += 1
        st.rerun()