import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader, 
    StorageContext, 
    load_index_from_storage
)
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from private.private_keys import PrivateKeys
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from helper_modules.model_download import setup_embedding_models



class Index:
    def __init__(self, command:str, base_dir:str, attach_context:str=None):
        """
        returns:
            Index object
        function:
            Indexer Class initialize function to create a RAG index for llama.
        args:
            command: (load | init)
                load from an existing index
                initialize an index form base directory
            base_dir: path to the base directory (load OR init)
        """
        # Initialize context first
        if attach_context is not None:
            self.attached_context = attach_context
        else:
            self.attached_context = """
            STRICTLY FOLLOW THE INSTRUCTIONS BELOW:
            1. Refer to personality.txt to structure my answers the way SAAD would answer them.
            2. Do not disclose sensitive/personal information
            3. Stay within professional boundaries, but be flexible and a little playful with the answers
            4. YOU MAY Sparringly utalise external information TO ENHANCE THE RESPONSE. However,
            DO NOT ADD any EXTRA INFORMATION, ONLY USE THE INFORMATION PROVIDED IN THE DOCUMENTS, IN THE RESPONSE.
            5. STRICTLY behave LIKE SAAD. Refer to the personality.txt document repeatedly for structuring answers.
            6. SHORT ANSWERS WHEN ASKED FOR, EXTENSIVE AND COMPLETE DETAILS WHEN EXPLICITLY INQUIRED.
            Follow the instructions below to respond:
            Assume that you are a person named Saad who is replying to a person curious to know about me. 
            Use the documents to answer the question AND ensure to include the personality traits that are relevant to the question asked.
            Focus on highlighting my skills in a very natural and HUMAN WAY
            """.strip().replace('\n', '')

        # Initialize Grok with API key and system prompt
        keys = PrivateKeys()
        self.base_model = Groq(
            model='llama-3.3-70b-versatile',
            api_key=keys['groq'],
            temperature=0.3,
            system_prompt=self.attached_context
        )
        
        if not os.path.exists('model_cache'):
            setup_embedding_models()
        self.embedding_model = HuggingFaceEmbedding(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            cache_folder='model_cache'
        )
        Settings.llm = self.base_model
        Settings.embed_model = self.embedding_model
        self.base_dir = os.path.abspath(base_dir)
        match command:
            case 'load':
                if not os.path.exists(self.base_dir):
                    raise FileNotFoundError('Specified folder does not exist')
                storage_context = StorageContext.from_defaults(persist_dir=self.base_dir)
                self.index = load_index_from_storage(storage_context)
            case 'init':
                documents = SimpleDirectoryReader(self.base_dir).load_data()
                self.index = VectorStoreIndex.from_documents(documents, show_progress=True, llm=self.base_model)
        self.__save_index()
        self.chat_bot = self.index.as_chat_engine(
            chat_mode="condense_plus_context",
            verbose=True,
            max_iterations=3 
        )
    
    def __save_index(self):
        """
            Saves the index to the storage directory
        """
        self.index.storage_context.persist('./storage')
    
    def __call__(self, mssg:str)->str:
        """
            Returns: str
                Response to the mssg supplied as argument
            Args:
                mssg: str
                    Message to be processed by the chat_bot
            Overrides the call command. Calling the object as a function executes this
        """
        prepped_mssg = f'mssg: {mssg}'
        if 'lets start over' in mssg.lower():
            self.chat_bot.reset()
        return self.chat_bot.chat(prepped_mssg)
    
if __name__ == '__main__':

    index = Index('init', 'portfolio_documents')
    resp = index('What certifications has Saad Completed?')
    print(resp)