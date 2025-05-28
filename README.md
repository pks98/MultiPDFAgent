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

## Features
- Streamlit web UI with sidebar for sub-questions (reasoning steps)
- Sidebar displays all sub-questions generated for each query

## Usage
1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
2. Place your PDFs in the `Sample/` folder.
3. Run the scripts in order:
   - Extract and chunk PDFs:
     ```cmd
     python src/extract_pdfs.py
     ```
   - Build the index:
     ```cmd
     python src/build_index.py
     ```
   - Start the Streamlit app:
     ```cmd
     streamlit run app.py
     ```

4. Enter your legal question in the main area. The sidebar will show the sub-questions (reasoning steps) generated for your query. The answer will be displayed in a styled block with references to the source documents and sections.

## Notes
- The agent uses per-document retrieval and chain-of-thought breakdown for robust, explainable answers.
- If no relevant information is found, a clear message is shown.
- For best results, ensure your PDFs are clear and well-formatted.

---

