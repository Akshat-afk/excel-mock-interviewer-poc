# Excel Mock Interviewer (Streamlit PoC)

This repository implements a single-process Streamlit Proof-of-Concept for the AI-Powered Excel Mock Interviewer.

## Quickstart (local)

1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

2. Run Streamlit app

```bash
streamlit run app.py
```

3. Open http://localhost:8501

## What each file does (step-by-step)

- `app.py` — Streamlit UI and control; displays questions, captures answers and uploads, shows summary.
- `interview_logic.py` — Manages interview state, history, session id, and orchestrates evaluation calls.
- `evaluator.py` — Deterministic autograder helpers using openpyxl and an LLM wrapper (OpenAI when enabled). Returns parsed grading JSON.
- `prompts.py` — Questions and prompt templates used by the grader.
- `requirements.txt` — Python deps.

## How grading works in the Streamlit PoC

- For text answers: `interview_logic` calls `evaluator.call_llm()` which either calls OpenAI (chat completions) to obtain a JSON grade or uses a simple heuristic fallback.

## Extending to production

- Replace Gemini(free) grader with a high-quality production LLM and stronger prompt engineering.
- Persist sessions to a database and files to object storage.
- Add authentication and consent screens.
- Implement active-learning pipeline where low-confidence grades are routed to human reviewers.
