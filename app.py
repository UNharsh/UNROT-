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
            background: conic-gradient(#2b1d12, #4a321
