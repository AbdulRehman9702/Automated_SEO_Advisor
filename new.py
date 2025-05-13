import pandas as pd
import numpy as np
import re
from chromadb.utils import embedding_functions
import chromadb as db
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login


def create_chromadb_collection(df, chromadb_path, collection_name, model_name="all-MiniLM-L6-v2"):
    # Initialize the embedding model
    embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    
    # Initialize the ChromaDB client
    chroma_client = db.PersistentClient(path=chromadb_path)
    
    # Create the collection with the specified embedding function
    collection = chroma_client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_model,
    )
    
    # Combine all columns into a single string for each row to form the document content
    documents = df.apply(lambda row: ' '.join(row.astype(str)), axis=1).tolist()
    
    # Convert each row to a dictionary to use as metadata
    metadatas = df.to_dict(orient="records")
    
    # Generate unique IDs for each document
    ids = [str(i) for i in range(len(documents))]
    
    # Add documents, their metadata, and IDs to the collection
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    
    return collection

def query_chromadb_collection(collection, query_text, n_results=1):
    results = collection.query(query_texts=[query_text], n_results=n_results)
    return results

def generate_response_with_llm(model_id, access_token, prompt_template):
    login(token=access_token)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    lm_model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    
    pipe = pipeline(
        "text-generation",
        model=lm_model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        device_map="auto",
    )
    
    lm_response = pipe(prompt_template)
    return lm_response[0]["generated_text"]

def main(user_q, file_path="./dataset.csv", chromadb_path="./chromadb", model_id="meta-llama/Llama-3.2-1B-Instruct", access_token="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"):
    # Load the preprocessed data from the Excel file
    df = pd.read_csv(file_path)
    
    # Create or load the ChromaDB collection
    collection = create_chromadb_collection(df, chromadb_path, "SEO_Calligraphy_Collection")
    
    # Query the collection with the user's input
    user_query = user_q
    results = query_chromadb_collection(collection, user_query)
    
    # Prepare the context for the language model
    context = " ".join([f"#{str(i)}" for i in results["documents"]])
    prompt_template = f"""
    Relevant context: {context}
    Considering the relevant context, answer the question.
    Question: {user_query}
    Answer: """
    
    # Generate a response using the language model
    response = generate_response_with_llm(model_id, access_token, prompt_template)
    
    return response

