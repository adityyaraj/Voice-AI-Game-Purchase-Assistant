from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

def extract_game_name(user_input:str) -> str:
    prompt = PromptTemplate.from_template(
        'Extract the name of the game from the user input: "{user_input}"')
    chain = prompt | llm
    response = chain.invoke({"user_input": user_input})
    return response.content.strip()