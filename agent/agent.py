from langgraph.graph import StateGraph,END,START
import langchain
import langgraph
from typing import TypedDict
from langchain_core.messages import SystemMessage,AnyMessage,BaseMessage

class AgentState(TypedDict):
    message : AnyMessage
    directory : str
    
