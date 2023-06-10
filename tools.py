"""here we define tools that are needed by an agent
"""
from langchain.agents import load_tools
from langchain.agents.tools import Tool
from langchain.utilities import PythonREPL
from pydantic import BaseModel, Field
from langchain import LLMMathChain
from langchain.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
os.environ["SERPER_API_KEY"] = SERPAPI_KEY
search = GoogleSerperAPIWrapper()


# Defining schema for llm math chain as an example
class CalculatorInput(BaseModel):
    question: str = Field()

class Tools():

    def __init__(self,llm) :
        self.llm = llm

        self.tools = [
            Tool(
                name="AWS Executor",
                func=self.aws_executor,
                description="Use this tool for interacting with AWS"
            ),
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
                description="Useful for when you need to answer questions about current events. Does internet search.You should ask targeted questions."
                )
        ]

    def aws_executor(self, input):
        #for s3 etc
        pass

    def python_repl(self):
        python_repl = PythonREPL()
        
        return python_repl.run

    def llm_math(self):
        llm_math_chain = LLMMathChain(llm=self.llm, verbose=True)
        return llm_math_chain.run
    
    def list_tools(self):
        return self.tools
