from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import calculator

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

function_call = response.candidates[0].content.parts[0].function_call

print("Tool requested:", function_call.name)
print("Arguments:", function_call.args)

result = calculator(function_call.args["expression"])

print("Tool result:", result)

tool_result = types.Part.from_function_response (
    name = function_call.name,
    response = {
        "result": result
    }
)

final_response = client.models.generate_content (
    model = "gemini-3.6-flash",
    contents = [
        "What is 25% of 840?",
        response.candidates[0].content,
        tool_result,
    ],
    config = types.GenerateContentConfig (
        tools = [calculator_tool]
    )
)

print(final_response.text)