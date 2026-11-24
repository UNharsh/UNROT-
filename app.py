import random
import time
from datetime import datetime
from typing import List

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="UNROT. | Brain Rot Reset Lab",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top, #181c24 0%, #0d0f14 65%);
            color: #f3f4f6;
        }
        .poster-card {
            background: linear-gradient(145deg, #171a22, #101218);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 2.5rem 2rem;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55);
            margin-bottom: 1.5rem;
        }
        .poster-kicker {
            letter-spacing: 0.22em;
            font-size: 0.78rem;
            color: #9ca3af;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }
        .poster-title {
            font-size: clamp(2.2rem, 5vw, 3.8rem);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin: 0.5rem 0 1.5rem 0;
        }
        @keyframes mudSpinClean {
            0% {
                transform: rotate(0deg) scale(0.96);
                background: conic-gradient(#2b1d12, #4a321f, #1f140c, #3b2616, #2b1d12);
                border-color: #5c3d24;
                box-shadow: 0 0 0 6px rgba(74, 50, 31, 0.35), inset 0 0 18px rgba(0, 0, 0, 0.85);
                color: #8c6d53;
                filter: brightness(0.62) contrast(1.25);
            }
            65% {
                transform: rotate(1440deg) scale(1.03);
                background: conic-gradient(#4d3928, #6b7280, #3b2d22, #9ca3af, #4d3928);
                border-color: #9ca3af;
                box-shadow: 0 0 18px rgba(148, 163, 184, 0.25);
                color: #d1d5db;
                filter: brightness(0.88) contrast(1.1);
            }
            100% {
                transform: rotate(2160deg) scale(1.0);
                background: conic-gradient(#38bdf8, #818cf8, #34d399, #38bdf8);
                border-color: #e5e7eb;
                box-shadow: 0 0 28px rgba(56, 189, 248, 0.35);
                color: #ffffff;
                filter: brightness(1.05) contrast(1.0);
            }
        }
        .o-wheel {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 84px;
            height: 84px;
            border-radius: 50%;
            border: 3px solid #e5e7eb;
            font-size: 2.3rem;
            font-weight: 800;
            margin: 0 0.2rem;
            vertical-align: middle;
        }
        .o-muddy-idle {
            background: conic-gradient(#2b1d12, #4a321f, #1f140c, #3b2616, #2b1d12);
            border-color: #5c3d24;
            box-shadow: 0 0 0 6px rgba(74, 50, 31, 0.35), inset 0 0 18px rgba(0, 0, 0, 0.85);
            color: #8c6d53;
            filter: brightness(0.62) contrast(1.25);
        }
        .o-spinning-clean {
            animation: mudSpinClean 1.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
        .frosted-veil {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "unlocked": False,
        "spin_triggered": False,
        "countdown_active": False,
        "countdown_start": 0.0,
        "mode": "15s Feed",
        "brain_index": 50,
        "streak": 0,
        "logs": [],
        "feed_index": 0,
        "sprint_score": 0,
        "sprint_round": 1,
        "sprint_target": "",
        "sprint_options": [],
        "chaos_level": 1,
        "chaos_target": "",
        "chaos_options": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def record_event(mode: str, outcome: str, delta: int) -> None:
    st.session_state.brain_index = max(0, min(100, st.session_state.brain_index + delta))
    if delta > 0:
        st.session_state.streak += 1
    else:
        st.session_state.streak = 0
    st.session_state.logs.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode,
            "outcome": outcome,
            "delta": delta,
            "brain_index": st.session_state.brain_index,
        }
    )


def generate_round(pool: List[str], count: int = 4):
    target = random.choice(pool)
    distractors = [item for item in pool if item != target]
    options = random.sample(distractors, min(count - 1, len(distractors))) + [target]
    random.shuffle(options)
    return target, options


if not st.session_state.unlocked:
    spin_class = "o-spinning-clean" if st.session_state.spin_triggered else "o-muddy-idle"
    st.markdown(
        f"""
        <div class="poster-card">
            <div class="poster-kicker">UNROT. // COGNITIVE RESET SYSTEM</div>
            <div class="poster-title">
                YOUR BRAIN IS N<span class="o-wheel {spin_class}">O</span>T A FEED.
            </div>
            <p style="color:#9ca3af; max-width:560px; margin:0 auto 1.5rem auto;">
                Start with a dark, muddy wheel of passive scrolling. Tap unlock to spin away
                the noise and step into deliberate attention.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡ Spin & Unlock UNROT.", use_container_width=True, type="primary"):
            st.session_state.spin_triggered = True
            st.rerun()
        if st.session_state.spin_triggered:
            st.info("Cleaning the wheel... Click Enter Lab to start your focus session.")
            if st.button("▶ Enter UNROT. Lab", use_container_width=True):
                st.session_state.unlocked = True
                st.session_state.countdown_active = True
                st.session_state.countdown_start = time.time()
                st.rerun()
    st.stop()

if st.session_state.countdown_active:
    elapsed = time.time() - st.session_state.countdown_start
    remaining = max(0, 3 - int(elapsed))
    st.markdown(
        f"""
        <div class="frosted-veil">
            <div style="font-size:0.85rem; letter-spacing:0.18em; color:#cbd5e1;">FROSTED FOCUS VEIL</div>
            <div style="font-size:3rem; font-weight:800; margin:0.4rem 0;">{remaining if remaining > 0 else "GO"}</div>
            <div style="color:#94a3b8;">Pause the impulse scroll. Lock eyes on the signal.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Continue Countdown", use_container_width=True):
            if time.time() - st.session_state.countdown_start >= 3:
                st.session_state.countdown_active = False
            st.rerun()
    with c2:
        if st.button("Skip Veil & Start Now", use_container_width=True):
            st.session_state.countdown_active = False
            st.rerun()
    st.stop()

with st.sidebar:
    st.title("UNROT.")
    st.caption("Python + Streamlit Cognitive Reset Lab")

    st.metric("Brain Index", f"{st.session_state.brain_index} / 100")
    st.metric("Focus Streak", st.session_state.streak)

    modes = [
        "15s Feed",
        "60s Sprint",
        "Chaos Mode",
        "1. Stroop Signal",
        "2. Pattern Echo",
        "3. Odd One Out",
        "4. Number Ladder",
        "5. Word Filter",
        "6. Impulse Brake",
        "Brain Profile",
    ]
    st.session_state.mode = st.radio("Select Module", modes, index=modes.index(st.session_state.mode))

    st.divider()
    if st.button("🔒 Lock Screen Poster", use_container_width=True):
        st.session_state.unlocked = False
        st.session_state.spin_triggered = False
        st.rerun()

st.header(f"UNROT. — {st.session_state.mode}")

if st.session_state.mode == "15s Feed":
    feed_cards = [
        ("SIGNAL #1", "Close one open tab before opening a new one.", "Keep Signal (+6)", +6),
        ("NOISE TRAP #2", "Autoplay queued 12 short clips in a row.", "Resist Bait (+7)", +7),
        ("SIGNAL #3", "Take three slow breaths and name one task for the next 10 minutes.", "Lock In (+6)", +6),
        ("NOISE TRAP #4", "Rage-bait headline trying to hijack your mood.", "Scroll Past (+8)", +8),
    ]
    idx = st.session_state.feed_index % len(feed_cards)
    tag, prompt, action_label, delta = feed_cards[idx]

    st.markdown(f"**{tag}**")
    st.subheader(prompt)
    st.progress((idx + 1) / len(feed_cards))

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(action_label, use_container_width=True, type="primary"):
            record_event("15s Feed", f"Completed {tag}", delta)
            st.session_state.feed_index += 1
            st.rerun()
    with col_b:
        if st.button("Got Distracted (-5)", use_container_width=True):
            record_event("15s Feed", f"Distracted on {tag}", -5)
            st.session_state.feed_index += 1
            st.rerun()

elif st.session_state.mode == "60s Sprint":
    if not st.session_state.sprint_target:
        st.session_state.sprint_target, st.session_state.sprint_options = generate_round(
            ["FOCUS", "STILL", "CLEAR", "SIGNAL", "ANCHOR", "PULSE"]
        )

    st.write(f"**Round {st.session_state.sprint_round}** | **Sprint Points:** {st.session_state.sprint_score}")
    st.info(f"Tap the matching token: **{st.session_state.sprint_target}**")

    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.sprint_options):
        with cols[i % 2]:
            if st.button(opt, key=f"sprint_{st.session_state.sprint_round}_{opt}", use_container_width=True):
                if opt == st.session_state.sprint_target:
                    st.session_state.sprint_score += 10
                    record_event("60s Sprint", f"Matched {opt}", +5)
                else:
                    record_event("60s Sprint", f"Missed {st.session_state.sprint_target}", -4)
                st.session_state.sprint_round += 1
                st.session_state.sprint_target, st.session_state.sprint_options = generate_round(
                    ["FOCUS", "STILL", "CLEAR", "SIGNAL", "ANCHOR", "PULSE"]
                )
                st.rerun()

elif st.session_state.mode == "Chaos Mode":
    if not st.session_state.chaos_target:
        st.session_state.chaos_target, st.session_state.chaos_options = generate_round(
            ["🔺", "🟦", "⭐", "🔶", "🟢", "🟣"]
        )

    st.warning(f"Chaos Intensity Level {st.session_state.chaos_level} — Ignore visual clutter and pick **{st.session_state.chaos_target}**")
    cols = st.columns(2)
    for i, sym in enumerate(st.session_state.chaos_options):
        with cols[i % 2]:
            if st.button(f"{sym}  Select", key=f"chaos_{st.session_state.chaos_level}_{i}_{sym}", use_container_width=True):
                if sym == st.session_state.chaos_target:
                    st.session_state.chaos_level += 1
                    record_event("Chaos Mode", f"Cleared level {st.session_state.chaos_level - 1}", +7)
                else:
                    st.session_state.chaos_level = max(1, st.session_state.chaos_level - 1)
                    record_event("Chaos Mode", "Lost focus in clutter", -5)
                st.session_state.chaos_target, st.session_state.chaos_options = generate_round(
                    ["🔺", "🟦", "⭐", "🔶", "🟢", "🟣"]
                )
                st.rerun()

elif st.session_state.mode.startswith(("1.", "2.", "3.", "4.", "5.", "6.")):
    game_name = st.session_state.mode

    if game_name.startswith("1."):
        st.write("Select the word **BLUE** even if the label tries to trick you.")
        choices = ["RED", "BLUE", "GREEN", "YELLOW"]
        correct = "BLUE"
    elif game_name.startswith("2."):
        st.write("Complete the sequence: **2, 4, 8, 16, ?**")
        choices = ["24", "30", "32", "64"]
        correct = "32"
    elif game_name.startswith("3."):
        st.write("Which item does **not** belong with the others (all others are data structures)?")
        choices = ["Stack", "Queue", "Tree", "Loop"]
        correct = "Loop"
    elif game_name.startswith("4."):
        st.write("Pick the **largest** value.")
        choices = ["3/4", "0.72", "68%", "0.81"]
        correct = "0.81"
    elif game_name.startswith("5."):
        st.write("Which word is an **anagram** of **LISTEN**?")
        choices = ["SILENT", "SIMPLE", "SILVER", "SISTER"]
        correct = "SILENT"
    else:
        st.write("Impulse Brake: Do **NOT** click 'CLICK ME NOW' — choose **HOLD STEADY**.")
        choices = ["CLICK ME NOW", "FREE REWARD", "HOLD STEADY", "FLASH OFFER"]
        correct = "HOLD STEADY"

    cols = st.columns(2)
    for i, choice in enumerate(choices):
        with cols[i % 2]:
            if st.button(choice, key=f"mg_{game_name}_{choice}", use_container_width=True):
                if choice == correct:
                    st.success("Sharp response! Brain Index increased.")
                    record_event(game_name, f"Correct: {choice}", +6)
                else:
                    st.error(f"Not quite — expected '{correct}'.")
                    record_event(game_name, f"Incorrect: {choice}", -4)

elif st.session_state.mode == "Brain Profile":
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Brain Index", f"{st.session_state.brain_index}/100")
    c2.metric("Active Streak", st.session_state.streak)
    c3.metric("Logged Sessions", len(st.session_state.logs))

    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)
        st.line_chart(df["brain_index"], height=240)
        st.dataframe(df, use_container_width=True)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Export Telemetry CSV",
            data=csv_bytes,
            file_name="unrot_telemetry.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info("Complete a round in 15s Feed, 60s Sprint, Chaos Mode, or any mini-game to generate telemetry.")
