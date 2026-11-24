import random
import time
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="UNROT. | Brain Rot Reset Lab",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Visual Styling ---
st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1b2232 0%, #0d1017 58%, #07090d 100%);
            color: #f3f4f6;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        .poster-shell {
            background: linear-gradient(160deg, rgba(25, 31, 45, 0.92), rgba(12, 15, 22, 0.96));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 28px;
            padding: 3rem 2rem 2.5rem 2rem;
            text-align: center;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            margin-bottom: 1.5rem;
        }
        .poster-tag {
            display: inline-block;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.28);
            color: #7dd3fc;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        .poster-headline {
            font-size: clamp(2.1rem, 5.2vw, 4rem);
            font-weight: 900;
            letter-spacing: -0.035em;
            line-height: 1.12;
            margin: 0.4rem 0 1.4rem 0;
            color: #ffffff;
        }
        .poster-sub {
            color: #9ca3af;
            font-size: 1.02rem;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }
        @keyframes mudSpinClean {
            0% {
                transform: rotate(0deg) scale(0.95);
                background: conic-gradient(#2a1b10, #4d321e, #1a1009, #3c2616, #2a1b10);
                border-color: #634126;
                box-shadow: 0 0 0 7px rgba(77, 50, 30, 0.35), inset 0 0 20px rgba(0, 0, 0, 0.9);
                color: #967458;
                filter: brightness(0.65) contrast(1.25);
            }
            65% {
                transform: rotate(1440deg) scale(1.04);
                background: conic-gradient(#4c3827, #64748b, #382a20, #94a3b8, #4c3827);
                border-color: #cbd5e1;
                box-shadow: 0 0 22px rgba(148, 163, 184, 0.3);
                color: #e2e8f0;
                filter: brightness(0.92) contrast(1.08);
            }
            100% {
                transform: rotate(2160deg) scale(1.0);
                background: conic-gradient(#38bdf8, #818cf8, #34d399, #38bdf8);
                border-color: #f8fafc;
                box-shadow: 0 0 32px rgba(56, 189, 248, 0.42);
                color: #ffffff;
                filter: brightness(1.06) contrast(1.0);
            }
        }
        .o-orb {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 82px;
            height: 82px;
            border-radius: 50%;
            border: 3px solid #e2e8f0;
            font-size: 2.2rem;
            font-weight: 900;
            margin: 0 0.25rem;
            vertical-align: middle;
        }
        .o-muddy {
            background: conic-gradient(#2a1b10, #4d321e, #1a1009, #3c2616, #2a1b10);
            border-color: #634126;
            box-shadow: 0 0 0 7px rgba(77, 50, 30, 0.35), inset 0 0 20px rgba(0, 0, 0, 0.9);
            color: #967458;
            filter: brightness(0.65) contrast(1.25);
        }
        .o-clean {
            animation: mudSpinClean 1.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
        .veil-panel {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 24px;
            padding: 2.6rem 2rem;
            text-align: center;
            margin: 1.5rem auto;
            max-width: 680px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }
        .veil-count {
            font-size: 4rem;
            font-weight: 900;
            line-height: 1;
            margin: 0.75rem 0;
            color: #38bdf8;
        }
        .feed-card {
            background: linear-gradient(145deg, rgba(24, 30, 44, 0.9), rgba(14, 17, 26, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.11);
            border-radius: 22px;
            padding: 2rem;
            margin: 1rem 0 1.25rem 0;
        }
        .badge-signal {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 8px;
            background: rgba(52, 211, 153, 0.14);
            color: #6ee7b7;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 0.7rem;
        }
        .badge-noise {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 8px;
            background: rgba(251, 113, 133, 0.14);
            color: #fda4af;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 0.7rem;
        }
        .clutter-banner {
            background: repeating-linear-gradient(
                -45deg,
                rgba(245, 158, 11, 0.14),
                rgba(245, 158, 11, 0.14) 12px,
                rgba(239, 68, 68, 0.14) 12px,
                rgba(239, 68, 68, 0.14) 24px
            );
            border: 1px dashed rgba(251, 191, 36, 0.55);
            border-radius: 16px;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- State Initialization ---
def init_state() -> None:
    defaults: Dict[str, object] = {
        "unlocked": False,
        "spin_triggered": False,
        "countdown_active": False,
        "countdown_start": 0.0,
        "mode": "15s Feed",
        "brain_index": 50,
        "streak": 0,
        "logs": [],
        "feed_step": 0,
        "sprint_active": False,
        "sprint_start": 0.0,
        "sprint_duration": 60,
        "sprint_score": 0,
        "sprint_round": 1,
        "sprint_target": "",
        "sprint_options": [],
        "chaos_level": 1,
        "chaos_target": "",
        "chaos_options": [],
        "game_round": 1,
        "game_score": 0,
        "game_question": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# --- Core Helpers ---
def record_event(mode: str, outcome: str, delta: int) -> None:
    st.session_state.brain_index = max(0, min(100, int(st.session_state.brain_index) + delta))
    if delta > 0:
        st.session_state.streak = int(st.session_state.streak) + 1
    else:
        st.session_state.streak = 0
    logs: List[Dict[str, object]] = list(st.session_state.logs)
    logs.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode,
            "outcome": outcome,
            "delta": delta,
            "brain_index": st.session_state.brain_index,
        }
    )
    st.session_state.logs = logs


def pick_options(pool: List[str], count: int = 4) -> Tuple[str, List[str]]:
    target = random.choice(pool)
    distractors = [x for x in pool if x != target]
    opts = random.sample(distractors, min(count - 1, len(distractors))) + [target]
    random.shuffle(opts)
    return target, opts


def build_minigame_question(game_mode: str, round_num: int) -> Tuple[str, List[str], str, str]:
    if game_mode.startswith("1."):
        bank = [
            ("Tap the word **BLUE** (ignore decoy labels).", ["RED", "BLUE", "GREEN", "YELLOW"], "BLUE", "Stroop inhibition"),
            ("Tap the word **SIGNAL** (ignore noise words).", ["NOISE", "SIGNAL", "STATIC", "DRIFT"], "SIGNAL", "Stroop inhibition"),
            ("Tap the word **CALM** (stay sharp).", ["RUSH", "PANIC", "CALM", "BLUR"], "CALM", "Stroop inhibition"),
        ]
    elif game_mode.startswith("2."):
        bank = [
