import faiss
import pickle
import requests
import json
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify
from flask_cors import CORS
import config  # <-- Imports your new config file with the API key

# 1. Initialize Flask App and CORS
app = Flask(__name__)
CORS(app)

# 2. Load necessary data and models
print("Loading pre-trained model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded.")

print("Loading FAISS index and chunk data...")
try:
    index = faiss.read_index('faiss_index.bin')
    with open('chunk_data.pkl', 'rb') as f:
        chunk_data = pickle.load(f)
    print("Data loaded successfully.")
except FileNotFoundError:
    print("ERROR: faiss_index.bin or chunk_data.pkl not found.")
    index = None
    chunk_data = None

# --- UPDATED: Function now uses the API Key from config.py ---
def generate_answer(question, context_chunks):
    # This is the endpoint for the Gemini model
    api_key = config.API_KEY  # <-- Use the key from our new file
    
    # Check if the API key has been set
    if api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE" or not api_key:
        print("ERROR: Gemini API Key is not set in config.py")
        return "Error: The Gemini API Key has not been configured in the backend."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    context = "\n".join([f"Source: {chunk['source']}, Content: {chunk['text']}" for chunk in context_chunks])
    system_instruction = "You are the Academic Navigator. Based ONLY on the provided context from academic papers, provide a concise, direct answer to the user's question. Synthesize the information from the different sources. Do not use outside knowledge. If the answer is not in the context, say so."
    prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() 
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print("API Warning: No candidates returned from Gemini.")
            # Check for blockades
            if 'promptFeedback' in result and 'blockReason' in result['promptFeedback']:
                 return f"Content blocked by the API. Reason: {result['promptFeedback']['blockReason']}"
            return "The model could not generate an answer based on the provided context."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "There was an error communicating with the generative AI model."


@app.route('/api/query', methods=['POST'])
def query_api():
    if not index or not chunk_data:
        return jsonify({"error": "Backend data not loaded. Run ingest.py."}), 500

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided."}), 400

    print(f"Received question: {question}")

    # 1. RETRIEVAL: Perform the semantic search
    k = 5
    question_embedding = model.encode([question])
    distances, indices = index.search(question_embedding, k)

    relevant_chunks = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        relevant_chunks.append({
            'source': chunk_data[idx]['source'],
            'text': chunk_data[idx]['text']
        })
    
    print(f"Found {len(relevant_chunks)} relevant chunks.")

    # 2. GENERATION: Use the retrieved chunks to generate an answer
    print("Generating answer with Gemini...")
    answer = generate_answer(question, relevant_chunks)
    print(f"Generated Answer: {answer}")

    # 3. RESPOND: Send both the answer and the sources back to the frontend
    return jsonify({
        "answer": answer,
        "sources": relevant_chunks
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

