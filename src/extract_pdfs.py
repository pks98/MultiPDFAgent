"""
Extracts and chunks text from all PDFs in the Sample/ folder
Saves the chunks and metadata to a JSONL file for indexing
"""
import os
import fitz  # PyMuPDF
import json
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"[WARN] Could not open {pdf_path}: {e}")
        return []
    full_text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            full_text += f"\n[Page {page_num+1}]\n" + text.strip()
    # Use RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = []
    for i, chunk in enumerate(splitter.split_text(full_text)):
        chunks.append({
            'doc_name': os.path.basename(pdf_path),
            'chunk_id': i,
            'text': chunk
        })
    return chunks

def main():
    sample_dir = Path(__file__).parent.parent / 'Sample'
    output_path = Path(__file__).parent.parent / 'pdf_chunks.jsonl'
    all_chunks = []
    for pdf_file in sample_dir.glob('*.pdf'):
        chunks = extract_text_from_pdf(pdf_file)
        if not chunks:
            print(f"[INFO] No text extracted from {pdf_file}")
        all_chunks.extend(chunks)
    if not all_chunks:
        print("[ERROR] No text extracted from any PDFs. Exiting.")
        return
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    print(f"Extracted {len(all_chunks)} chunks from PDFs. Saved to {output_path}")

if __name__ == '__main__':
    main()
