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


def run_agent(user_message: str):
    contents = [user_message]

    while True:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=types.GenerateContentConfig(tools=[calculator_tool]),
        )

        model_content = response.candidates[0].content
        contents.append(model_content)

        function_call = None

        for part in model_content.parts:
            if part.function_call:
                function_call = part.function_call
                break

        if function_call is None:
            return response.text

        result = calculator(function_call.args["expression"])

        tool_result = types.Part.from_function_response(
            name=function_call.name, response={"result": result}
        )

        contents.append(tool_result)


# function_call = response.candidates[0].content.parts[0].function_call

# print("Tool requested:", function_call.name)
# print("Arguments:", function_call.args)

# result = calculator(function_call.args["expression"])

# print("Tool result:", result)

# tool_result = types.Part.from_function_response (
#     name = function_call.name,
#     response = {
#         "result": result
#     }
# )

# final_response = client.models.generate_content (
#     model = "gemini-3.6-flash",
#     contents = [
#         "What is 25% of 840?",
#         response.candidates[0].content,
#         tool_result,
#     ],
#     config = types.GenerateContentConfig (
#         tools = [calculator_tool]
#     )
# )

# print(final_response.text)

answer = run_agent("what is 25% of 840?")
print(answer)
