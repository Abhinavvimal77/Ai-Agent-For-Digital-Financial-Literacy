"""
FinancialAgentApp.py
A single-file Streamlit app that implements a simple Financial AI Agent (chatbot)
and tools:
 - Mutual Fund return calculator (lump-sum and SIP)
 - Stock price finder using yfinance (current price + historical chart)

Requirements:
 pip install streamlit openai yfinance pandas numpy matplotlib

Usage:
 Run with:
 streamlit run FinancialAgentApp.py
"""

import os
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from openai import OpenAI

# ----------------------------- API Key Input -----------------------------

st.title("📈 Financial AI Agent — Chat + Tools")

api_key = st.text_input("🔑 Enter your **OpenRouter API Key**:", type="password")

if api_key:
    os.environ["OPENROUTER_API_KEY"] = api_key
    st.success("✅ OpenRouter API key set successfully!")
else:
    st.warning("⚠️ Please enter your OpenRouter API key to continue.")
    st.stop()

# ----------------------------- Helpers ---------------------------------

@dataclass
class MFInputs:
    nav_start: float
    nav_end: float
    start_date: str
    end_date: str


def cagr(start_value: float, end_value: float, years: float) -> float:
    return (end_value / start_value) ** (1.0 / years) - 1.0


def days_to_years(days: int) -> float:
    return days / 365.25


def parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")


def mf_lumpsum_return(nav_start: float, nav_end: float, start_date: str, end_date: str) -> dict:
    start_dt, end_dt = parse_date(start_date), parse_date(end_date)
    days = (end_dt - start_dt).days
    years = days_to_years(days)
    abs_return = (nav_end - nav_start) / nav_start
    cagr_val = cagr(nav_start, nav_end, years) if years > 0 else np.nan
    return {
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "absolute_return_pct": abs_return * 100,
        "cagr_pct": cagr_val * 100,
    }


def sip_future_value(monthly: float, annual_rate_pct: float, months: int) -> float:
    r = annual_rate_pct / 100.0 / 12.0
    if r == 0:
        return monthly * months
    return monthly * (((1 + r) ** months - 1) / r) * (1 + r)

# ----------------------------- Chatbot ---------------------------------

SYSTEM_PROMPT = (
    "You are a helpful financial assistant. You may provide educational information, calculations, and explanations. "
    "Do not offer personalised financial advice or recommend specific buy/sell actions. "
    "If asked for personal recommendations, politely refuse and suggest general principles."
)


def chat_with_openrouter(prompt: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    """Chat wrapper using OpenRouter API endpoint"""
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=800,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error calling OpenRouter: {e}]"


def mock_chat_response(prompt: str) -> str:
    return (
        "I can help compute returns, fetch stock prices, and explain financial concepts. "
        "Try: 'stock: AAPL', 'mf lumpsum: 100 150 2020-01-01 2023-01-01', or 'sip: 5000 12 24'"
    )

# ----------------------------- Streamlit UI -----------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chatbot")
    user_input = st.text_area("Ask the agent anything (or use tool commands)", height=150)
    run_chat = st.button("Send")

    if run_chat and user_input.strip():
        lower = user_input.strip().lower()

        if lower.startswith("stock:"):
            symbol = user_input.split(":", 1)[1].strip().upper()
            st.info(f"Fetching latest price for {symbol}...")
            data = yf.Ticker(symbol).history(period="5d")
            if not data.empty:
                price = data['Close'].iloc[-1]
                st.success(f"{symbol} latest close: {price:.2f}")
                st.line_chart(data['Close'])
            else:
                st.error("No data found for that ticker")

        elif lower.startswith("mf lumpsum:"):
            try:
                parts = user_input.split(":", 1)[1].strip().split()
                nav_start, nav_end, sdate, edate = float(parts[0]), float(parts[1]), parts[2], parts[3]
                res = mf_lumpsum_return(nav_start, nav_end, sdate, edate)
                st.write(res)
            except Exception:
                st.error("Invalid format. Use: mf lumpsum: 100 150 2020-01-01 2023-01-01")

        else:
            with st.spinner("Contacting OpenRouter..."):
                reply = chat_with_openrouter(user_input, api_key)
            st.markdown("**Agent:**")
            st.write(reply)

    st.markdown("---")
    st.header("Quick Tools")
    tool_tab = st.tabs(["Stock Finder", "Mutual Fund Calculator", "SIP Calculator"])

# ----------------------------- Tools ---------------------------------

# Stock Finder Tab
# Stock Finder Tab
with tool_tab[0]:
    st.subheader("Stock price & chart (yfinance)")

    # --- Added Market Selection ---
    market = st.selectbox(
        "Select Market / Exchange",
        ["NSE (India)", "BSE (India)", "NASDAQ (US)", "NYSE (US)", "Other"],
        index=0,
    )

    sym = st.text_input("Ticker symbol (e.g. TCS, AAPL)", value="TCS")

    # Map the selected market to Yahoo Finance ticker suffix
    market_suffix = {
        "NSE (India)": ".NS",
        "BSE (India)": ".BO",
        "NASDAQ (US)": "",
        "NYSE (US)": "",
        "Other": "",
    }.get(market, "")

    period = st.selectbox("History period", ["1d", "5d", "1mo", "6mo", "1y", "5y"], index=4)

    if st.button("Get Price", key="get_price"):
        # Append suffix if needed
        ticker_symbol = sym.strip().upper() + market_suffix
        st.info(f"Fetching data for **{ticker_symbol}** from {market}...")

        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period)

        if hist.empty:
            st.error("No data found. Check the ticker symbol or try a different market/period.")
        else:
            latest_close = hist['Close'].iloc[-1]
            st.metric(label=f"{ticker_symbol} latest close", value=f"{latest_close:.2f}")
            fig, ax = plt.subplots()
            ax.plot(hist.index, hist['Close'])
            ax.set_title(f"{ticker_symbol} Close Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            st.pyplot(fig)

            st.pyplot(fig)

# Mutual Fund Calculator Tab
with tool_tab[1]:
    st.subheader("Lump-sum return calculator")
    col_a, col_b = st.columns(2)
    with col_a:
        nav_start = st.number_input("NAV at start", min_value=0.0, value=100.0, format="%.4f")
        start_date = st.date_input("Start date", value=pd.to_datetime("2020-01-01"))
    with col_b:
        nav_end = st.number_input("NAV at end", min_value=0.0, value=150.0, format="%.4f")
        end_date = st.date_input("End date", value=pd.to_datetime("2023-01-01"))

    if st.button("Calculate MF Return"):
        sdate_str, edate_str = start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
        res = mf_lumpsum_return(nav_start, nav_end, sdate_str, edate_str)
        st.write("**Results**")
        st.write(f"Period: {res['start_date']} to {res['end_date']} — {res['days']} days")
        st.metric("Absolute return (%)", f"{res['absolute_return_pct']:.2f}%")
        st.metric("CAGR (%)", f"{res['cagr_pct']:.2f}%")

# SIP Calculator Tab
with tool_tab[2]:
    st.subheader("SIP future value calculator")
    monthly = st.number_input("Monthly SIP amount", min_value=0.0, value=5000.0)
    annual_rate = st.number_input("Expected annual return (%)", min_value=0.0, value=12.0)
    years = st.number_input("Years", min_value=0.1, value=3.0)
    months = int(years * 12)
    if st.button("Calculate SIP"):
        fv = sip_future_value(monthly, annual_rate, months)
        invested = monthly * months
        gain = fv - invested
        st.write(f"Future value after {years} years ({months} months): {fv:,.2f}")
        st.metric("Total invested", f"{invested:,.2f}")
        st.metric("Estimated gain", f"{gain:,.2f}")

# ----------------------------- Footer ----------------------------------

st.markdown("---")
st.caption("Made By Siddharth G using Open Router.")
