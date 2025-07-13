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
            
            # Try multiple encodings to handle different file formats
            txt = self._read_file_with_fallback_encoding(path)
            if txt is not None:
                all_messages.append(txt)

        return all_messages
    
    def _read_file_with_fallback_encoding(self, file_path):
        """
        Try to read a file with multiple encoding options.
        Returns the file content as string, or None if all encodings fail.
        """
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return None
        
        # If all encodings fail, try reading with error handling
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                print(f"Warning: Had to use error replacement for file {file_path}")
                return file.read()
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")
            return None
    
    def remove_DS_Store(self):
        all_files = os.listdir(self.messages_path)
        if ".DS_Store" in all_files:
            all_files.remove(".DS_Store")
        
        return all_files

    # 1-indexed
    def get_group(self, group_id: int):
        return self.messages[group_id - 1]






        
        
