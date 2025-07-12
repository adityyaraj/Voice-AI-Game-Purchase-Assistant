from livekit.agents import function_tool, Agent, RunContext
from game_site.epic import buy_epic, epic_info
from game_site.gog import buy_gog, gog_info
from game_site.steam import buy_steam, steam_info
from logic.compare import choose_best
from llm.agent import extract_game_name

@function_tool
async def buy_game_tool(ctx: RunContext, game_name: str) -> str:
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