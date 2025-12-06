📈 Financial AI Agent – Chat + Real-Time Tools

An AI-powered interactive platform designed to improve digital financial literacy through a conversational chatbot, real-time stock market data, and investment calculators for Mutual Funds and SIP.

🚀 Overview

The Financial AI Agent combines the power of AI and financial computation into an easy-to-use Streamlit application.
It helps users learn financial concepts, check stock prices, calculate mutual fund returns, and estimate SIP growth — all through a simple interface.

This tool is designed for students, beginners, and anyone interested in understanding finance without needing complex knowledge.

✨ Features
🧠 AI Chatbot (OpenRouter LLM)

Ask any finance-related question in natural language

Simple, beginner-friendly explanations

Avoids personalized investment advice

Works using OpenRouter’s LLM API

📊 Real-Time Stock Price Finder

Fetches real-time prices from Yahoo Finance

Supports NSE, BSE, NASDAQ, NYSE

Visualizes historical closing price charts

Powered by yfinance and matplotlib

💰 Mutual Fund Return Calculator

Computes Absolute Return

Computes CAGR (Compound Annual Growth Rate)

Uses user-provided NAV values + dates

Helps users understand return performance easily

📈 SIP Future Value Calculator

Calculates future value of monthly SIP

Shows:

Total invested amount

Final value

Estimated gain

Uses the standard compounding formula

🛠️ Tech Stack

Python 3.x

Streamlit – frontend interface

OpenRouter API – AI chatbot

yfinance – stock market data

NumPy & Pandas – calculations

Matplotlib – charts

Dataclasses – clean structured input handling

📥 Installation
1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Install dependencies
pip install -r requirements.txt


If you don’t have a requirements file, install manually:

pip install streamlit openai yfinance pandas numpy matplotlib

🔑 Before Running

You will need an OpenRouter API Key.
Create a free key at: https://openrouter.ai

▶️ Run the Application
streamlit run FinancialAgentApp.py

📚 How to Use
1. Enter your API key

The app will prompt you for your OpenRouter API key.

2. Ask questions in chat

Examples:

“What is SIP?”

“Explain CAGR”

“Difference between mutual fund and stock?”

3. Use Quick Tools

Tabs include:

Stock Finder

Mutual Fund Calculator

SIP Calculator

Each tool is interactive and easy to use.

🧵 Project Structure
│── FinancialAgentApp.py     # Main Streamlit app
│── README.md                # Project documentation
│── screenshots/             # (Optional) Images of UI
│── requirements.txt         # Dependencies

🧪 Key Calculations
📌 Absolute Return
((NAV_end - NAV_start) / NAV_start) * 100

📌 CAGR
((NAV_end / NAV_start)^(1/years)) - 1

📌 SIP Future Value
FV = P * [((1 + r)^n - 1)/r] * (1 + r)

🔮 Future Enhancements

Multilingual chatbot

User portfolio tracking

Risk assessment tools

Budget planner

Deployment on cloud (Streamlit Cloud / Render)

News sentiment analysis for stocks

🧑‍💻 Developed By

Abhinav M & Siddharth G
MSc Statistics – Data Science
Vishwakarma University, Pune

📝 License

This project is open-source and free to use for educational purposes.
