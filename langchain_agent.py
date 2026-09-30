from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

from tools import calculator, faq_lookup


@tool
def calculator_tool(expression: str) -> float:
    """Performs mathematical calculations."""
    return calculator(expression)


@tool
def faq_lookup_tool(topic: str) -> str:
    """Looks up information about customer support topics such as refunds, delivery, and support hours."""
    return faq_lookup(topic)


llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

agent = create_agent(
    model=llm,
    tools=[
        calculator_tool,
        faq_lookup_tool,
    ],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is 15% of 200 and then add 50?"}]}
)

for message in result["messages"]:
    print("\n---")
    print(message)
