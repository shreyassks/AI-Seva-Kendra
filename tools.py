"""here we define tools that are needed by an agent #test
"""
from langchain.agents import load_tools
from langchain.agents.tools import Tool
from langchain.utilities import PythonREPL
from pydantic import BaseModel, Field
from langchain import LLMMathChain
from langchain import SerpAPIWrapper
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.document_loaders import DirectoryLoader
from langchain.chat_models import ChatOpenAI
from math import radians, cos, sin, asin, sqrt
import requests
import json
import os

search = SerpAPIWrapper()
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
def setup_pdf_parser():
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")

    # Data Ingestion
    pdf_loader = DirectoryLoader('static/', glob="**/*.pdf")

    loaders = [pdf_loader]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    # Chunk and Embeddings
    text_splitter = CharacterTextSplitter(chunk_size=2100, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)

    memory = ConversationSummaryBufferMemory(
        llm=llm,
        output_key='answer',
        memory_key='chat_history',
        return_messages=True)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4, "include_metadata": True})

    # Initialise Langchain - Conversation Retrieval Chain
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, return_source_documents=True,
                                                memory=memory, chain_type="stuff", get_chat_history=lambda h : h)

    return qa



# Function to calculate distance between two coordinates
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return round(c * r,2)

def get_location_coordinates(location):
    """Get the latitude and longitude of a location using Google Maps API"""
    #TODO: implement this function
    # async with aiohttp.ClientSession() as session:
    #     parameters = {
    #         "address": location,
    #         "key": API_KEY
    #     }
    
    #     async with session.get("https://maps.googleapis.com/maps/api/geocode/json", params=parameters) as response:

    # latitude = data['coordinates']['lat']
    # longitude = data['coordinates']['lng']
    latitude = 12.9715987  
    longitude = 77.5945627
    return latitude, longitude

def fetch_nearest_location(location,longitude, latitude):
    """Fetch the nearest location using SerpAPI"""
    params = {
        "engine": "google_maps",
        "q": "aadhar near " + location, #TODO: take aadhar as variable
        "google_domain": "google.com",
        "api_key": SERPAPI_KEY,
    }

    response = requests.get("https://serpapi.com/search", params)
    #print(response.json())
    data = response.json()
    
    latitude_result = data["local_results"][0]['gps_coordinates']['latitude']
    longitude_result = data["local_results"][0]['gps_coordinates']['longitude']
    distance = haversine(longitude, latitude, longitude_result, latitude_result)
    rounded_distance = round(distance, 2)

    return data['local_results'][0]['title'],rounded_distance

# Defining schema for llm math chain as an example
class CalculatorInput(BaseModel):
    question: str = Field()


class Tools():

    def __init__(self,llm) :
        self.llm = llm
        self.qa = setup_pdf_parser()
        self.tools = [
            Tool(
               name="python_repl",
               description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
                func=self.python_repl()
            ),
            Tool(
                name="Calculator",
                func=self.llm_math(),
                description="A calculator. Use this to do math. Input should be a math question. For example, `What is 2+2?`",
                args_schema=CalculatorInput
            ),
            Tool(
                name="Search",
                func=search.run,
                description="Useful for when you need to search internet.Output must be in hindi devanagari script"
                ),
            Tool(
                name="Aadhar UADAI Information Tool",
                func=self.aadhar_uadai_tool,
                description="Useful for when you need to answer questions about aadhar and UADAI.\
                Example: 'What is the process to get aadhar card?'\
                Output must be in hindi devanagari script",
                ),
            Tool(
                name="Distance on Map",
                func=self.distance_map,
                description="Useful for when you need to find the nearest aadhar center.\
                Example: 'मैं indiranagar,bangalore में रहता हूँ, निकटतम आधार केंद्र कहाँ है?\
                Input expects address in english"
            )
        ]


    def python_repl(self):
        python_repl = PythonREPL()
        return python_repl.run

    def llm_math(self):
        llm_math_chain = LLMMathChain(llm=self.llm, verbose=True)
        return llm_math_chain.run
    
    def aadhar_uadai_tool(self, prompt):
        response = self.qa({"question": prompt})
        return response["answer"]
    
    def distance_map(self, address):
        latitude, longitude = get_location_coordinates(address)
        answer,distance=fetch_nearest_location(address, longitude, latitude)
        
        return f"निकटतम आधार केंद्र है: {answer} , {distance} km दूरी पर:"

    def list_tools(self):
        return self.tools
