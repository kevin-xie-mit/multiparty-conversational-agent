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
                            "- If there are disagreements or misunderstandings between participants, acknowledge different viewpoints and integrate and summarize all key points discussed.\n"
                            "Encourage participants to focus on the correct solution rather than on the consensus. \n"
                            "Never push participants—implicitly or explicitly—toward specific interpretations or solutions and never decide for them.\n"
                        ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "INTERVENE": {
                                "type": "boolean",
                                "description": (
                                    "Set to true if an intervention is needed according to the description above."
                                    "False if no intervention is necessary."
                                )
                            },
                            "TEXT": {
                                "type": "string",
                                "description": (
                                    "The exact message or response to inject into the conversation."
                                    "Should be helpful, corrective, or directive based on context."
                                    "Return the message in English only."
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
                {"role": "user", "content": f"{context}"}
            ],
            tools=self.tools,
            tool_choice="required"  # Force the model to use the function
        )

        # Check for tool_calls (newer format) instead of function_call
        if response.choices[0].message.tool_calls:
            # Get the function arguments from the first tool call
            function_args = response.choices[0].message.tool_calls[0].function.arguments
            
            # Parse the JSON arguments
            output = json.loads(function_args)

            if output["INTERVENE"]:
                return output["TEXT"]
            else:
                print("No intervention needed:")
                return None

        else:
            print("ERROR: No tool calls found in the response")
            print("Full response:", response.choices[0].message)
            return None

    def update_long_term_context(self, conversation_history: str, previous_lt_context: str):
        """
        Given a short section of the chat, this function extracts the most relevant
        information and adds it to the long-term context.

        Relevant information is considered any claims that the users make, disagreements,
        and any other information that is relevant to the murder mystery.

        Args:
            - conversation_history: str of the most recent messages
            - previous_lt_context: str of the previous long-term context

        Returns:
            - new_lt_context: str of the new long-term context

        The new long-term context updates the previous long-term context by adding the most relevant information.
        It also removes any information that is no longer relevant.
        """

        prompt = f"""
            You are the moderator of a murder mystery game. Your role is to observe the conversation and maintain an up-to-date summary of key developments (the long-term context) to help guide participants toward solving the mystery—without being intrusive.

            Your task:
            Given the most recent conversation history (`conversation_history`) and the previous long-term context (`previous_lt_context`), generate an updated long-term context that reflects the current state of the mystery.

            Guidelines:
            - Concisely summarize the **most relevant facts**, suspicions, and character dynamics from the conversation so far.
            - Indicate if one speaker dominates the conversation or not.
            - Indicate if the discussion goes off-topic or not.
            - Indicate if the discussion is advancing the mystery or not. 
            - Include **new information** that affects the mystery (e.g., new accusations, revealed alibis, character behaviors).
            - **Remove outdated or irrelevant** information from the previous context.

            Inputs:
            - conversation_history: {conversation_history}
            - previous_lt_context: {previous_lt_context}

            Output format: string
            - new_lt_context: A concise string capturing the current state of the mystery and the participants' progress towards solving the mystery.

        """

        updated_lt_context = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"conversation_history: {conversation_history}\nprevious_lt_context: {previous_lt_context}"}
            ]
        )

        return updated_lt_context.choices[0].message.content
        
    