from typing import Annotated, TypedDict, List
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.tools import tool
from game_site.epic import buy_epic, epic_info
from game_site.gog import buy_gog, gog_info
from game_site.steam import buy_steam, steam_info
from logic.compare import choose_best
from llm.agent import extract_game_name
load_dotenv()

@tool
def extract_game_name_tool(user_input: str) -> str:
    """Extracts the name of the game from user input."""
    return extract_game_name(user_input)

@tool
def best_options_tool(game_name: str) -> dict:
    """Fetches price and source info from Epic, Steam, and GOG, and returns the best option."""
    epic = epic_info(game_name)
    steam = steam_info(game_name)
    gog = gog_info(game_name)
    options = [epic, steam, gog]
    best = choose_best(options)
    return best

@tool
def buy_game_tool(game_name: str) -> str:
    """Extract name from user prompt and fetch the price and choose the best cheap option and buys the game for the user best option for getting games."""
    game_title = extract_game_name(game_name)
    epic = epic_info(game_title)
    steam = steam_info(game_title)
    gog = gog_info(game_title)
    options = [epic, steam, gog]
    best = choose_best(options)
    print(f"Best option for {best['source']}: {best['price']}")
    if best["source"] == "epic":
        buy_epic(game_title)
    elif best["source"] == "steam":
        buy_steam(game_title)
    elif best["source"] == "gog":
        buy_gog(game_title)
    else:
        return "Unknown source"
    return f"Task completed. Successfully purchased.No further action or invoke need until next user input."


tools = [
    Tool.from_function(
        name="extract_game_name",
        func=extract_game_name_tool,
        description="Extracts game name from user input"
    ),
    Tool.from_function(
        name="best_options",
        func=best_options_tool,
        description="Finds the best site for buying the game"
    ),
    Tool.from_function(
        name="buy_game",
        func=buy_game_tool,
        description="Extract name of the game from user prompt and fetch the price and choose the best cheap option and buys the game for the user best option for getting games all in one."
    )
]

llm =  ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # Uses tool calling mode
    verbose=True
)
class State(TypedDict):
    messages: Annotated[list, add_messages]
    purchase_completed: bool


def agent(state: State):
    if state.get("purchase_completed", False):
        return {
            "messages": state["messages"] + [HumanMessage(content="Task already completed. Do you want to buy another game?")],
            "purchase_completed": True
        }
    
    user_message = state["messages"][-1].content
    result = agent_executor.invoke({"input": user_message})
    purchase_done = "Task completed" in result["output"]

    return {
        "messages": state["messages"] + [HumanMessage(content=result["output"])],
        "purchase_completed": purchase_done
    }



graph_builder = StateGraph(State)

graph_builder.add_node("agent", agent)
graph_builder.set_entry_point("agent")
graph_builder.add_edge("agent", END)
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({
        "messages": [{"role": "user", "content": user_input}],
        "purchase_completed": False
    }):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "If Task Completed, then ask user for further input and ask the user for input and no need to invoke any tool with any game name."
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
 