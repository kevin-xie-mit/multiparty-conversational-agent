import os
from helper.prompt import sys_prompt
from helper.moderator import Moderator
from helper.chats import Chat
from helper.vector_store import VectorStore

all_chats = Chat(messages_path='/Users/kevinxie/Desktop/MIT/multiparty-conversational-agent/New_IDS_Chat (Old studies)')
moderator = Moderator(sys_prompt)
# vector_store = VectorStore()

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
    long_term_context = ""
    
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
            # vector_store.embed_messages(
            #     message, 
            #     metadata={
            #         "speaker": character, 
            #         "line_number": line_num,
            #         "chat_group": chat_number
            #     }
            # )
            
            # Add conversation context every few messages
            # if len(participant_messages) >= 3:
            #     vector_store.embed_conversation_context(
            #         participant_messages[-5:],  # Last 5 messages as context
            #         context_type="recent_conversation"
            #     )

            with open(os.path.join(output_path, f"group_{chat_number}.txt"), "a") as f:
                f.write(f"{character}: {message}\n")

        # If it is the moderator, we need to inject the intervention
        else:
            # Build context from all messages since the last moderator message
            # if last_moderator_index == -1:
            #     # No previous moderator message, use all participant messages
            #     recent_context = "\n".join(participant_messages) if participant_messages else ""
            # else:
            #     # Get all messages after the last moderator message
            #     messages_since_last_moderator = participant_messages[last_moderator_index + 1:]
            #     recent_context = "\n".join(messages_since_last_moderator) if messages_since_last_moderator else ""

            recent_context = "\n".join(participant_messages[-10:]) if participant_messages else ""

            # Add current moderator message to tracking
            last_moderator_index = len(participant_messages) - 1  # Update the index

            # Update the long-term context
            long_term_context = moderator.update_long_term_context(recent_context, long_term_context)
            
            # Combine recent messages with retrieved context
            full_context = f"""
            RECENT CONVERSATION:
            {recent_context}
            
            IMPORTANT INFORMATION FROM CONVERSATION HISTORY:
            {long_term_context}
            """

            # print("LT context:", long_term_context)

            moderation_result = moderator.get_moderation(full_context)
            
            with open(os.path.join(output_path, f"group_{chat_number}.txt"), "a") as f:
                if moderation_result:
                    f.write(f"MODERATOR: {moderation_result}\n")
                else:
                    f.write(f"MODERATOR: (No intervention needed)\n")


def main():
    pass

for i in range(11, 21):
    process_chat(i)