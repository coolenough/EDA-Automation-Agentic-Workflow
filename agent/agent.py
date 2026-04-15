from langgraph.graph import StateGraph,END,START
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import TypedDict,Annotated
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage,AnyMessage,BaseMessage
from tools.tools import agent_tools
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

model = model.bind_tools(tools = agent_tools)

graph = StateGraph(AgentState)

def AgentCall(state : AgentState) -> AgentState:
    state["message"] = model.invoke(f" {SYSTEM_PROMPT} , {state['message']} ").content
    return state

def passon(state : AgentState) -> AgentState:
    return state

def to_continue(state : AgentState) ->str:
  message = state["message"]
  last_message = message[-1]
  if not last_message.tool_calls:
    return "end"
  else:
    return "continue"


# passon -> AgentCall -> tools -> output

tools_node = ToolNode(tools = agent_tools)

graph.add_node("passon" , passon)
graph.add_node("Model" , AgentCall)
graph.add_node("tools" , tools_node)

graph.set_entry_point("passon")
graph.add_edge("passon","Model")
graph.add_conditional_edges("Model" , to_continue , {
   "end" : END,
   "continue" : "tools"
})

graph.add_edge("tools" , "Model")

app = graph.compile()

if __name__ == "__main__":
    x = app.get_graph().draw_mermaid_png()
    
    with open("architecture.png" , "wb") as f:
        f.write(x)
    
