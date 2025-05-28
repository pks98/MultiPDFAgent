# Builds a FAISS vector index from extracted PDF chunks
import json
import os
from pathlib import Path
import faiss
from langchain_community.embeddings import OpenAIEmbeddings
import numpy as np
import sys

# Check for OpenAI API key
if not os.environ.get('OPENAI_API_KEY'):
    print('[ERROR] Please set your OPENAI_API_KEY environment variable.')
    sys.exit(1)

# Load chunks
chunks_path = Path(__file__).parent.parent / 'pdf_chunks.jsonl'
with open(chunks_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Get texts and metadatas
texts = [chunk['text'] for chunk in chunks]
metadatas = [{'doc_name': chunk['doc_name'], 'chunk_id': chunk['chunk_id']} for chunk in chunks]

# Get embeddings
embeddings = OpenAIEmbeddings()
text_vectors = embeddings.embed_documents(texts)
text_vectors = np.array(text_vectors).astype('float32')

# Build FAISS index
index = faiss.IndexFlatL2(text_vectors.shape[1])
index.add(text_vectors)

# Save index and metadata
faiss.write_index(index, str(Path(__file__).parent.parent / 'faiss.index'))
with open(Path(__file__).parent.parent / 'faiss_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(metadatas, f, ensure_ascii=False, indent=2)

print(f"FAISS index built with {len(texts)} chunks.")
