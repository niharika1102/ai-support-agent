from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import calculator, faq_lookup

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


faq_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="faq_lookup",
            description=(
                "Looks up information about customer support topics "
                "such as refunds, delivery, and support hours."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "topic": types.Schema(
                        type="STRING",
                        description="The customer support topic to look up.",
                    )
                },
                required=["topic"],
            ),
        )
    ]
)

tools = {
    "calculator": calculator,
    "faq_lookup": faq_lookup,
}

def run_agent(user_message: str):

    contents = [user_message]

    max_iterations = 5

    for _ in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[
                    calculator_tool,
                    faq_tool,
                ]
            ),
        )

        model_content = response.candidates[0].content

        contents.append(model_content)

        function_call = None

        for part in model_content.parts:
            if part.function_call:
                function_call = part.function_call
                break

        # No tool requested → final answer
        if function_call is None:
            return response.text

        tool = tools.get(function_call.name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {function_call.name}"
            )

        result = tool(**function_call.args)

        # Send tool result back to Gemini
        tool_result = types.Part.from_function_response(
            name=function_call.name,
            response={"result": result},
        )

        contents.append(tool_result)
    
    raise RuntimeError("Agent has reached its maximum number of iterations.")


answer = run_agent("What is the refund policy?")

print(answer)
