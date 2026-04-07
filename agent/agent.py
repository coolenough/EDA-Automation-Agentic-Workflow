from langgraph.graph import StateGraph,END,START
from langgraph.graph.message import add_messages
import langchain
import langgraph
from typing import TypedDict,Annotated
from langchain_core.messages import SystemMessage,AnyMessage,BaseMessage

class AgentState(TypedDict):
    message : Annotated[BaseMessage, add_messages]
    directory : str
    
