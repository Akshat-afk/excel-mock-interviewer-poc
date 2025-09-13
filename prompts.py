QUESTIONS = [
    {"id": "q1", "text": "Explain the difference between VLOOKUP and INDEX+MATCH and when you'd prefer INDEX+MATCH."},
    {"id": "q2", "text": "Write an Excel formula to sum column B where column A equals 'Completed'."},
    {"id": "q3", "text": "You have a dataset with Date, Product, Revenue. Describe how you'd build a pivot table to show monthly revenue by product."},
]

SYSTEM_PROMPT = (
    "You are an impartial Excel expert grader. Given a question, candidate answer, and deterministic evidence, "
    "return JSON ONLY with: score (0-4 integer), short_reason (<=20 words), suggestions (list of 1-3 strings)."
)

PROMPT_TEMPLATE = (
    "Question: {question}\n"
    "Candidate answer: {answer}\n"
    "Evidence: {evidence}\n"
    "Return JSON only."
)
