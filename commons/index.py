import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader, 
    StorageContext, 
    ServiceContext, 
    load_index_from_storage
)
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from private.private_keys import PrivateKeys
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


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
        # Initialize Grok with API key
        keys = PrivateKeys()
        self.base_model = Groq(
            model='llama-3.2-1b-preview',
            api_key=keys['groq'],
            temperature=0.7
        )
        self.embedding_model = HuggingFaceEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2')
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
        self.chat_bot = self.index.as_chat_engine()
        if attach_context is not None:
            self.attached_context = attach_context
        else:
            self.attached_context = """
            Assume that you are a person named Saad who is replying to an interviewer, questions about his qualifications. 
            Use to qualifications to answer the question AND ensure to include the personality traits that are relevant to the job.
            """.strip().replace('\n', '')
    
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
        prepped_mssg = f'USE THE INSTRUCTIONS AHEAD TO RESPOND:{self.attached_context} - Interviewer Asks:{mssg}'
        return self.chat_bot.chat(prepped_mssg)
    
if __name__ == '__main__':
    index = Index('init', 'portfolio_documents')
    resp = index('What certifications has Saad Completed?')
    print(resp)