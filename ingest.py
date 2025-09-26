import os
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

print("Starting the ingestion process...")

# --- Configuration ---
# The folder containing your academic papers
PDF_FOLDER = "corpus" 
# The pre-trained model to generate embeddings. "all-MiniLM-L6-v2" is a great starting point.
MODEL_NAME = "all-MiniLM-L6-v2"
# The files where we'll save our processed data
FAISS_INDEX_PATH = "faiss_index.bin"
CHUNK_DATA_PATH = "chunk_data.pkl"

# --- 1. Load Model ---
print(f"Loading sentence transformer model: {MODEL_NAME}...")
# This will download the model from the internet on the first run.
model = SentenceTransformer(MODEL_NAME)
print("Model loaded successfully.")

# --- 2. Extract Text and Chunk Documents ---
documents = []
for filename in os.listdir(PDF_FOLDER):
    if filename.endswith('.pdf'):
        path = os.path.join(PDF_FOLDER, filename)
        print(f"Processing PDF: {filename}...")
        try:
            doc = fitz.open(path)
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            
            # Simple chunking strategy: split by paragraph
            # A more advanced strategy could split by sentence or use a fixed size with overlap.
            chunks = [chunk.strip() for chunk in text_content.split('\n\n') if chunk.strip()]
            
            for chunk in chunks:
                # We store the chunk text and the source filename
                documents.append({'text': chunk, 'source': filename})
            
            print(f"  - Extracted and chunked {len(chunks)} paragraphs.")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if not documents:
    print("No documents were processed. Make sure you have PDF files in the 'corpus' folder.")
else:
    print(f"\nTotal text chunks created: {len(documents)}")

    # --- 3. Generate Embeddings ---
    print("Generating embeddings for all text chunks...")
    # Extract just the text from our documents list
    all_chunks_text = [doc['text'] for doc in documents]
    # The model.encode() method converts the text to vectors (embeddings)
    embeddings = model.encode(all_chunks_text, show_progress_bar=True)
    print(f"Embeddings generated with shape: {embeddings.shape}") # (num_chunks, embedding_dimension)

    # --- 4. Create and Store FAISS Index ---
    embedding_dimension = embeddings.shape[1]
    # We use IndexFlatL2, a basic but effective index for L2 (Euclidean) distance.
    index = faiss.IndexFlatL2(embedding_dimension)
    
    print("Adding embeddings to FAISS index...")
    index.add(np.array(embeddings).astype('float32'))
    
    print(f"Saving FAISS index to {FAISS_INDEX_PATH}...")
    faiss.write_index(index, FAISS_INDEX_PATH)
    
    # We also need to save the 'documents' list so we can retrieve the original text later
    print(f"Saving chunk data to {CHUNK_DATA_PATH}...")
    with open(CHUNK_DATA_PATH, 'wb') as f:
        pickle.dump(documents, f)
        
    print("\n--- Ingestion Complete! ---")
    print("You can now run app.py to start the search API.")
