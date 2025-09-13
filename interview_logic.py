import uuid
from prompts import QUESTIONS
from evaluator import call_llm
import json

class InterviewAgent:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.idx = 0
        self.history = []  
        self.results = []  
        self.active = True
        self.history.append({
            'role': 'agent',
            'text': 'Hello — I am your Excel mock interviewer. I will ask a few questions.'
        })
        self.history.append({'role': 'agent', 'text': QUESTIONS[0]['text']})

    @property
    def current_question(self):
        return QUESTIONS[self.idx]

    def record_answer(self, text: str):
        q = self.current_question
        self.history.append({'role': 'user', 'text': text})
        evidence = {}
        grade = call_llm(q['text'], text, evidence)
        self.results.append({
            'question_id': q['id'],
            'answer': text,
            'grade': grade,
            'evidence': evidence
        })
        self.idx += 1
        if self.idx < len(QUESTIONS):
            self.history.append({'role': 'agent', 'text': QUESTIONS[self.idx]['text']})
        else:
            self.finish()

    def record_upload(self, filepath: str):
        self.history.append({'role': 'user', 'text': f'Uploaded file: {filepath}'})
        self.results.append({'question_id': 'upload', 'file': filepath})
        self.idx += 1
        if self.idx < len(QUESTIONS):
            self.history.append({'role': 'agent', 'text': QUESTIONS[self.idx]['text']})
        else:
            self.finish()

    def finish(self):
        self.active = False
        self.history.append({'role': 'agent', 'text': 'Thank you. The interview is finished.'})

    def summary(self):
        total = 0
        count = 0
        for r in self.results:
            g = r.get('grade')
            if g and isinstance(g.get('score'), int):
                total += g['score']
                count += 1
        avg = total / count if count else 0
        return {
            'session_id': self.session_id,
            'avg_score': avg,
            'results': self.results
        }

    def transcript_json(self):
        return json.dumps({
            'session_id': self.session_id,
            'history': self.history,
            'results': self.results
        }, indent=2)