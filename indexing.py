import os
import sqlite3
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, ChatPromptTemplate, Document
from llama_index.llms.ollama import Ollama

# Define embedding model
embedding_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5", device='cuda')

# Define LLM with parameters for optimization
llm = Ollama(
    model="llama3.2:1b",          
    request_timeout=60.0,         
    temperature=0.5,              
    top_k=40,                     
    top_p=0.85,                   
    max_tokens=256,
    stream=True             
)

# Directory to store the cached index
INDEX_STORAGE_DIR = "index_storage"

def fetch_data_from_db():
    """Fetches content from SQLite database and returns a list of Document objects."""
    conn = sqlite3.connect("data/scraped_data.db")
    c = conn.cursor()
    c.execute("SELECT content FROM web_pages")
    rows = c.fetchall()
    conn.close()
    
    return [Document(text=row[0]) for row in rows] if rows else []

def build_and_save_index():
    """Builds the index from the database content and saves it for future use."""
    print("Building and saving the index...")
    
    documents = fetch_data_from_db()
    if not documents:
        print("No data found in the database!")
        return
    
    index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)
    storage_context = index.storage_context
    storage_context.persist(persist_dir=INDEX_STORAGE_DIR)
    print("Index saved successfully.")

def load_index_once():
    """Loads the index once and stores it in memory for future queries."""
    if not hasattr(load_index_once, "cached_index"):
        if os.path.exists(INDEX_STORAGE_DIR):
            print("Loading existing index into memory...")
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_DIR)
            load_index_once.cached_index = load_index_from_storage(
                storage_context, embed_model=embedding_model
            )
        else:
            print("Index not found. Building a new one...")
            build_and_save_index()
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_DIR)
            load_index_once.cached_index = load_index_from_storage(
                storage_context, embed_model=embedding_model
            )
    return load_index_once.cached_index

def indexer(question):
    """Uses the cached or newly created index to answer the given question."""
    index = load_index_once()

    # Define the chat prompt template
    chat_prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a highly intelligent assistant specialized in understanding and analyzing complex data. "
            "Your task is to provide clear, concise, and accurate answers strictly based on the given context. "
            "Avoid making assumptions or using information that is not explicitly present in the context."
        ),
        (
            "user",
            """### Context:
{context_str}

### Instruction:
Based on the context provided, answer the following query as accurately and concisely as possible. Avoid including any information not found in the context.

### Query:
{query_str}"""
        )
    ])

    query_engine = index.as_query_engine(
        text_qa_template=chat_prompt_template,
        llm=llm
    )

    response = query_engine.query(question)
    return response.response

if __name__ == "__main__":
    question = input("Enter your question about RVCE: ")
    print(indexer(question))
