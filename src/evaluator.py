"""
Evaluation agent for reviewing the main agent's answers.
Checks for completeness, accuracy, and correct source citation.
"""
import os
import sys
from langchain.chat_models import ChatOpenAI

def evaluate_answer(question, answer, context):
    """
    Uses an LLM to evaluate the answer for:
    - Completeness (did it use all relevant context?)
    - Accuracy (is the answer correct?)
    - Source citation (are sources cited and correct?)
    """
    llm = ChatOpenAI(temperature=0,model_name='gpt-4.1-mini')
    prompt = f"""
You are an expert legal QA evaluator. Given the user's question, the answer provided by an agent, and the context (relevant document excerpts), evaluate the answer for:
- Completeness: Did the answer use all relevant context?
- Accuracy: Is the answer correct and faithful to the context?
- Source citation: Are the cited document names and page numbers correct and sufficient?

Provide a short evaluation summary and a score from 1 (poor) to 5 (excellent).

Question: {question}

Context:
{context}

Agent's Answer:
{answer}

Evaluation (summary and score):
"""
    return llm.predict(prompt)

if __name__ == "__main__":
    print("Paste the user question:")
    question = input()
    print("Paste the agent's answer:")
    answer = input()
    print("Paste the context (relevant document excerpts):")
    context = input()
    evaluation = evaluate_answer(question, answer, context)
    print("\n---\nEvaluation:\n", evaluation)
