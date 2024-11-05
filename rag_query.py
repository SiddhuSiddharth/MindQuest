import argparse
import os
import json
import time
from datetime import datetime, timedelta
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from get_embedding_function import get_embedding_function, TransformerEmbedding
import cohere  # Import Co:here SDK

# Update these paths to cloud storage if necessary
CHROMA_PATH = "chroma"  # Use a relative path for cloud deployment
MEMORY_FILE = "chat_memory.json"
MEMORY_DURATION_DAYS = 3

PROMPT_TEMPLATE = """
You are an AI assistant. Use the following context to answer the question. If the context does not contain the information needed, use your pre-trained knowledge to provide a comprehensive answer.

Context:
{context}

---

Question: {question}

Answer:
"""

CASUAL_CONVERSATIONS = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What can I do for you?",
    "how are you": "I'm an AI, so I don't have feelings, but I'm here to help you!",
    "goodbye": "Goodbye! Have a great day!",
    "bye": "Bye! Take care!",
}

# Co:here API setup
API_KEY = "bfG3xtxmuePvTNe4e4RWNUxuqVj9HigTy3T1jBMx"
cohere_client = cohere.Client(API_KEY)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    response_text = query_rag(query_text)
    print(response_text)


model_name = "distilbert-base-uncased"
embedding_instance = TransformerEmbedding(model_name)


def query_rag(query_text: str):
    # Handle casual conversation
    for trigger, response in CASUAL_CONVERSATIONS.items():
        if trigger in query_text.lower():
            return response

    # Load memory
    memory = load_memory()
    if memory:
        memory_context = "\n\n".join(
            [f"User: {entry['user']}\nBot: {entry['bot']}" for entry in memory]
        )
    else:
        memory_context = ""

    # Prepare the DB
    embedding_function = embedding_instance  # Ensure this returns the correct object
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    combined_context = f"{memory_context}\n\n---\n\n{context_text}".strip()
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=combined_context, question=query_text)

    # Use Co:here to generate the response
    try:
        response = cohere_client.generate(
            model="command-xlarge-nightly",  # Adjust the model name
            prompt=prompt,
            max_tokens=300,
            temperature=0.5,
        )
        response_text = response.generations[0].text.strip()
    except cohere.error.CohereError as e:
        st.error(f"Co:here API error: {e}")
        return "Sorry, there was an error with the AI model."

    response_text = response.generations[0].text.strip()

    # Save memory
    memory.append({"user": query_text, "bot": response_text})
    save_memory(memory)

    return response_text


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            try:
                memory_data = json.load(file)
            except json.JSONDecodeError:
                return []
        timestamp = memory_data.get("timestamp")
        memory = memory_data.get("memory")
        if (
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            + timedelta(days=MEMORY_DURATION_DAYS)
            > datetime.now()
        ):
            return memory
    return []


def save_memory(memory):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MEMORY_FILE, "w") as file:
        json.dump({"timestamp": timestamp, "memory": memory}, file)


if __name__ == "__main__":
    main()