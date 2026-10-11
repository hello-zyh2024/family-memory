# -*- coding: utf-8 -*-
"""家的记忆 —— 一个给家里人看的相册。"""

import html
import json
from datetime import datetime
from pathlib import Path

import streamlit as st

import photo_data as P

BASE = Path(__file__).parent
STATIC = BASE / "static"
GUESTBOOK = BASE / "guestbook.json"

st.set_page_config(
    page_title="家的记忆",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "家的记忆 · 2024 夏"},
)

# ---------------------------------------------------------------- 留言本存取


def load_guestbook():
    if GUESTBOOK.exists():
        try:
            return json.loads(GUESTBOOK.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def add_guestbook(name, words):
    entries = load_guestbook()
    entries.append(
        {
            "name": name.strip() or "匿名",
            "words": words.strip(),
            "at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    GUESTBOOK.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------- 样式

CSS = """
<style>
.mem, .mem * { box-sizing: border-box; }

.mem {
  --ink:       #4A3F35;
  --ink-soft:  #8A7864;
  --paper:     #FBF7F0;
  --line:      #E6DAC8;
  --accent:    #A9714B;
  --serif: 'KaiTi', 'Kaiti SC', 'STKaiti', '楷体', 'Noto Serif SC', 'Songti SC', serif;
  max-width: 1180px;
  margin: 0 auto;
  color: var(--ink);
  font-feature-settings: "palt";
}

/* ---------------------------------------------------------- 首页大图 */
.mem .hero {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 55px rgba(74, 63, 53, .20);
  margin-bottom: 2.6rem;
}
.mem .hero img {
  display: block;
  width: 100%;
  height: 58vh;
  min-height: 340px;
  max-height: 600px;
  object-fit: cover;
}
.mem .hero .veil {
  position: absolute; inset: 0;
  background: linear-gradient(180deg,
              rgba(32, 25, 17, .08) 0%,
              rgba(32, 25, 17, .26) 42%,
              rgba(32, 25, 17, .74) 100%);
}
.mem .hero .words {
  position: absolute; left: 0; right: 0; bottom: 9%;
  text-align: center;
  color: #FFF9F0;
  text-shadow: 0 2px 20px rgba(0, 0, 0, .5);
}
.mem .hero h1 {
  font-family: var(--serif);
  font-size: clamp(2.1rem, 5.2vw, 3.9rem);
  font-weight: 600;
  letter-spacing: .40em;
  text-indent: .40em;
  margin: 0 0 .7rem;
  color: #FFF9F0;
  border: 0;
  padding: 0;
}
.mem .hero .sub {
  font-size: clamp(.78rem, 1.4vw, .98rem);
  letter-spacing: .34em;
  text-indent: .34em;
  opacity: .88;
}

/* ---------------------------------------------------------- 引言 */
.mem .intro {
  max-width: 620px;
  margin: 0 auto 3.4rem;
  text-align: center;
  font-family: var(--serif);
  font-size: 1.05rem;
  line-height: 2.1;
  color: var(--ink-soft);
  letter-spacing: .06em;
}
.mem .intro .orn {
  display: block;
  color: var(--accent);
  opacity: .55;
  letter-spacing: .6em;
  text-indent: .6em;
  font-size: .8rem;
  margin-bottom: 1.1rem;
}

/* ---------------------------------------------------------- 时间轴 */
.mem .grp { margin-bottom: 3.6rem; }
.mem .grp-head {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin: 2.9rem 0 1.6rem;
  padding-bottom: .7rem;
  border-bottom: 1px solid var(--line);
}

/* ---------------------------------------------------------- 视频 */
.mem .vidcap {
  text-align: center;
  margin-top: 1.1rem;
  font-family: var(--serif);
  font-size: 1rem;
  letter-spacing: .08em;
  color: var(--ink-soft);
  line-height: 2;
}
.mem .vidcap .vnote {
  display: block;
  margin-top: .5rem;
  font-family: system-ui, sans-serif;
  font-size: .72rem;
  letter-spacing: .05em;
  color: #B6A794;
}
.mem .grp-date {
  font-family: var(--serif);
  font-size: 1.5rem;
  letter-spacing: .22em;
  color: var(--ink);
  white-space: nowrap;
}
.mem .grp-title {
  font-size: .92rem;
  letter-spacing: .16em;
  color: var(--accent);
  white-space: nowrap;
}
.mem .grp-meta {
  margin-left: auto;
  font-size: .74rem;
  letter-spacing: .18em;
  color: var(--ink-soft);
  opacity: .75;
  white-space: nowrap;
}

/* ---------------------------------------------------------- 照片墙 */
.mem .grid {
  column-count: 3;
  column-gap: 20px;
}
@media (max-width: 900px) { .mem .grid { column-count: 2; } }
@media (max-width: 600px) { .mem .grid { column-count: 1; } }

.mem .card {
  display: block;
  break-inside: avoid;
  -webkit-column-break-inside: avoid;
  margin: 0 0 20px;
  padding: 11px 11px 0;
  background: #FFFFFF;
  border-radius: 3px;
  box-shadow: 0 5px 16px rgba(74, 63, 53, .13);
  transform: rotate(var(--tilt, 0deg));
  transition: transform .38s cubic-bezier(.2, .7, .3, 1),
              box-shadow .38s ease;
  cursor: zoom-in;
}
.mem .card:hover {
  transform: rotate(0deg) translateY(-7px);
  box-shadow: 0 20px 44px rgba(74, 63, 53, .25);
}
.mem .card img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 2px;
  background: #EFE7DA;
}
.mem .card .cap {
  padding: 11px 5px 15px;
  font-size: .85rem;
  line-height: 1.75;
  color: var(--ink-soft);
  letter-spacing: .03em;
}

/* ---------------------------------------------------------- 灯箱 */
.mem .lbstate { display: none; }
.mem .ov {
  display: none;
  position: fixed; inset: 0;
  z-index: 99999;
  background: rgba(26, 20, 14, .94);
}
.mem .ov-bg { position: absolute; inset: 0; cursor: zoom-out; }
.mem .ov-box {
  position: relative;
  margin: 0;
  text-align: center;
  max-width: 92vw;
}
.mem .ov-box img {
  max-width: 92vw;
  max-height: 76vh;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 30px 90px rgba(0, 0, 0, .65);
}
.mem .ov-box figcaption {
  margin-top: 1.1rem;
  color: #F2E7D7;
  font-size: .95rem;
  letter-spacing: .08em;
  font-family: var(--serif);
}
.mem .ov-x {
  position: absolute;
  top: -16px; right: -16px;
  width: 40px; height: 40px;
  border-radius: 50%;
  background: #FBF7F0;
  color: #4A3F35;
  display: grid; place-items: center;
  font-size: 1.05rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 8px 22px rgba(0, 0, 0, .45);
}
.mem .ov-x:hover { background: #FFFFFF; }

/* ---------------------------------------------------------- 留言 */
.gb-card {
  background: #FFFFFF;
  border: 1px solid #E6DAC8;
  border-radius: 12px;
  padding: 1.1rem 1.3rem;
  margin-bottom: .85rem;
  box-shadow: 0 3px 12px rgba(74, 63, 53, .07);
}
.gb-card .who {
  font-size: .85rem;
  color: #A9714B;
  letter-spacing: .08em;
  margin-bottom: .45rem;
}
.gb-card .who .at {
  float: right;
  color: #B6A794;
  font-size: .72rem;
  letter-spacing: .04em;
}
.gb-card .what {
  font-size: .95rem;
  line-height: 1.9;
  color: #4A3F35;
  white-space: pre-wrap;
}
</style>
"""


# ---------------------------------------------------------------- 画廊渲染

TILTS = [-1.3, 0.9, -0.6, 1.5, -1.0, 0.5, -1.6, 1.1, -0.4, 1.3, -0.9, 0.7]


def group_head_html(group):
    n = len(group["photos"])
    meta = f'{group["weather"]} · {n} 张' if n else group["weather"]
    return (
        '<div class="grp-head">'
        f'<span class="grp-date">{html.escape(group["date"])}</span>'
        f'<span class="grp-title">{html.escape(group["title"])}</span>'
        f'<span class="grp-meta">{html.escape(meta)}</span>'
        "</div>"
    )


def build_hero():
    hero_file = html.escape(P.HERO["file"], quote=True)
    return (
        '<div class="mem">'
        '<div class="hero">'
        f'<img src="app/static/{hero_file}" alt="">'
        '<div class="veil"></div>'
        '<div class="words"><h1>家的记忆</h1>'
        f'<div class="sub">{html.escape(P.HERO["sub"])}</div>'
        "</div></div>"
        '<div class="intro"><span class="orn">❋ ❋ ❋</span>'
        f'{html.escape(P.INTRO)}</div>'
        "</div>"
    )


def build_photo_group(group, gi, start):
    """渲染一组照片墙，返回 (HTML, 下一个可用编号)。

    灯箱用纯 CSS 实现：radio 的 :checked 通过兄弟选择器控制覆盖层显隐。
    硬性要求是覆盖层必须和 radio 同父、且排在所有 radio 之后，所以每次
    必须整组一次性生成。各组用 gi 做 id 前缀，避免跨组撞 id。
    """
    pre = f"g{gi}"
    idx = start
    cards, overlays = [], []

    for photo in group["photos"]:
        idx += 1
        f = html.escape(photo["file"], quote=True)
        cap = html.escape(photo["caption"])
        cards.append(
            f'<label class="card" for="{pre}-lb-{idx}" '
            f'style="--tilt:{TILTS[(idx - 1) % len(TILTS)]}deg">'
            f'<img src="app/static/{f}" alt="" loading="lazy">'
            f'<div class="cap">{cap}</div></label>'
        )
        overlays.append(
            f'<div class="ov" id="{pre}-ov-{idx}">'
            f'<label class="ov-bg" for="{pre}-none"></label>'
            f'<figure class="ov-box"><img src="app/static/{f}" alt="">'
            f'<label class="ov-x" for="{pre}-none">✕</label>'
            f"<figcaption>{cap}</figcaption></figure></div>"
        )

    inputs = "".join(
        f'<input class="lbstate" type="radio" name="lb-{pre}" id="{pre}-lb-{k}">'
        for k in range(start + 1, idx + 1)
    )
    inputs += (
        f'<input class="lbstate" type="radio" name="lb-{pre}" id="{pre}-none" checked>'
    )

    rules = "".join(
        f"#{pre}-lb-{k}:checked ~ #{pre}-ov-{k}"
        "{ display: grid; place-items: center; padding: 3vh 3vw; }"
        for k in range(start + 1, idx + 1)
    )

    doc = (
        f'<div class="mem">{group_head_html(group)}{inputs}'
        f'<div class="grid">{"".join(cards)}</div>'
        f'{"".join(overlays)}<style>{rules}</style></div>'
    )
    return doc, idx


# 全局样式只注入一次；后面每组的 <style> 只补充各自的显隐规则
st.html(CSS)
st.html(build_hero())

_index = 0
for _gi, _group in enumerate(P.GROUPS):
    if _group.get("video"):
        st.html(f'<div class="mem">{group_head_html(_group)}</div>')
        _c = st.columns([1.2, 1, 1.2])
        with _c[1]:
            st.video(str(STATIC / _group["video"]))
        st.html(
            '<div class="mem"><div class="vidcap">'
            f'{html.escape(_group["video_caption"])}'
            f'<span class="vnote">{html.escape(_group.get("video_note", ""))}</span>'
            "</div></div>"
        )
    else:
        _doc, _index = build_photo_group(_group, _gi, _index)
        st.html(_doc)


# ---------------------------------------------------------------- 留言板

st.markdown(
    '<div style="max-width:1180px;margin:3.5rem auto 0;'
    'border-top:1px solid #E6DAC8;"></div>',
    unsafe_allow_html=True,
)

st.subheader(":material/edit_note: 留一句话")

with st.form("guestbook", clear_on_submit=True):
    c1, c2 = st.columns([1, 3])
    gb_name = c1.text_input("怎么称呼你", placeholder="比如：小妹")
    gb_words = c2.text_input("想说点什么", placeholder="写一句就好")
    submitted = st.form_submit_button("写上去", icon=":material/ink_pen:")

if submitted:
    if gb_words.strip():
        add_guestbook(gb_name, gb_words)
        st.rerun()
    else:
        st.warning("至少写一句话吧。")

entries = load_guestbook()
if entries:
    for e in reversed(entries):
        st.markdown(
            '<div class="gb-card">'
            f'<div class="who">{html.escape(e.get("name", "匿名"))}'
            f'<span class="at">{html.escape(e.get("at", ""))}</span></div>'
            f'<div class="what">{html.escape(e.get("words", ""))}</div>'
            "</div>",
            unsafe_allow_html=True,
        )
else:
    st.caption("还没有人留言。")

st.caption(
    "说明：留言存在应用所在机器的 guestbook.json 里。部署到 Streamlit Cloud 后，"
    "硬盘是临时的，应用重启或重新部署时留言会清空。"
)


# ---------------------------------------------------------------- 侧边栏

with st.sidebar:
    st.markdown("### 🌾 家的记忆")
    st.caption(f"{P.total()} 张照片 · {len(P.GROUPS)} 天")

    st.markdown("**目录**")
    for gi, group in enumerate(P.GROUPS):
        st.markdown(
            f"- [{group['date']} · {group['title']}](#g-{gi})",
            unsafe_allow_html=False,
        )

    st.divider()

    music = sorted(
        p for p in STATIC.glob("*") if p.suffix.lower() in (".mp3", ".m4a", ".ogg", ".wav")
    )
    if music:
        st.markdown("**背景音乐**")
        st.audio(str(music[0]))
        if len(music) > 1:
            st.caption(f"（另有 {len(music) - 1} 首，取的是第一首）")
    else:
        st.markdown("**背景音乐**")
        st.caption("把一首 mp3 放进 static/ 目录，这里就会出现播放器。")

    st.divider()
    st.caption("2024 · 夏")
