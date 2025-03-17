docs="https://docs.python.org/3.12/"
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.agent import Agent
from agno.models.google import Gemini
from agno.vectordb.lancedb import LanceDb
from agno.embedder.google import GeminiEmbedder
from agno.vectordb.search import SearchType
from agno.tools.website import WebsiteTools
from rich import print
from pathlib import Path
from agno.agent import Agent
from agno.media import Image
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import pyautogui
import time
import streamlit as st
from beeply.notes import *
ting=beeps()
#from agno.tools.crawl4ai import Crawl4aiTools
knowledge_base = WebsiteKnowledgeBase(
    urls=[docs],
    # Number of links to follow from the seed URLs
    max_links=10,
    vector_db=LanceDb(
                uri="/tmp/lancedb",
                table_name="website_documents",
                embedder=GeminiEmbedder(dimensions=1536),
                search_type=SearchType.keyword
    ),
)
agent = Agent(
    model=Gemini("gemini-2.0-flash-exp"),
    knowledge=knowledge_base,
    debug_mode=True,
    search_knowledge=True,
    tools=[DuckDuckGoTools()], show_tool_calls=True,
    add_history_to_messages=True,
    description="You are a python tutor that helps user learn python at any level from beginner to intermediate to advanced, your goal is to help the user become a good developer",
    instructions=[
        "Ask the user about their skill level and experience with python",
        "Ask what the user would like to learn about",
        "Teach the user one concept at a time starting with the first",
        "Ask a random easy question related to the concept you taught as you continue to make sure the user is engaged",
        "If it required give links to the python docs",
        "If the user wants to learn something related to python not in data base search the web with duckduckgo to help the user",
        "Recommend relevant communities, forums, and study groups for peer learning and networking.",
        "Recommend high-quality YouTube videos and online courses that match the user's learning style and proficiency level.",
        "Break down complex topics into digestible chunks and provide step-by-step explanations with practical examples.",
        "Create personalized assignments with clear milestones, deadlines, and progress tracking.",
        "Ask the user to use the active watch mode if they need active help as they code, it'll enable you to watch their screen"
    ]
)
st.title("PyTeacher AI")
on = st.toggle("Active Watch mode")
if on:
    st.write("Actively watching your screen now, taking screenshot every 30 seconds, do not open sensitive info")
    print("taking screenshot in 10 seconds")
    while on:
        ting.hear('A')
        for i in range(30):
            print(f"taking screenshot in {30-i} seconds")
            time.sleep(1)
        image1 = pyautogui.screenshot("image1.png")
        ting.hear('A_')
        image_path = Path(__file__).parent.joinpath("image1.png")
        with st.chat_message("assistant"):
            reply=agent.run("look at this screenshot and give feedback on my code like a teacher does without too much hand holding",
            images=[Image(filepath=image_path)])
            stream=True,
            response = st.write(reply.content)
            st.session_state.messages.append({"role": "assistant", "content": reply.content})
        time.sleep(30)
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
            reply=agent.run(prompt)
            stream=True,
            response = st.write(reply.content)
    st.session_state.messages.append({"role": "assistant", "content": reply.content})