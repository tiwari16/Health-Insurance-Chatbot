import json
import pandas as pd
import re
import toml
import os
from chatbot.chatbot_logic import setup_chatbot
from chatbot.utils import format_response
from rouge_score import rouge_scorer
from langchain_openai import ChatOpenAI

# ---- Securely Load API Key from Streamlit secrets ----

secrets = toml.load(".streamlit/secrets.toml")
os.environ["OPENAI_API_KEY"] = secrets.get("OPENAI_API_KEY")

# ---- Configuration ----

EVAL_FILE = "tests/evaluation_data/policy_eval.jsonl"
REPORT_FILE = "tests/evaluation_data/policy_eval_results.csv"

# ---- Setup ----

qa_chain = setup_chatbot()
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
judge_llm = ChatOpenAI()  # Will auto-pick key from environment

# ---- Evaluation Loop ----

results = []
total = 0
passed_exact = 0

print("\n--- Starting Comprehensive Policy Chatbot Evaluation ---")

with open(EVAL_FILE, "r") as f:
    for line in f:
        case = json.loads(line)
        question = case["Query"]
        expected_answer = case["truth"].lower()

        response = qa_chain.invoke({
            "question": question,
            "chat_history": []
        })
        
        answer_text = response.get("answer", "")
        formatted_answer = format_response(answer_text).lower()

        rouge_score_val = scorer.score(expected_answer, formatted_answer)["rougeL"].fmeasure
        exact_match = expected_answer in formatted_answer
        if exact_match:
            passed_exact += 1

        sources = [doc.metadata.get("source") for doc in response.get("source_documents", [])]

        # LLM-as-a-Judge
        eval_prompt = f"""
You are an expert health insurance reviewer.

The expected correct answer is:
\"\"\"{expected_answer}\"\"\"

The chatbot's response was:
\"\"\"{formatted_answer}\"\"\"

Rate the response on:
- Relevance to the question
- Completeness based on expected answer
- Grounding (only using provided policy info)

Respond only with a score from 1 (poor) to 5 (excellent) and a short justification.
"""

        judge_response = judge_llm.invoke(eval_prompt)
        judge_score = None
        judge_reason = ""

        if isinstance(judge_response, dict):
            judge_text = judge_response.get("text", "")
        else:
            judge_text = str(judge_response)

        match = re.search(r"([1-5])", judge_text)
        if match:
            judge_score = int(match.group(1))
            judge_reason = judge_text.strip()

        results.append({
            "question": question,
            "expected": expected_answer,
            "actual": formatted_answer,
            "rougeL_f1": round(rouge_score_val, 3),
            "sources": ", ".join(sources),
            "exact_match": exact_match,
            "llm_judge_score": judge_score,
            "llm_reason": judge_reason
        })

        status = "✅ PASSED" if exact_match else "❌ PARTIAL"
        print(f"\n{status}: {question}\nROUGE-L: {rouge_score_val:.2%}\nLLM Judge: {judge_score}\nSources: {sources}\n")

        total += 1

# ---- Final Summary ----

print(f"\n--- Evaluation Complete ---")
print(f"Total: {total}, Exact Matches: {passed_exact}, Partial/Needs Review: {total - passed_exact}")
print(f"Exact Match Accuracy: {passed_exact/total:.2%}")

df = pd.DataFrame(results)
df.to_csv(REPORT_FILE, index=False)
print(f"\nDetailed results saved to: {REPORT_FILE}")
