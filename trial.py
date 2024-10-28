import os
import json
import requests
import openai
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from threading import Thread
import queue

# Import the key CrewAI classes
from crewai import Agent, Task, Crew

# Load environment variables (OpenAI API key)
load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit UI Setup
st.set_page_config(page_title="Career & Skills Guidance Portal", layout="wide")
st.title("Career Guidance & Skills Development Portal")

# Disclaimer
with st.expander("IMPORTANT NOTICE:"):
    st.write("""
    IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)

# Create the web search tool
from crewai_tools import WebsiteSearchTool
tool_websearch = WebsiteSearchTool("https://www.myskillsfuture.gov.sg/")

# Create Agents
agent_scraper = Agent(
    role="Data Scraper",
    goal="Scrape up-to-date and relevant content from SkillsFuture website and related resources.",
    backstory="You're responsible for gathering all the necessary information from public sources and preparing it for further analysis.",
    allow_delegation=False,
    verbose=True
)

agent_analyzer = Agent(
    role="Information Analyzer",
    goal="Analyze scraped data to identify relevant content that addresses user queries.",
    backstory="You will identify the most useful information from scraped data to help answer user queries related to upskilling or career guidance.",
    allow_delegation=False,
    verbose=True
)

agent_responder = Agent(
    role="Response Generator",
    goal="Generate detailed responses for user queries based on the relevant data.",
    backstory="You will generate a comprehensive, user-friendly response using the relevant information provided by the Information Analyzer.",
    allow_delegation=False,
    verbose=True
)

# Define Tasks
task_scrape = Task(
    description="Scrape general data from SkillsFuture and related portals.",
    expected_output="A collection of data from SkillsFuture including headings, paragraphs, and lists of information.",
    agent=agent_scraper,
    tools=[tool_websearch],
    async_execution=True
)

task_analyze = Task(
    description="Analyze the scraped data to find content relevant to the user's query.",
    expected_output="Relevant sections from the scraped data that help address the user's query.",
    agent=agent_analyzer,
    async_execution=False
)

task_respond = Task(
    description="Generate a comprehensive response to the user query based on the analyzed data.",
    expected_output="A detailed, friendly response that helps the user understand their upskilling or career guidance options.",
    agent=agent_responder,
    async_execution=False
)

# Create Crew
crew = Crew(
    agents=[agent_scraper, agent_analyzer, agent_responder],
    tasks=[task_scrape, task_analyze, task_respond],
    verbose=True
)

# Step 4: Main Query Handling
user_query = st.text_input("Enter your question:", placeholder="E.g., 'What courses are available for data science?'")
if user_query:
    st.write("Searching for relevant information...")

    # Running the Crew to handle user query
    result = crew.kickoff(inputs={"topic": user_query})

    # Displaying the output
    if result and 'output' in result:
        st.subheader(result['output']['task_respond'])
    else:
        st.write("No relevant information found for your query.")

# Display Raw Data (Optional)
if st.checkbox("Show Raw Data"):
    st.write("Scraped Information:")
    st.json(result.get('output', {}).get('task_scrape', "No data available."))
