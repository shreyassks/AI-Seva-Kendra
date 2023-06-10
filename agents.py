"""here we define our agent class and their actions with tools
"""

from tools import Tools
from langchain.agents import AgentType
from langchain.agents import AgentExecutor # will be used for custom agents
from langchain.agents import initialize_agent




class ActionAgent():
		
    def _init_(self,llm):
        self.llm = llm
        self.agent = self.create_agent()

    def create_agent(self):    
        """
        Returns: AgentExecutor 
        
        AgnetType-> Zero-shot means the agent functions on the current action only — it has no memory.
                    ReAcT - Reasoning and Action steps, that LLM could cycle through
                    Enabling a multi-step process for identifying answers.
        """
        agent_executor = initialize_agent(self.fetch_tools(), self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        return agent_executor

    def fetch_tools(self):
        self.tools= Tools(self.llm).list_tools()
        return self.tools

    def run(self, input):
        return self.agent.run(input=input)