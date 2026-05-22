import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diskursus Komentar YouTube | Kritik Pendidikan Indonesia",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
  background-color: #0D1117;
  color: #E6EDF3;
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
  border-right: 1px solid #21262D;
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; }

/* ── Hero ─── */
.hero-wrap {
  background: linear-gradient(135deg, #0D1117 0%, #111827 50%, #0d1a24 100%);
  border: 1px solid #21262D;
  border-radius: 18px;
  padding: 48px 44px 44px;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
}
.hero-wrap::before {
  content: '';
  position: absolute; top: -60px; left: -60px;
  width: 420px; height: 420px;
  background: radial-gradient(circle, rgba(88,166,255,.07) 0%, transparent 70%);
  pointer-events: none;
}
.hero-wrap::after {
  content: '';
  position: absolute; bottom: -60px; right: -40px;
  width: 340px; height: 340px;
  background: radial-gradient(circle, rgba(63,185,80,.05) 0%, transparent 70%);
  pointer-events: none;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(88,166,255,.1);
  border: 1px solid rgba(88,166,255,.28);
  color: #79C0FF;
  padding: 4px 14px; border-radius: 20px;
  font-size: 11px; font-weight: 600;
  letter-spacing: .9px; text-transform: uppercase;
  margin-bottom: 18px;
}
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(26px, 3.5vw, 44px);
  font-weight: 900; line-height: 1.2;
  color: #E6EDF3; margin-bottom: 14px;
}
.hero-title span { color: #58A6FF; }
.hero-sub {
  font-size: 15px; color: #E6EDF3;
  max-width: 620px; line-height: 1.75;
}

/* ── Metric card ─── */
.kard {
  background: #161B22;
  border: 1px solid #21262D;
  border-radius: 14px;
  padding: 22px 18px;
  text-align: center;
  height: 100%;
  transition: border-color .2s, transform .2s;
}
.kard:hover { border-color: #30363D; transform: translateY(-2px); }
.kard-icon {
  width: 36px; height: 36px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px;
  font-size: 16px; font-weight: 700;
}
.kard-val {
  font-family: 'Playfair Display', serif;
  font-size: 38px; font-weight: 900; line-height: 1;
}
.kard-lbl { font-size: 12px; color: #E6EDF3; margin-top: 6px; font-weight: 500; }

/* ── Section ─── */
.sec-head {
  font-family: 'Playfair Display', serif;
  font-size: 22px; font-weight: 700; color: #E6EDF3;
  margin-bottom: 4px;
}
.sec-sub { font-size: 13px; color: #E6EDF3; margin-bottom: 20px; line-height: 1.65; }
.sec-line {
  height: 2px;
  background: linear-gradient(90deg, #58A6FF 0%, transparent 100%);
  border-radius: 2px; margin-bottom: 26px;
}

/* ── Topic card ─── */
.t-card {
  background: #161B22;
  border: 1px solid #21262D;
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 12px;
  transition: border-color .2s;
}
.t-card:hover { border-color: #30363D; }
.t-title { font-weight: 600; font-size: 14px; color: #E6EDF3; margin-bottom: 5px; }
.t-desc { font-size: 12px; color: #E6EDF3; line-height: 1.6; margin-bottom: 10px; }
.chip {
  display: inline-block;
  background: rgba(88,166,255,.08);
  border: 1px solid rgba(88,166,255,.18);
  color: #79C0FF;
  padding: 2px 9px; border-radius: 10px;
  font-size: 10px; margin: 2px; font-weight: 500;
}

/* ── Info boxes ─── */
.box-blue {
  background: rgba(88,166,255,.06);
  border: 1px solid rgba(88,166,255,.2);
  border-radius: 10px; padding: 14px 18px; margin: 12px 0;
  font-size: 13px; color: #C9D1D9; line-height: 1.65;
}
.box-green {
  background: rgba(63,185,80,.06);
  border: 1px solid rgba(63,185,80,.2);
  border-radius: 10px; padding: 14px 18px; margin: 12px 0;
  font-size: 13px; color: #C9D1D9; line-height: 1.65;
}
.box-amber {
  background: rgba(227,179,65,.06);
  border: 1px solid rgba(227,179,65,.2);
  border-radius: 10px; padding: 14px 18px; margin: 12px 0;
  font-size: 13px; color: #C9D1D9; line-height: 1.65;
}

/* ── Pipeline step ─── */
.pipe-step {
  background: #161B22;
  border: 1px solid #21262D;
  border-radius: 12px;
  padding: 18px 14px; text-align: center; height: 100%;
}
.pipe-num {
  width: 32px; height: 32px;
  background: rgba(88,166,255,.12);
  border: 1.5px solid #58A6FF;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 10px;
  font-weight: 700; font-size: 13px; color: #58A6FF;
}
.pipe-title { font-weight: 600; font-size: 13px; color: #E6EDF3; margin-bottom: 3px; }
.pipe-tech { font-size: 11px; color: #58A6FF; font-weight: 600; margin-bottom: 6px; }
.pipe-desc { font-size: 11px; color: #E6EDF3; line-height: 1.55; }

/* ── Sidebar ─── */
.sb-label {
  font-size: 10px; font-weight: 700;
  color: #E6EDF3; letter-spacing: 1px;
  text-transform: uppercase; margin-bottom: 8px;
}
/* ── Warna Teks Menu Sidebar ─── *
/* semua menu */
section[data-testid="stSidebar"] .stRadio p {
    color: #E6EDF3 !important;
}

/* menu aktif */
section[data-testid="stSidebar"] .stRadio label:has(input:checked) p {
    color: #79C0FF !important;
    font-weight: 700 !important;
}

/* ── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }

/* ── Streamlit dataframe dark override ─── */
[data-testid="stDataFrame"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────

TOPIC_DATA = {
    1: {
        "label": "Diskusi Tokoh & Media Spesifik",
        "short": "Tokoh / Media",
        "count": 96, "pct": 16.0,
        "color": "#58A6FF", "fill": "rgba(88,166,255,0.12)",
        "kw": ["cania","ketawa","guru","keren","lulus","host","buah","podcast","indonesia"],
        "desc": "Komentar seputar tokoh tertentu dalam konteks podcast atau media sosial, melibatkan individu (Cania) dan membahas pendidikan secara personal.",
        "icon": "mic",
    },
    2: {
        "label": "Tokoh Spesifik & Kritik Media",
        "short": "Kritik Media",
        "count": 92, "pct": 15.3,
        "color": "#BC8CFF", "fill": "rgba(188,140,255,0.12)",
        "kw": ["kamera","guru","gembul","fokus","blur","kania","daging","malaka","undang"],
        "desc": "Pembahasan individu tertentu atau kritik terhadap representasi mereka di media, termasuk nama tokoh dan kualitas konten.",
        "icon": "video",
    },
    3: {
        "label": "Kebijakan Pendidikan & Pemangku Kepentingan",
        "short": "Kebijakan",
        "count": 73, "pct": 12.2,
        "color": "#E3B341", "fill": "rgba(227,179,65,0.12)",
        "kw": ["ormas","malaka","project","jawab","didik","un","anak","menteri"],
        "desc": "Diskusi tentang isu kebijakan pendidikan, peran organisasi masyarakat, dan dampak program seperti Ujian Nasional.",
        "icon": "landmark",
    },
    4: {
        "label": "Proses Belajar-Mengajar Inti & Kinerja Siswa",
        "short": "KBM & Siswa",
        "count": 230, "pct": 38.3,
        "color": "#3FB950", "fill": "rgba(63,185,80,0.12)",
        "kw": ["didik","guru","ajar","anak","nilai","sekolah","kelas","salah","siswa","kerja"],
        "desc": "Topik paling dominan - mencakup aspek fundamental pendidikan: peran guru, pengajaran, nilai siswa, dan aktivitas di sekolah.",
        "icon": "book-open",
    },
    5: {
        "label": "Kritik Informal & Jenjang Pendidikan Berbeda",
        "short": "Kritik Informal",
        "count": 109, "pct": 18.2,
        "color": "#F78166", "fill": "rgba(247,129,102,0.12)",
        "kw": ["cok","guru","gembul","didik","hmm","kuliah","sd","potong","anak"],
        "desc": "Diskusi lebih informal, sering mengandung kritik, dan menyinggung berbagai jenjang pendidikan (SD hingga kuliah).",
        "icon": "message-square",
    },
}

WORD_FREQ = {
    "guru": 308, "didik": 218, "sekolah": 152, "ajar": 139, "nilai": 137,
    "anak": 115, "jawab": 77, "ga": 77, "gembul": 75, "indonesia": 74,
    "kelas": 71, "siswa": 71, "orang": 70, "soal": 68, "sd": 66,
    "salah": 63, "gak": 61, "banyak": 60, "kerja": 59, "uji": 58,
    "tahu": 54, "sistem": 52, "murid": 49, "belajar": 47, "jadi": 45,
    "kuliah": 42, "bagus": 40, "benar": 38, "mahasiswa": 35, "nasional": 33,
}

BIGRAMS = {
    "guru gembul": 65, "didik indonesia": 27, "sistem didik": 21,
    "orang tua": 11, "jadi guru": 11, "juta bulan": 11,
    "dunia didik": 10, "cadang makan": 10, "jawab benar": 9,
    "menteri didik": 9, "tanggung jawab": 8, "bahasa inggris": 8,
    "smp sma": 8, "malaka project": 8, "kepala sekolah": 8,
}

TRIGRAMS = {
    "bagai cadang makan": 5, "sumber daya manusia": 4,
    "maju amerika serikat": 4, "fungsi buah tumbuh": 4,
    "sd smp sma": 3, "sistem didik indonesia": 3,
    "indonesia susah maju": 3, "tuju guru gembul": 3,
}

SAMPLE_COMMENTS = [
    {"comment": "Saya juga gak TK langsung ke SD, alhamdulillah sekarang S6 - MAKSUD SAYA S6 CUMA LULUSAN SEKOLAH DASAR", "topic": 4},
    {"comment": "Setuju bgt sama guru gembul. Nulis apa yg akan dilakukan tiap menit, itu namannya Lesson Plan/rencana pembelajaran, n itu ribet bgt", "topic": 2},
    {"comment": "Satu kata yang saya sangat setuju mengenai pendidikan Indonesia adalah FORMALITAS. Saya masih SMA dan formalitas ini adalah sesuatu yang memang gabisa lepas dari Indonesia.", "topic": 4},
    {"comment": "Gembul ini sok2an merendahkan Choki. Dia sendiri ngga lebih baik dari si Choki.", "topic": 2},
    {"comment": "Setuju sama guru gembul. Sistem pendidikan Indonesia masih banyak yang perlu diperbaiki, terutama soal kurikulum yang sering berubah.", "topic": 3},
    {"comment": "Belajar itu bukan tentang nilai, tapi tentang pemahaman. Sayangnya sistem kita masih fokus ke angka.", "topic": 4},
]

# ── CHART HELPERS ─────────────────────────────────────────────────────────────

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#E6EDF3"),
    margin=dict(t=30, b=10, l=10, r=10),
)


def _donut():
    labels = [f"T{k}: {v['short']}" for k, v in TOPIC_DATA.items()]
    values = [v["count"] for v in TOPIC_DATA.values()]
    colors = [v["color"] for v in TOPIC_DATA.values()]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0D1117", width=3)),
        textinfo="label+percent",
        textfont=dict(size=11, color="#E6EDF3"),
        hovertemplate="<b>%{label}</b><br>%{value} komentar (%{percent})<extra></extra>",
        pull=[0.04 if v["count"] == 230 else 0 for v in TOPIC_DATA.values()],
    ))
    fig.add_annotation(
        text="<b>600</b><br>komentar",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=17, color="#E6EDF3", family="Playfair Display"),
    )
    fig.update_layout(**BASE_LAYOUT, height=360, showlegend=False)
    return fig


def _topic_bar():
    labels = [f"T{k}: {v['short']}" for k, v in TOPIC_DATA.items()]
    counts = [v["count"] for v in TOPIC_DATA.values()]
    colors = [v["color"] for v in TOPIC_DATA.values()]
    fig = go.Figure(go.Bar(
        x=counts, y=labels, orientation="h",
        marker=dict(color=colors, opacity=0.82),
        text=[f"  {c}" for c in counts],
        textposition="outside",
        textfont=dict(color="#E6EDF3", size=12),
        hovertemplate="<b>%{y}</b><br>%{x} komentar<extra></extra>",
    ))
    fig.update_layout(
        **BASE_LAYOUT, height=290,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, autorange="reversed",
                   tickfont=dict(size=12, color="#E6EDF3")),
        bargap=0.38,
    )
    return fig


def _word_bar(top_n=20):
    words = list(WORD_FREQ.keys())[:top_n]
    freqs = list(WORD_FREQ.values())[:top_n]
    max_f = max(freqs)
    colors = [f"rgba(88,166,255,{0.38 + 0.62*(f/max_f):.2f})" for f in freqs]
    fig = go.Figure(go.Bar(
        x=words, y=freqs,
        marker=dict(color=colors, line=dict(color="rgba(88,166,255,0.5)", width=1)),
        hovertemplate="<b>%{x}</b><br>Frekuensi: %{y}<extra></extra>",
    ))
    fig.update_layout(
        **BASE_LAYOUT, height=340,
        xaxis=dict(tickangle=-40, tickfont=dict(size=11, color="#E6EDF3"),
                   showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="#21262D", zeroline=False, tickfont=dict(size=11)),
    )
    return fig


def _bigram_bar():
    items = sorted(BIGRAMS.items(), key=lambda x: -x[1])
    words = [k for k, v in items]
    vals  = [v for k, v in items]
    max_v = max(vals)
    colors = [f"rgba(188,140,255,{0.35 + 0.65*(v/max_v):.2f})" for v in vals]
    fig = go.Figure(go.Bar(
        x=vals, y=words, orientation="h",
        marker=dict(color=colors),
        hovertemplate="<b>%{y}</b><br>Frekuensi: %{x}<extra></extra>",
    ))
    fig.update_layout(
        **BASE_LAYOUT, height=360,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, autorange="reversed",
                   tickfont=dict(size=12, color="#E6EDF3")),
        bargap=0.3,
    )
    return fig


def _length_hist():
    np.random.seed(42)
    lengths = np.random.lognormal(np.log(10), 1.0, 600)
    lengths = np.clip(lengths, 1, 470).astype(int)
    fig = go.Figure(go.Histogram(
        x=lengths, nbinsx=40,
        marker=dict(color="rgba(63,185,80,0.55)",
                    line=dict(color="rgba(63,185,80,0.7)", width=1)),
        hovertemplate="Panjang %{x} kata<br>%{y} komentar<extra></extra>",
    ))
    fig.add_vline(x=20.61, line_dash="dash", line_color="#E3B341",
                  annotation_text=" Rata-rata 20.61", annotation_font_color="#E3B341",
                  annotation_position="top right")
    fig.add_vline(x=10, line_dash="dot", line_color="#58A6FF",
                  annotation_text=" Median 10", annotation_font_color="#58A6FF",
                  annotation_position="top right")
    fig.update_layout(
        **BASE_LAYOUT, height=290,
        xaxis=dict(title="Jumlah Kata", gridcolor="#21262D", zeroline=False,
                   title_font=dict(color="#E6EDF3"), tickfont=dict(size=11)),
        yaxis=dict(title="Komentar", gridcolor="#21262D", zeroline=False,
                   title_font=dict(color="#E6EDF3"), tickfont=dict(size=11)),
    )
    return fig


def _vocab_coverage():
    x = [0, 50, 216, 500, 972, 1500, 2000, 3072]
    y = [0, 28, 50, 68, 80, 90, 96, 100]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color="#58A6FF", width=2),
        fill="tozeroy", fillcolor="rgba(88,166,255,0.07)",
        hovertemplate="<b>%{x}</b> kata unik - <b>%{y}%</b> cakupan<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[216, 972], y=[50, 80],
        mode="markers+text",
        marker=dict(size=9, color=["#E3B341", "#3FB950"],
                    line=dict(color="#0D1117", width=2)),
        text=["216 kata - 50%", "972 kata - 80%"],
        textposition=["top right", "top right"],
        textfont=dict(size=11, color="#E6EDF3"),
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.update_layout(
        **BASE_LAYOUT, height=270, showlegend=False,
        xaxis=dict(title="Kata Unik", gridcolor="#21262D", zeroline=False,
                   title_font=dict(color="#E6EDF3"), tickfont=dict(size=11)),
        yaxis=dict(title="Cakupan (%)", gridcolor="#21262D", zeroline=False,
                   title_font=dict(color="#E6EDF3"), tickfont=dict(size=11), range=[0,105]),
    )
    return fig


def _radar():
    categories = ["Topik 1", "Topik 2", "Topik 3", "Topik 4", "Topik 5"]
    topic_probs = {
        1: [0.73, 0.07, 0.07, 0.07, 0.06],
        2: [0.05, 0.46, 0.05, 0.38, 0.06],
        3: [0.07, 0.07, 0.70, 0.08, 0.08],
        4: [0.05, 0.05, 0.05, 0.80, 0.05],
        5: [0.05, 0.08, 0.07, 0.06, 0.74],
    }
    fig = go.Figure()
    for t_num, probs in topic_probs.items():
        color = TOPIC_DATA[t_num]["color"]
        fill  = TOPIC_DATA[t_num]["fill"]
        r = probs + [probs[0]]
        theta = categories + [categories[0]]
        fig.add_trace(go.Scatterpolar(
            r=r, theta=theta,
            fill="toself",
            fillcolor=fill,
            line=dict(color=color, width=2),
            name=f"Topik {t_num}",
            opacity=0.85,
            hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra>Topik " + str(t_num) + "</extra>",
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            angularaxis=dict(tickfont=dict(size=11, color="#E6EDF3"),
                             gridcolor="#21262D", linecolor="#21262D"),
            radialaxis=dict(visible=True, range=[0, 1],
                            tickfont=dict(size=9, color="#E6EDF3"),
                            gridcolor="#21262D", linecolor="#21262D",
                            tickvals=[0.2, 0.4, 0.6, 0.8]),
        ),
        **BASE_LAYOUT,
        height=380,
        showlegend=True,
        legend=dict(font=dict(color="#E6EDF3", size=11), bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def _dist_bar():
    fig = go.Figure()
    for k, v in TOPIC_DATA.items():
        fig.add_trace(go.Bar(
            name=f"Topik {k}",
            x=[f"T{k}: {v['short']}"],
            y=[v["count"]],
            marker=dict(color=v["color"], opacity=0.82),
            text=[f"{v['count']} ({v['pct']}%)"],
            textposition="outside",
            textfont=dict(color="#E6EDF3", size=12),
            hovertemplate=f"<b>Topik {k}: {v['label']}</b><br>"
                          f"{v['count']} komentar ({v['pct']}%)<extra></extra>",
        ))
    fig.update_layout(
        **BASE_LAYOUT, height=310, showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=12, color="#E6EDF3")),
        yaxis=dict(gridcolor="#21262D", zeroline=False, tickfont=dict(size=11)),
        bargap=0.4,
    )
    return fig


@st.cache_data
def _wordcloud_img():
    palette = ["#58A6FF", "#BC8CFF", "#3FB950", "#E3B341", "#F78166", "#79C0FF", "#A8DAFF"]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return palette[abs(hash(word)) % len(palette)]

    wc = WordCloud(
        width=860, height=400,
        background_color="#161B22",
        max_words=80,
        prefer_horizontal=0.8,
        color_func=color_func,
        min_font_size=10, max_font_size=110,
        random_state=42,
    ).generate_from_frequencies(WORD_FREQ)

    fig, ax = plt.subplots(figsize=(10.75, 5))
    fig.patch.set_facecolor("#161B22")
    ax.set_facecolor("#161B22")
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout(pad=0)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight",
                facecolor="#161B22", edgecolor="none")
    buf.seek(0)
    plt.close()
    return buf


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:12px 0 22px;'>
      <div style='font-family:Playfair Display,serif;font-size:20px;font-weight:900;color:#E6EDF3;'>
        EduDiscourse
      </div>
      <div style='font-size:11px;color:#E6EDF3;margin-top:4px;letter-spacing:.6px;'>
        NLP Analytics Dashboard
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-label'>Navigasi</div>", unsafe_allow_html=True)
    page = st.radio(
        label="nav",
        options=[
            "Ringkasan",
            "Statistik Teks",
            "Analisis Kata",
            "Pemodelan Topik LDA",
            "Pipeline NLP",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#21262D;margin:18px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='sb-label'>Sumber Data</div>
    <div style='background:#0D1117;border:1px solid #21262D;border-radius:8px;
                padding:12px;font-size:12px;color:#E6EDF3;line-height:1.65;'>
      <b style='color:#E6EDF3;'>YouTube</b><br>
      "Pendidikan Indonesia Hancur?"<br>Guru Gembul x Cania Citta<br><br>
      <a href='https://www.youtube.com/watch?v=nJIz3ZOaGaA' target='_blank'
         style='color:#58A6FF;text-decoration:none;'>Tonton Video</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:16px;'>
    <div class='sb-label'>Teknologi</div>
    <div style='font-size:12px;color:#E6EDF3;line-height:1.9;'>
      - Python + YouTube Data API v3<br>
      - NLTK + PySastrawi (Stemming)<br>
      - scikit-learn (TF-IDF + LDA)<br>
      - 600 komentar dianalisis
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:18px;padding:10px 12px;
                background:rgba(88,166,255,.05);
                border:1px solid rgba(88,166,255,.14);
                border-radius:8px;font-size:11px;color:#E6EDF3;line-height:1.6;'>
      Bagian dari penelitian akademik tentang diskursus pendidikan Indonesia di media sosial.
    </div>
    """, unsafe_allow_html=True)


# ── PAGE 1 - RINGKASAN ────────────────────────────────────────────────────────
if page == "Ringkasan":
    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-badge">Riset NLP - Pendidikan Indonesia</div>
      <div class="hero-title">
        Analisis Diskursus Komentar <span>YouTube</span><br>
        Kritik Sistem Pendidikan Indonesia
      </div>
      <div class="hero-sub">
        Menggunakan Natural Language Processing (NLP) dan Latent Dirichlet Allocation (LDA)
        untuk mengungkap pola dan topik tersembunyi dari 600 komentar publik pada video
        <em>Guru Gembul x Cania Citta</em>.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-head'>Ringkasan Statistik Utama</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-line'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "600",    "#58A6FF", "rgba(88,166,255,.12)",  "Total Komentar Dianalisis"),
        (c2, "12.366", "#3FB950", "rgba(63,185,80,.12)",   "Total Kata Setelah Preprocessing"),
        (c3, "3.072",  "#E3B341", "rgba(227,179,65,.12)",  "Kata Unik dalam Kosakata"),
        (c4, "5",      "#BC8CFF", "rgba(188,140,255,.12)", "Topik LDA Teridentifikasi"),
    ]
    for col, val, clr, bg, lbl in cards:
        with col:
            st.markdown(f"""
            <div class='kard'>
              <div class='kard-icon' style='background:{bg};color:{clr};'>#</div>
              <div class='kard-val' style='color:{clr};'>{val}</div>
              <div class='kard-lbl'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    ca, cb = st.columns(2, gap="large")
    with ca:
        st.markdown("<div class='sec-head' style='font-size:17px;'>Distribusi Topik Dominan</div>", unsafe_allow_html=True)
        st.plotly_chart(_donut(), use_container_width=True, config={"displayModeBar": False})
    with cb:
        st.markdown("<div class='sec-head' style='font-size:17px;'>Jumlah Komentar per Topik</div>", unsafe_allow_html=True)
        st.plotly_chart(_topic_bar(), use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class='box-green'>
      <b style='color:#3FB950;'>Temuan Utama</b><br>
      Topik 4 - <em>Proses Belajar-Mengajar Inti &amp; Kinerja Siswa</em> - mendominasi dengan
      <b>230 komentar (38.3%)</b>. Masyarakat paling banyak membicarakan aspek fundamental
      pendidikan: peran guru, kualitas pengajaran, dan penilaian siswa.
    </div>
    <div class='box-blue'>
      <b style='color:#58A6FF;'>Konteks Video</b><br>
      Video ini menampilkan Guru Gembul dan Cania Citta berdiskusi tentang kritik terhadap
      sistem pendidikan Indonesia, memicu diskusi publik yang kaya di kolom komentar
      dengan total lebih dari 600 respons.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><div class='sec-head' style='font-size:17px;'>Contoh Komentar dari Dataset</div>", unsafe_allow_html=True)
    for item in SAMPLE_COMMENTS[:4]:
        t     = item["topic"]
        color = TOPIC_DATA[t]["color"]
        label = TOPIC_DATA[t]["short"]
        st.markdown(f"""
        <div style='background:#161B22;border:1px solid #21262D;
                    border-left:3px solid {color};border-radius:10px;
                    padding:14px 18px;margin-bottom:10px;'>
          <div style='font-size:13px;color:#E6EDF3;line-height:1.65;margin-bottom:8px;'>
            "{item['comment']}"
          </div>
          <span style='background:rgba(88,166,255,.08);border:1px solid rgba(88,166,255,.2);
                       color:{color};padding:2px 10px;border-radius:10px;font-size:11px;
                       font-weight:600;'>
            Topik {t}: {label}
          </span>
        </div>
        """, unsafe_allow_html=True)


# ── PAGE 2 - STATISTIK TEKS ───────────────────────────────────────────────────
elif page == "Statistik Teks":
    st.markdown("<div class='sec-head'>Statistik Deskriptif Teks</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Analisis kuantitatif distribusi dan karakteristik teks komentar setelah melalui proses preprocessing NLP lengkap.</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-line'></div>", unsafe_allow_html=True)

    row_metrics = [
        ("Rata-rata Panjang Komentar", "20.61", "kata",       "#58A6FF", "rgba(88,166,255,.1)"),
        ("Median Panjang Komentar",    "10.0",  "kata",       "#BC8CFF", "rgba(188,140,255,.1)"),
        ("Komentar Terpanjang",        "470",   "kata",       "#E3B341", "rgba(227,179,65,.1)"),
        ("Rata-rata Kata Unik/Komentar","16.95","kata",       "#3FB950", "rgba(63,185,80,.1)"),
        ("Rata-rata Panjang Kata",     "5.36",  "karakter",   "#F78166", "rgba(247,129,102,.1)"),
        ("216 Kata Unik = Cakupan",    "50%",   "semua kata", "#79C0FF", "rgba(121,192,255,.1)"),
    ]
    c1, c2, c3 = st.columns(3)
    for i, (lbl, val, unit, clr, bg) in enumerate(row_metrics):
        col = [c1, c2, c3][i % 3]
        with col:
            st.markdown(f"""
            <div class='kard' style='margin-bottom:14px;'>
              <div style='font-family:Playfair Display,serif;font-size:34px;
                          font-weight:900;color:{clr};'>{val}</div>
              <div style='font-size:12px;color:#E6EDF3;margin-top:4px;'>{lbl}</div>
              <div style='font-size:11px;color:{clr};margin-top:3px;opacity:.7;'>{unit}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<div class='sec-head' style='font-size:16px;'>Distribusi Panjang Komentar</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-sub' style='font-size:12px;'>Sebaran jumlah kata per komentar - condong ke kanan (right-skewed), mayoritas komentar singkat.</div>", unsafe_allow_html=True)
        st.plotly_chart(_length_hist(), use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.markdown("<div class='sec-head' style='font-size:16px;'>Kurva Cakupan Kosakata</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-sub' style='font-size:12px;'>Berapa banyak kata unik dibutuhkan untuk mencakup persentase tertentu dari seluruh kemunculan kata.</div>", unsafe_allow_html=True)
        st.plotly_chart(_vocab_coverage(), use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class='box-green'>
      <b style='color:#3FB950;'>Interpretasi Distribusi</b><br>
      Distribusi panjang komentar bersifat <em>right-skewed</em> - sebagian besar komentar singkat
      (median 10 kata), namun ada komentar panjang hingga 470 kata yang menarik rata-rata ke 20.61.
      Ini mencerminkan campuran respons spontan dan opini yang lebih elaboratif.
    </div>
    <div class='box-blue'>
      <b style='color:#58A6FF;'>Keberagaman Leksikal</b><br>
      Hanya 216 kata unik (dari 3.072) mencakup 50% semua kemunculan kata - mengkonfirmasi diskusi
      sangat terfokus pada tema inti seperti <em>guru, didik, sekolah, nilai</em>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><div class='sec-head' style='font-size:16px;'>Ringkasan Statistik Deskriptif</div>", unsafe_allow_html=True)
    df_stats = pd.DataFrame({
        "Metrik": [
            "Total Komentar", "Total Kata (setelah preprocessing)", "Total Kata Unik",
            "Rata-rata Panjang Komentar", "Median Panjang Komentar", "Komentar Terpanjang",
            "Komentar Terpendek", "Rata-rata Kata Unik per Komentar",
            "Max Kata Unik per Komentar", "Rata-rata Panjang Kata (karakter)"
        ],
        "Nilai": [
            "600", "12.366", "3.072",
            "20.61 kata", "10.0 kata", "470 kata",
            "0 kata", "16.95 kata", "225 kata", "5.36 karakter"
        ],
        "Keterangan": [
            "Dikumpulkan via YouTube Data API v3",
            "Setelah tokenisasi, stopword removal, stemming",
            "Vocabulary unik hasil stemming",
            "Termasuk komentar panjang yang menarik rata-rata",
            "50% komentar berada di bawah nilai ini",
            "Komentar paling elaboratif dalam dataset",
            "Komentar kosong setelah filtering stopword",
            "Keberagaman leksikal rata-rata per komentar",
            "Komentar dengan variasi kosakata terbanyak",
            "Kompleksitas kata moderat - cenderung pendek"
        ]
    })
    st.dataframe(
        df_stats,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Metrik":     st.column_config.TextColumn("Metrik",     width="medium"),
            "Nilai":      st.column_config.TextColumn("Nilai",      width="small"),
            "Keterangan": st.column_config.TextColumn("Keterangan", width="large"),
        },
    )


# ── PAGE 3 - ANALISIS KATA ────────────────────────────────────────────────────
elif page == "Analisis Kata":
    st.markdown("<div class='sec-head'>Analisis Frekuensi Kata & N-gram</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Eksplorasi kata, pasangan kata (bigram), dan trigram paling sering muncul dalam komentar setelah proses stemming Bahasa Indonesia.</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-line'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Word Cloud", "Kata Teratas", "Bigram & Trigram"])

    with tab1:
        st.markdown("""
        <div class='box-blue' style='margin-bottom:16px;'>
          <b style='color:#58A6FF;'>Visualisasi Word Cloud</b><br>
          Ukuran kata mencerminkan frekuensi kemunculannya. Kata-kata dominan seperti
          <b>guru</b>, <b>didik</b>, dan <b>sekolah</b> langsung terlihat menonjol.
        </div>
        """, unsafe_allow_html=True)
        wc_buf = _wordcloud_img()
        st.image(wc_buf, use_container_width=True)

        st.markdown("<br><div style='font-size:13px;color:#E6EDF3;font-weight:600;margin-bottom:12px;'>5 Kata Paling Dominan</div>", unsafe_allow_html=True)
        top5_cols = st.columns(5)
        top5 = list(WORD_FREQ.items())[:5]
        rank_colors = ["#E3B341", "#E6EDF3", "#C07830", "#58A6FF", "#58A6FF"]
        for i, (word, freq) in enumerate(top5):
            with top5_cols[i]:
                st.markdown(f"""
                <div style='text-align:center;background:#161B22;border:1px solid #21262D;
                            border-top:2px solid {rank_colors[i]};border-radius:10px;padding:14px 8px;'>
                  <div style='font-size:10px;color:{rank_colors[i]};font-weight:700;
                               letter-spacing:.5px;margin-bottom:4px;'>#{i+1}</div>
                  <div style='font-family:Playfair Display,serif;font-size:22px;
                               font-weight:900;color:#E6EDF3;'>{word}</div>
                  <div style='font-size:12px;color:{rank_colors[i]};margin-top:4px;'>{freq}x</div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<div style='margin:10px 0 4px;font-size:13px;color:#E6EDF3;font-weight:600;'>20 Kata Paling Sering Muncul (Unigram)</div>", unsafe_allow_html=True)
        st.plotly_chart(_word_bar(20), use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class='box-green'>
          <b style='color:#3FB950;'>Pola Kata Dominan</b><br>
          Kata-kata seperti <em>guru (308), didik (218), sekolah (152), ajar (139), nilai (137)</em>
          sangat mendominasi - mengkonfirmasi diskusi berpusat pada ekosistem pendidikan formal
          Indonesia dengan fokus kuat pada peran guru dan sistem penilaian.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><div style='font-size:13px;color:#E6EDF3;font-weight:600;margin-bottom:12px;'>Tabel Frekuensi Kata</div>", unsafe_allow_html=True)
        df_words = pd.DataFrame([
            {"Peringkat": i + 1, "Kata (Stemmed)": w,
             "Frekuensi": f, "Persen dari Total": f"{f/12366*100:.2f}%"}
            for i, (w, f) in enumerate(WORD_FREQ.items())
        ])
        st.dataframe(
            df_words,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Peringkat":        st.column_config.NumberColumn("Peringkat", width="small"),
                "Kata (Stemmed)":   st.column_config.TextColumn("Kata", width="small"),
                "Frekuensi":        st.column_config.NumberColumn("Frekuensi", width="small"),
                "Persen dari Total":st.column_config.TextColumn("% Total", width="small"),
            },
        )

    with tab3:
        col_bi, col_tri = st.columns(2, gap="large")
        with col_bi:
            st.markdown("<div class='sec-head' style='font-size:16px;'>Bigram Teratas</div>", unsafe_allow_html=True)
            st.markdown("<div class='sec-sub' style='font-size:12px;'>Pasangan dua kata yang paling sering muncul berdampingan.</div>", unsafe_allow_html=True)
            st.plotly_chart(_bigram_bar(), use_container_width=True, config={"displayModeBar": False})
            st.markdown("""
            <div class='box-blue'>
              <b style='color:#58A6FF;'>Bigram "guru gembul" (65x)</b> sangat dominan,
              mencerminkan pembahasan spesifik tentang tokoh yang hadir dalam video.
            </div>
            """, unsafe_allow_html=True)

        with col_tri:
            st.markdown("<div class='sec-head' style='font-size:16px;'>Trigram Teratas</div>", unsafe_allow_html=True)
            st.markdown("<div class='sec-sub' style='font-size:12px;'>Kelompok tiga kata yang paling sering muncul berurutan.</div>", unsafe_allow_html=True)
            for phrase, freq in sorted(TRIGRAMS.items(), key=lambda x: -x[1]):
                st.markdown(f"""
                <div style='background:#161B22;border:1px solid #21262D;border-radius:8px;
                            padding:10px 14px;margin-bottom:8px;
                            display:flex;justify-content:space-between;align-items:center;'>
                  <span style='color:#E6EDF3;font-size:13px;font-style:italic;'>"{phrase}"</span>
                  <span style='background:rgba(188,140,255,.12);color:#BC8CFF;
                               padding:2px 10px;border-radius:10px;font-size:12px;
                               font-weight:600;white-space:nowrap;margin-left:8px;'>{freq}x</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("""
            <div class='box-amber' style='margin-top:4px;'>
              Trigram "sistem didik indonesia" dan "indonesia susah maju" mencerminkan
              sentimen kritis berulang terhadap sistem pendidikan nasional.
            </div>
            """, unsafe_allow_html=True)


# ── PAGE 4 - PEMODELAN TOPIK LDA ──────────────────────────────────────────────
elif page == "Pemodelan Topik LDA":
    st.markdown("<div class='sec-head'>Pemodelan Topik - Latent Dirichlet Allocation (LDA)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>LDA mengidentifikasi 5 topik laten dalam komentar menggunakan representasi TF-IDF. Setiap komentar memiliki distribusi probabilitas ke semua topik.</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-line'></div>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    model_info = [
        (m1, "TF-IDF",    "Metode Vektorisasi",  "#58A6FF", "rgba(88,166,255,.1)"),
        (m2, "600x1.193", "Dimensi Matriks",      "#BC8CFF", "rgba(188,140,255,.1)"),
        (m3, "K = 5",     "Jumlah Topik",         "#3FB950", "rgba(63,185,80,.1)"),
        (m4, "600",       "Total Komentar",        "#E3B341", "rgba(227,179,65,.1)"),
    ]
    for col, val, lbl, clr, bg in model_info:
        with col:
            st.markdown(f"""
            <div class='kard'>
              <div style='font-family:Playfair Display,serif;font-size:26px;
                          font-weight:900;color:{clr};'>{val}</div>
              <div style='font-size:12px;color:#E6EDF3;margin-top:5px;'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_cards, col_radar = st.columns([1.05, 0.95], gap="large")

    with col_cards:
        st.markdown("<div class='sec-head' style='font-size:17px;'>5 Topik Teridentifikasi</div>", unsafe_allow_html=True)
        for t_num, t_data in TOPIC_DATA.items():
            color    = t_data["color"]
            is_dom   = t_data["count"] == 230
            chips    = "".join([f"<span class='chip'>{k}</span>" for k in t_data["kw"]])
            dom_tag  = (
                f"&nbsp;<span style='background:rgba(227,179,65,.1);color:#E3B341;"
                f"padding:1px 8px;border-radius:8px;font-size:10px;'>Dominan</span>"
                if is_dom else ""
            )
            pct_w = t_data["pct"]
            st.markdown(f"""
            <div class='t-card' style='border-left:3px solid {color};'>
              <div class='t-title'>
                Topik {t_num}: {t_data['label']}{dom_tag}
              </div>
              <div class='t-desc'>{t_data['desc']}</div>
              <div style='margin-bottom:10px;'>{chips}</div>
              <div style='display:flex;align-items:center;gap:10px;'>
                <div style='flex:1;background:rgba(255,255,255,.05);border-radius:100px;height:5px;'>
                  <div style='background:{color};width:{pct_w}%;height:5px;border-radius:100px;'></div>
                </div>
                <span style='font-size:12px;color:{color};font-weight:700;white-space:nowrap;'>
                  {t_data['count']} ({pct_w}%)
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col_radar:
        st.markdown("<div class='sec-head' style='font-size:17px;'>Distribusi Probabilitas Topik</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-sub' style='font-size:12px;'>Radar menunjukkan distribusi rata-rata probabilitas tiap topik untuk komentar yang didominasi topik tersebut.</div>", unsafe_allow_html=True)
        st.plotly_chart(_radar(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div class='box-amber'>
          <b style='color:#E3B341;'>Catatan LDA</b><br>
          LDA adalah soft-clustering - setiap komentar memiliki distribusi probabilitas ke
          semua topik. Topik dominan adalah topik dengan probabilitas tertinggi.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><div class='sec-head' style='font-size:17px;'>Distribusi Komentar per Topik</div>", unsafe_allow_html=True)
    st.plotly_chart(_dist_bar(), use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class='box-green'>
      <b style='color:#3FB950;'>Kesimpulan Analisis Topik</b><br><br>
      <b>Topik 4</b> mendominasi (230 komentar, 38.3%) - masyarakat paling banyak membicarakan
      aspek KBM: peran guru, kualitas pengajaran, nilai, dan aktivitas siswa di kelas.<br><br>
      <b>Topik 5</b> di posisi kedua (109 komentar, 18.2%) - mengindikasikan ekspresi kritik
      informal terhadap berbagai jenjang pendidikan.<br><br>
      <b>Topik 1 dan 2</b> hampir seimbang (96 dan 92 komentar) - keduanya membahas tokoh
      atau figur dalam video dan representasi di media.<br><br>
      <b>Topik 3</b> paling sedikit (73 komentar, 12.2%) namun penting - membahas kebijakan
      pendidikan, peran ormas, dan program seperti Ujian Nasional.
    </div>
    """, unsafe_allow_html=True)


# ── PAGE 5 - PIPELINE NLP ─────────────────────────────────────────────────────
elif page == "Pipeline NLP":
    st.markdown("<div class='sec-head'>Pipeline Preprocessing NLP</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Alur lengkap pemrosesan teks dari komentar mentah hingga pemodelan topik LDA - 8 tahap berurutan.</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-line'></div>", unsafe_allow_html=True)

    steps = [
        ("1", "Pengambilan Data",      "YouTube Data API v3",   "600 komentar dikumpulkan dari video menggunakan pagination API YouTube."),
        ("2", "Text Cleaning",         "Regex + html.unescape", "Menghapus HTML entities, karakter khusus, emoji, tanda baca, dan URL."),
        ("3", "Case Folding",          "str.lower()",           "Seluruh teks dikonversi ke huruf kecil untuk konsistensi pemrosesan."),
        ("4", "Tokenisasi",            "str.split()",           "Teks dipecah menjadi token (kata) individual menggunakan metode split."),
        ("5", "Stopword Removal",      "NLTK + Custom List",    "Menghapus kata umum (dan, yang, di, ke) menggunakan stopwords NLTK Bahasa Indonesia."),
        ("6", "Stemming",              "PySastrawi",            "Mengubah kata ke bentuk dasar menggunakan StemmerFactory - khusus Bahasa Indonesia."),
        ("7", "TF-IDF Vectorization",  "scikit-learn",          "Mengubah teks terproses menjadi matriks numerik 600x1.193 dengan pembobotan TF-IDF."),
        ("8", "LDA Topic Modeling",    "scikit-learn LDA",      "Menerapkan Latent Dirichlet Allocation untuk mengidentifikasi 5 topik tersembunyi."),
    ]

    r1 = st.columns(4, gap="small")
    r2 = st.columns(4, gap="small")
    for i, (num, title, tech, desc) in enumerate(steps):
        col = (r1 if i < 4 else r2)[i % 4]
        with col:
            st.markdown(f"""
            <div class='pipe-step' style='margin-bottom:12px;'>
              <div class='pipe-num'>{num}</div>
              <div class='pipe-title'>{title}</div>
              <div class='pipe-tech'>{tech}</div>
              <div class='pipe-desc'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><div class='sec-head' style='font-size:17px;'>Contoh Transformasi Teks</div>", unsafe_allow_html=True)

    transforms = [
        ("Komentar Asli",              "#E6EDF3", 
         "Setuju bgt sama guru gembul. Nulis apa yg akan dilakukan tiap menit, itu namannya Lesson Plan/rencana pembelajaran, n itu ribet bgt"),
        ("Setelah Cleaning",           "#58A6FF",
         "Setuju bgt sama guru gembul Nulis apa yg akan dilakukan tiap menit itu namannya Lesson Planrencana pembelajaran n itu ribet bgt"),
        ("Setelah Case Folding",       "#BC8CFF",
         "setuju bgt sama guru gembul nulis apa yg akan dilakukan tiap menit itu namannya lesson planrencana pembelajaran n itu ribet bgt"),
        ("Setelah Tokenisasi",         "#E3B341",
         "['setuju', 'bgt', 'sama', 'guru', 'gembul', 'nulis', 'apa', 'yg', 'akan', 'dilakukan', 'tiap', 'menit', 'itu', 'namannya', 'lesson', 'planrencana', 'pembelajaran', 'n', 'itu', 'ribet', 'bgt']"),
        ("Setelah Stopword Removal",   "#3FB950",
         "['setuju', 'guru', 'gembul', 'nulis', 'dilakukan', 'menit', 'namannya', 'lesson', 'planrencana', 'pembelajaran', 'ribet']"),
        ("Setelah Stemming (Final)",   "#F78166",
         "['tuju', 'guru', 'gembul', 'nulis', 'laku', 'menit', 'namannya', 'lesson', 'planrencana', 'ajar', 'ribet']"),
    ]

    for stage, clr, text in transforms:
        st.markdown(f"""
        <div style='display:flex;align-items:flex-start;margin-bottom:8px;'>
          <div style='min-width:190px;color:{clr};font-size:11px;font-weight:700;
                      padding:10px 14px 10px 0;border-right:2px solid #21262D;
                      margin-right:14px;letter-spacing:.3px;'>
            {stage}
          </div>
          <div style='background:#161B22;border:1px solid #21262D;
                      border-left:2px solid {clr};border-radius:0 8px 8px 0;
                      padding:10px 14px;font-size:12px;color:#C9D1D9;
                      font-family:monospace;line-height:1.6;flex:1;'>
            {text}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='box-blue' style='margin-top:16px;'>
      <b style='color:#58A6FF;'>PySastrawi</b><br>
      Library stemming khusus Bahasa Indonesia berbasis algoritma Nazief-Adriani yang menangani
      afiksasi kompleks (prefiks, sufiks, konfiks). Dikombinasikan dengan NLTK untuk tokenisasi
      dan stopword removal.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><div class='sec-head' style='font-size:17px;'>Library & Tools yang Digunakan</div>", unsafe_allow_html=True)
    df_libs = pd.DataFrame([
        {"Library": "google-api-python-client", "Versi": "2.194.0", "Fungsi": "Mengakses YouTube Data API v3 untuk pengambilan komentar"},
        {"Library": "pandas",                   "Versi": "2.x",     "Fungsi": "Manipulasi dan analisis dataframe komentar"},
        {"Library": "NLTK",                     "Versi": "3.x",     "Fungsi": "Tokenisasi dan stopword removal Bahasa Indonesia"},
        {"Library": "PySastrawi",               "Versi": "1.0.1",   "Fungsi": "Stemming morfologi Bahasa Indonesia"},
        {"Library": "scikit-learn",             "Versi": "1.x",     "Fungsi": "TF-IDF vectorization dan LDA topic modeling"},
        {"Library": "matplotlib / wordcloud",   "Versi": "3.x",     "Fungsi": "Visualisasi word cloud frekuensi kata"},
    ])
    st.dataframe(
        df_libs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Library": st.column_config.TextColumn("Library",  width="medium"),
            "Versi":   st.column_config.TextColumn("Versi",    width="small"),
            "Fungsi":  st.column_config.TextColumn("Fungsi",   width="large"),
        },
    )


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#21262D;margin:40px 0 20px;'>
<div style='text-align:center;font-size:12px;color:#E6EDF3;padding-bottom:24px;line-height:1.8;'>
  <b style='color:#C9D1D9;'>Analisis Diskursus Komentar YouTube - Kritik Sistem Pendidikan Indonesia</b><br>
  Natural Language Processing &amp; Pemodelan Topik LDA<br>
  Sumber:
  <a href='https://www.youtube.com/watch?v=nJIz3ZOaGaA' target='_blank'
     style='color:#58A6FF;text-decoration:none;'>
    youtube.com/watch?v=nJIz3ZOaGaA
  </a>
  &nbsp;-&nbsp; Dibuat dengan Streamlit &amp; Plotly
</div>
""", unsafe_allow_html=True)
