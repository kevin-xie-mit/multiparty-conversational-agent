import os

class Chat:
    def __init__(self, messages_path: str):
        self.messages_path = messages_path

        # self.messages is a list of strings
        self.messages = self.load_messages()

    def load_messages(self):
        all_messages = []

        all_files = self.remove_DS_Store()

        all_files = sorted(all_files, key=lambda x: int(x.split('_')[1].split('.')[0]))

        for txt_file in all_files:
            path = os.path.join(self.messages_path, txt_file)


            with open(path, 'r') as file:
                print(path)
                txt = file.read()

                all_messages.append(txt)

        

        return all_messages
    
    def remove_DS_Store(self):
        if ".DS_Store" in os.listdir(self.messages_path):
            all_files = os.listdir(self.messages_path)
            all_files.remove(".DS_Store")
        
        return all_files

    # 1-indexed
    def get_group(self, group_id: int):
        return self.messages[group_id - 1]






        
        
