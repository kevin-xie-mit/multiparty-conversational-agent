import os
from helper.prompter import Prompter
from helper.chats import Chat

all_chats = Chat(messages_path='/Users/kevinxie/Desktop/MIT/multiparty-conversational-agent/New_IDS_Chat (Old studies)')

group_1 = all_chats.get_group(1)
