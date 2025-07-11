import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


class Moderator:
    def __init__(self, prompt: str):
        self.prompt = prompt

        # Initialize the OpenAI client
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            )

        # CREATE TOOLS
        self.tools = self.create_tools()

    def create_tools(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "intervene",
                    "description": (
                            "Use this tool to determine whether to intervene in a conversation.\n\n"
                            "Your role, as the moderator, is to facilitate communication without being intrusive. "
                            "You should only intervene in the following cases:\n"
                            "- If one speaker dominates the conversation, encourage quieter members to contribute. "
                            "Participants have a higher chance of correctly identifying the culprit if they successfully share all their unique information.\n"
                            "- If the discussion goes off-topic, remind participants to stay focused on the main goal of the conversation.\n"
                            "- If participants are disrespectful or using inappropriate language, ensure a civil and constructive discussion.\n"
                            "- If there are disagreements or misunderstandings between participants, acknowledge different viewpoints and integrate and summarize all key points discussed."
                        ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "INTERVENE": {
                                "type": "boolean",
                                "description": (
                                    "Set to true if an intervention is needed according to the description above. "
                                    "False if no intervention is necessary."
                                )
                            },
                            "TEXT": {
                                "type": "string",
                                "description": (
                                    "The exact message or response to inject into the conversation. "
                                    "Should be helpful, corrective, or directive based on context."
                                )
                            }
                        },
                        "required": ["INTERVENE", "TEXT"]
                    }
                }
            }
        ]

        return tools

    def get_moderation(self, context):
        """
        Given the context of the chat + RAG context, determine whether intervention is needed
        """
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": context}
            ],
            tools=self.tools
        )

        if response.choices[0].message.function_call:
            content = response.choices[0].message.content

            output = json.loads(content)

            print("Debugging Output: ", output)

            if output["INTERVENE"]:
                return output["TEXT"]
            else:
                return None

        else:
            print("ERROR: No function call found in the response")
            return None

    