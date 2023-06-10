"""main file to call agents and execute tasks
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import  PromptTemplate
from agents import ActionAgent

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_KEY
os.environ["SERPAPI_API_KEY"] = SERPAPI_KEY


llm = OpenAI(openai_api_key=OPENAI_KEY,temperature=0.9)

action_agent= ActionAgent(llm) 


#print(action_agent.agent.llm_chain.prompt.template) #check template

prompt = st.text_input('Enter your goal here')
if prompt:
    st.write(action_agent.run(prompt))