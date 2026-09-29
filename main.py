from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

calculator_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculator",
            description="Performs mathematical calculations.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "expression": types.Schema(
                        type="STRING",
                        description="The mathematical expression to calculate.",
                    )
                },
                required=["expression"],
            ),
        )
    ]
)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="What is 25% of 840?",
    config=types.GenerateContentConfig(tools=[calculator_tool]),
)

print(response)
