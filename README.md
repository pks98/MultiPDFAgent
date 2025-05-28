# MultiPDFAgent: Legal Document QA Bot

## Folders
- `Sample/` : Place your legal PDF documents here.
- `src/` : Source code for extraction, indexing, agent, and evaluation.

## Files
- `extract_pdfs.py` : Extracts and chunks text from PDFs.
- `build_index.py` : Builds a vector index from extracted chunks.
- `agent.py` : Main agent logic for answering questions.
- `evaluator.py` : Evaluates agent responses for completeness and accuracy.
- `requirements.txt` : Python dependencies.

## Setup
1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
2. Place your PDFs in the `Sample/` folder.
3. Run the scripts in order:
   - Extract and chunk PDFs
   - Build the index
   - Start the agent/chatbot

