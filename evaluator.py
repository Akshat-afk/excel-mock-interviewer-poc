# evaluator.py
import os, json
import google.generativeai as genai
from prompts import SYSTEM_PROMPT, PROMPT_TEMPLATE
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import re, json

def call_llm(question: str, answer: str, evidence: dict):
    prompt = PROMPT_TEMPLATE.format(
        question=question,
        answer=answer,
        evidence=json.dumps(evidence)
    )
    import google.generativeai as genai
    response = genai.GenerativeModel("models/gemini-1.5-flash-8b").generate_content(prompt)
    text = response.text.strip()

    m = re.search(r'```json\s*(\{.*?\})\s*```', text, flags=re.S)
    if not m:
        m = re.search(r'(\{.*\})', text, flags=re.S)

    if m:
        try:
            return json.loads(m.group(1))
        except Exception as e:
            return {"score": 0, "short_reason": "parse-error", "suggestions": [str(e), text[:200]]}
    else:
        return {"score": 0, "short_reason": "no-json-found", "suggestions": [text[:200]]}