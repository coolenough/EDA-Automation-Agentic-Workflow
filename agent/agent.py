from langgraph.graph import StateGraph,END,START
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import langchain
import langgraph
from typing import TypedDict,Annotated
from langchain_core.messages import SystemMessage,AnyMessage,BaseMessage
from tools import tools
import dotenv
import os
from agent.prompts import SYSTEM_PROMPT

dotenv.load_dotenv()

class AgentState(TypedDict):
    message : Annotated[BaseMessage, add_messages]
    directory : str

model = ChatOpenAI(
    model = os.getenv("model" , ""),
    base_url = os.getenv("model_base_url",""),
    api_key = os.getenv("model_api_key","")
)

graph = StateGraph(AgentState)

def AgentCall(state : AgentState) -> AgentState:
    state["message"] = model.invoke(f" {SYSTEM_PROMPT} , {state['message']} ").content
    return state


graph.add_node(AgentCall , "Model")
    
