import os
import asyncio
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel, PrivateAttr
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from functools import lru_cache

load_dotenv()

# MongoDB connection setup (adjust URI as needed)
uri = os.getenv("MONGO_CLUSTER_URI")
client = MongoClient(uri)
if not uri:
    raise ValueError("MONGO_URI is missing! Set it in the .env file.")

# Database and collection selection
db = client[os.getenv("MONGO_DB_NAME")]  # Replace with your database name
comments_collection = db["comments"]
movies_collection = db["movies"]
users_collection = db["users"]
sessions_collection = db["sessions"]
theaters_collection = db["theaters"]

# MongoDB Retriever class using Pydantic's BaseModel
class MongoDBRetriever(BaseModel):
    _collection_name: str = PrivateAttr()

    def __init__(self, collection_name: str):
        super().__init__()
        self._collection_name = collection_name

    def _get_relevant_documents(self, query: str):
        collection = db[self._collection_name]
        try:
            # Optimized MongoDB aggregation query with text score sorting
            documents = collection.aggregate([
                {"$match": {"$text": {"$search": query}}},
                {"$project": {"score": {"$meta": "textScore"}, "fullplot": 1}},
                {"$sort": {"score": -1}},
                {"$limit": 5}
            ])
            results = [doc for doc in documents]
            return results if results else [{"answer": "Sorry, I couldn't find relevant information."}]
        except Exception as e:
            return [{"error": f"Error while fetching data from MongoDB: {str(e)}"}]

# Define MongoDB retrievers for each collection
comments_retriever = MongoDBRetriever(collection_name="comments")
movies_retriever = MongoDBRetriever(collection_name="movies")
users_retriever = MongoDBRetriever(collection_name="users")
sessions_retriever = MongoDBRetriever(collection_name="sessions")
theaters_retriever = MongoDBRetriever(collection_name="theaters")

# Create the language model using HuggingFace API (EleutherAI GPT-Neo)
llm = HuggingFaceEndpoint(repo_id="EleutherAI/gpt-neo-2.7B", max_new_tokens=150)

#llm = HuggingFaceEndpoint(repo_id="EleutherAI/gpt-j-6B", max_new_tokens=150)
# Define a prompt template to inject retrieved documents into the LLM
prompt_template = """
Use the following documents to answer the user's query. 
If the information is not found, provide a reasonable answer based on what is available, relevent to the documents.
Documents:
{docs}

The user's question is: {query}

Answer:
"""

# Create the LLM Chain to handle responses with the RAG mechanism
llm_chain = LLMChain(prompt=PromptTemplate(input_variables=["query", "docs"], template=prompt_template), llm=llm)

# Define the tools (retrievers) available for the agent
tools = [
    Tool(name="comments_retriever", func=comments_retriever._get_relevant_documents, description="Retrieve relevant comments information from MongoDB"),
    Tool(name="movies_retriever", func=movies_retriever._get_relevant_documents, description="Retrieve relevant movie information from MongoDB"),
    Tool(name="users_retriever", func=users_retriever._get_relevant_documents, description="Retrieve relevant user information from MongoDB"),
    Tool(name="sessions_retriever", func=sessions_retriever._get_relevant_documents, description="Retrieve relevant session information from MongoDB"),
    Tool(name="theaters_retriever", func=theaters_retriever._get_relevant_documents, description="Retrieve relevant theater information from MongoDB")
]

# Initialize the LangChain agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # This is an agent type that uses tools like retrievers
    verbose=True
)

# Preprocessing to limit document size and avoid large payloads
def preprocess_documents(documents):
    processed_docs = []
    for doc in documents:
        try:
            # Truncate document to the first 500 characters of 'fullplot' or other relevant field
            truncated_doc = doc.get('fullplot', '')[:500]  
            processed_docs.append(truncated_doc)
        except Exception as e:
            processed_docs.append(f"Error processing document: {str(e)}")
    return processed_docs

# Caching for repeated queries
@lru_cache(maxsize=128)
def get_cached_documents(query):
    retrieved_docs = ""
    for tool in tools:
        docs = tool.func(query)  # Get documents for each tool
        docs = preprocess_documents(docs)  # Preprocess and limit size
        retrieved_docs += "\n".join([str(doc) for doc in docs])  # Concatenate docs
    return retrieved_docs

# Async function to handle chatbot queries
async def fetch_documents_async(tool, query):
    return await asyncio.to_thread(tool.func, query)

# Function to generate response based on query and documents
async def chatbot(query):
    # Retrieve documents in parallel
    tasks = [fetch_documents_async(tool, query) for tool in tools]
    results = await asyncio.gather(*tasks)
    
    # Preprocess retrieved documents
    docs = [preprocess_documents(res) for res in results]
    retrieved_docs = "\n".join([str(doc) for doc in docs])
    
    try:
        # Generate response based on the processed documents
        response = llm_chain.run({"query": query, "docs": retrieved_docs})
        return response
    except Exception as e:
        return f"Error while generating response: {str(e)}"

# Function to interact with the chatbot
def run_chatbot():
    print("Welcome to the chatbot! Type 'exit' to quit.")
    while True:
        query = input("Please enter your query: ")  # Get user input
        if query.lower() == 'exit':
            print("Exiting chatbot. Goodbye!")
            break
        
        response = asyncio.run(chatbot(query))
        print("Response:", response)

# Test the chatbot with user input
if __name__ == "__main__":
    run_chatbot()
