# Main agent logic for answering questions using FAISS index
import faiss
import json
import numpy as np
import os
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from pathlib import Path
from collections import defaultdict

from dotenv import load_dotenv
# Load environment variables from .env file if it exists
load_dotenv()
# Check for OpenAI API key
if not os.environ.get('OPENAI_API_KEY'):
    print('[ERROR] Please set your OPENAI_API_KEY environment variable.')
    sys.exit(1)

# Load FAISS index and metadata
indexes_dir = Path(__file__).parent.parent / 'indexes'
index = faiss.read_index(str(indexes_dir / 'faiss.index'))
with open(indexes_dir / 'faiss_metadata.json', 'r', encoding='utf-8') as f:
    metadatas = json.load(f)
with open(indexes_dir / 'pdf_chunks.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0, model_name='gpt-4.1-mini')

def build_per_document_indices():
    """
    Build a separate FAISS index and metadata for each document in the Sample folder.
    Returns a dict: {doc_name: (faiss_index, [chunks], [metadatas])}
    """
    doc_chunks = defaultdict(list)
    doc_metas = defaultdict(list)
    for chunk, meta in zip(chunks, metadatas):
        doc_name = meta['doc_name']
        doc_chunks[doc_name].append(chunk['text'])
        doc_metas[doc_name].append(meta)
    doc_indices = {}
    for doc_name, texts in doc_chunks.items():
        if not texts:
            continue
        vectors = np.array(embeddings.embed_documents(texts)).astype('float32')
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)
        doc_indices[doc_name] = (index, texts, doc_metas[doc_name])
    return doc_indices

doc_indices = build_per_document_indices()

# Helper: Retrieve relevant chunks from a single document

def retrieve_from_doc(doc_name, query, top_k=8):
    index, texts, metas = doc_indices[doc_name]
    query_vec = np.array(embeddings.embed_query(query)).astype('float32').reshape(1, -1)
    D, I = index.search(query_vec, top_k)
    results = []
    for idx in I[0]:
        if idx < len(texts):
            results.append({
                'text': texts[idx],
                'doc_name': doc_name,
                'chunk_id': metas[idx]['chunk_id']
            })
    return results

def answer_question(query):
    """
    1. Break down the question into sub-questions (CoT prompt)
    2. For each document, retrieve relevant context for each sub-question
    3. Synthesize a comprehensive answer with sources, grouped by document
    """
    # Step 1: Ask LLM to break down the question
    breakdown_prompt = f"""
Break down the following legal question into logical sub-questions or reasoning steps. List each step as a separate line.

Question: {query}

Sub-questions/steps:
"""
    breakdown_response = llm.invoke(breakdown_prompt)
    if hasattr(breakdown_response, 'content'):
        breakdown_text = breakdown_response.content
    else:
        breakdown_text = str(breakdown_response)
    sub_questions = [s for s in breakdown_text.strip().split('\n') if s.strip()]
    # Step 2: For each document, retrieve relevant context for each sub-question
    doc_contexts = defaultdict(list)
    for doc_name in doc_indices:
        for subq in sub_questions:
            doc_contexts[doc_name].extend(retrieve_from_doc(doc_name, subq, top_k=3))
    # Step 3: Synthesize answer, grouped by document
    context_blocks = []
    for doc_name, doc_chunks in doc_contexts.items():
        if not doc_chunks:
            continue
        block = f"Document: {doc_name}\n" + "\n\n".join([
            f"[Chunk {c['chunk_id']}] {c['text']}" for c in doc_chunks
        ])
        context_blocks.append(block)
    context = "\n\n---\n\n".join(context_blocks)
    prompt = f"""
You are a highly capable legal document analysis agent. Use the following context from multiple legal documents to answer the user's question. Always cite the document name and page number for each fact. If the answer is not found, say so.

Context:
{context}

User Question:
{query}

---

Your step-by-step reasoning and answer (with sources):
"""
    answer_response = llm.invoke(prompt)
    if hasattr(answer_response, 'content'):
        answer_text = answer_response.content
    else:
        answer_text = str(answer_response)
    return answer_text

if __name__ == '__main__':
    user_query = input("Ask your legal question: ")
    answer = answer_question(user_query)
    print("\n---\nAnswer:\n", answer)
