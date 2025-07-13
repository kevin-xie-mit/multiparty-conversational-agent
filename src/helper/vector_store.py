import os
import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self, collection_name="conversation_context"):
        self.vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(),
            collection_name=collection_name,  # Fixed collection name
            persist_directory=os.getenv("PERSIST_DIRECTORY", "vector_store")
        )

    def embed_messages(self, message: str, metadata=None):
        """
        Add a single message to the vector store with optional metadata
        """
        if metadata is None:
            metadata = {}
        
        self.vector_store.add_texts([message], metadatas=[metadata])

    def embed_conversation_context(self, messages: list, context_type="recent_messages"):
        """
        Add a list of messages as conversation context with less redundancy
        """
        if len(messages) >= 5:
            # Create non-overlapping segments to reduce redundancy
            segment_size = 5
            for i in range(0, len(messages) - segment_size + 1, segment_size):  # Non-overlapping
                segment = "\n".join(messages[i:i+segment_size])
                metadata = {
                    "context_type": context_type,
                    "segment_start": i,
                    "segment_size": segment_size,
                    "message_count": len(messages[i:i+segment_size])
                }
                self.vector_store.add_texts([segment], metadatas=[metadata])

    def retrieve_context(self, query: str, k=5):
        """ 
        Cosine similarity search that returns formatted text content with deduplication
        """
        docs = self.vector_store.similarity_search(query, k)  # Get more to filter
        
        # Deduplicate and select diverse content
        seen_content = set()
        context_texts = []
        
        for doc in docs:
            content = doc.page_content.strip()
            
            # Skip if we've seen very similar content
            content_words = set(content.lower().split())
            is_duplicate = False
            
            for seen in seen_content:
                seen_words = set(seen.lower().split())
                # If more than 70% overlap, consider it duplicate
                overlap = len(content_words & seen_words) / len(content_words | seen_words)
                if overlap > 0.7:
                    is_duplicate = True
                    break
            
            if not is_duplicate and content:
                context_texts.append(content)
                seen_content.add(content)
                
                # Stop when we have enough diverse content
                if len(context_texts) >= k:
                    break
        
        return "\n\n---\n\n".join(context_texts) if context_texts else "No relevant context found."
    



        pass

