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
os.environ["SERPER_API_KEY"] = SERPAPI_KEY


llm = OpenAI(openai_api_key=OPENAI_KEY,temperature=0.9)

action_agent= ActionAgent(llm) 


#print(action_agent.agent.llm_chain.prompt.template) #check template


input_text = st.text_input("Write your goal:")
button_clicked = st.button('DEPLOY AGENT')


if button_clicked:

    prompt=input_text

    with st.spinner('Agents at Work...'):
        st.image('static/agent.png')
        #st.image('static/talk.gif')
        st.write(action_agent.run(prompt))