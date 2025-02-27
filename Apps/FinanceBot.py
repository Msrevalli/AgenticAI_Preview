from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

import os

import streamlit as st

api=st.secrets['GROQ_API_KEY']
groq_model = Groq(
    id="llama-3.3-70b-versatile",
    api_key=api,  # Pass API key directly instead of via env var
    # You might need to specify the base URL if required
    # api_base="https://api.groq.com/v1"
)

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=groq_model,
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=groq_model,
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=False,
    markdown=True,
)

# Streamlit app setup
st.title("The Financial Advisor Bot by Sreevalli")
st.write("Enter your query below:")

# Display finance-related sample questions in the sidebar
st.sidebar.header("Sample Finance Questions")
sample_questions = [
    "What is the current stock price of Tesla?",
    "How do I start investing in the stock market?",
    "What are the best investment strategies for beginners?",
    "Can you explain the concept of compound interest?",
    "What is the difference between a stock and a bond?",
    "How do I evaluate a company's financial health?",
    "What are the risks of investing in cryptocurrencies?",
    "What is a mutual fund, and how does it work?",
    "How do interest rates affect the economy?",
    "What is the significance of the S&P 500 index?",
    "How can I diversify my investment portfolio?",
    "What are the tax implications of selling stocks?",
    "What is the role of the Federal Reserve?",
    "How do I read a stock chart?",
    "What are ETFs and how do they work?",
    "What is the importance of diversification in investing?",
    "What are the signs of a market bubble?",
    "How do I assess the value of a stock?",
    "What is the impact of inflation on investments?",
    "What are the characteristics of a bear market?",
    "How do I choose a financial advisor?",
    "What is the significance of the price-to-earnings (P/E) ratio?",
    "How do I create a balanced investment portfolio?",
    "What are the benefits of investing in index funds?",
    "What is the role of venture capital in startups?",
    "How do I invest in foreign markets?",
    "What are the advantages of dollar-cost averaging?",
    "What is the impact of corporate earnings on stock prices?",
    "How do I understand economic indicators?",
    "What are the risks of investing in emerging markets?",
    "How do I protect my investments during market downturns?",
]
for question in sample_questions:
    if st.sidebar.button(question):
        st.session_state.user_query = question  # Set the input box to the selected question

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    st.write(chat)

# Input box for user query
user_query = st.text_input("Query:", value=st.session_state.get('user_query', ''))

if st.button("Submit"):
    if user_query:
        response = agent_team.run(user_query, stream=False)
        st.session_state.chat_history.append(f"You: {user_query}")
        st.session_state.chat_history.append(f"Agent: {response.content}")
        st.write("Response:")
        st.write(response.content)
    else:
        st.warning("Please enter a query.")
