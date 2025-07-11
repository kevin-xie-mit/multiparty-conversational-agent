import os
from helper.prompt import sys_prompt
from helper.moderator import Moderator
from helper.chats import Chat

all_chats = Chat(messages_path='/Users/kevinxie/Desktop/MIT/multiparty-conversational-agent/New_IDS_Chat (Old studies)')
moderator = Moderator(sys_prompt)

def process_chat(chat: str):
    """
    Process a singular chat and inject whether intervention in needed
    """

    pass

def main():
    pass