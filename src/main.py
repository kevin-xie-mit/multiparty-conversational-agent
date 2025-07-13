import os
from helper.prompt import sys_prompt
from helper.moderator import Moderator
from helper.chats import Chat
from helper.vector_store import VectorStore

all_chats = Chat(messages_path='/Users/kevinxie/Desktop/MIT/multiparty-conversational-agent/New_IDS_Chat (Old studies)')
moderator = Moderator(sys_prompt)
vector_store = VectorStore()

output_path = "/Users/kevinxie/Desktop/MIT/multiparty-conversational-agent/moderation_logs"

def process_chat(chat_number: int):
    """
    Process a singular chat and inject whether intervention in needed.

    Return a new text file with the intervention messages injected / replacing the original messages
    """
    # Clear the output file before processing
    output_file = os.path.join(output_path, f"group_{chat_number}.txt")
    if os.path.exists(output_file):
        os.remove(output_file)
    chat = all_chats.get_group(chat_number)
    lines = chat.split("\n")  # Split into lines

    messages_so_far = []
    participant_messages = []  # Track only participant messages for context
    
    for line_num, line in enumerate(lines):
        if ' - ' not in line or ':' not in line.split(' - ')[1]:
            continue  # Skip malformed lines
            
        character = line.split(' - ')[1].split(':')[0].strip()  # Extract character name
        message = line.split(' - ')[1].split(':')[1].strip()

        if character != "M":
            # Process participant message
            formatted_message = f"{character}: {message}"
            messages_so_far.append(formatted_message)
            participant_messages.append(formatted_message)
            
            # Add individual message to vector store with metadata
            vector_store.embed_messages(
                message, 
                metadata={
                    "speaker": character, 
                    "line_number": line_num,
                    "chat_group": chat_number
                }
            )
            
            # Add conversation context every few messages
            if len(participant_messages) >= 3:
                vector_store.embed_conversation_context(
                    participant_messages[-5:],  # Last 5 messages as context
                    context_type="recent_conversation"
                )

            with open(os.path.join(output_path, f"group_{chat_number}.txt"), "a") as f:
                f.write(f"{character}: {message}\n")

        # If it is the moderator, we need to inject the intervention
        else:
            # Build context query based on recent conversation
            recent_context = "\n".join(participant_messages[-10:]) if participant_messages else ""
            
            # Create a more specific query for retrieval
            k = 5

            query = f"""
            Have LLM find the top-{k} instances of the criteria and return them directly.
            "You should only intervene in the following cases:\n"
                "- If one speaker dominates the conversation, encourage quieter members to contribute. "
                "- Participants have a higher chance of correctly identifying the culprit if they successfully share all their unique information.\n"
                "- If the discussion goes off-topic, remind participants to stay focused on the main goal of the conversation.\n"
                "- If participants are disrespectful or using inappropriate language, ensure a civil and constructive discussion.\n"
                "- If there are disagreements or misunderstandings between participants, acknowledge different viewpoints and integrate and summarize all key points discussed."
            ),

            """
            retrieved_context = vector_store.retrieve_context(query, k=5)
            
            # Combine recent messages with retrieved context
            full_context = f"""
            RECENT CONVERSATION:
            {recent_context}
            
            SIMILAR PATTERNS FROM CONVERSATION HISTORY:
            {retrieved_context}
            """
            
            print("RETRIEVED CONTEXT:", retrieved_context)
            print("FULL CONTEXT SENT TO MODERATOR:", full_context)

            moderation_result = moderator.get_moderation(full_context)
            
            with open(os.path.join(output_path, f"group_{chat_number}.txt"), "a") as f:
                if moderation_result:
                    f.write(f"NEW MODERATOR: {moderation_result}\n")
                else:
                    f.write(f"MODERATOR: (No intervention needed)\n")


def main():
    pass

process_chat(11)