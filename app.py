import streamlit as st
from interview_logic import InterviewAgent
from pathlib import Path
import os
import json
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR', './uploads'))
SESSION_DIR = Path(os.getenv('SESSION_DIR', './sessions'))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SESSION_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title='Excel Mock Interviewer - PoC', layout='centered')

if 'agent' not in st.session_state:
    st.session_state.agent = InterviewAgent()

agent = st.session_state.agent

st.title('AI-Powered Excel Mock Interviewer — PoC')
st.write('Quick demo: answer questions or upload an Excel workbook when asked.')

for entry in agent.history:
    role = entry['role']
    text = entry['text']
    if role == 'agent':
        st.markdown(f"**Interviewer:** {text}")
    else:
        st.markdown(f"**You:** {text}")

def save_session():
    path = SESSION_DIR / f"{agent.session_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(agent.summary(), f, indent=2)

if agent.active:
    q = agent.current_question
    st.markdown(f"### Question: {q['text']}")
    txt = st.text_area('Your answer (text or formula)', key='answer_text')
    file = st.file_uploader('Upload workbook (.xlsx) if requested', type=['xlsx'])

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Submit Answer'):
            if not txt.strip():
                st.warning('Type an answer or upload a file before submitting.')
            else:
                agent.record_answer(txt)
                save_session()  
                st.rerun()
    with col2:
        if st.button('Submit Workbook'):
            if not file:
                st.warning('Choose an .xlsx file to upload')
            else:
                dst = UPLOAD_DIR / f"{agent.session_id}--{file.name}"
                with open(dst, 'wb') as f:
                    f.write(file.getbuffer())
                agent.record_upload(str(dst))
                save_session() 
                st.rerun()
else:
    st.success('Interview complete — see summary below')
    st.markdown('## Summary')
    st.write(agent.summary())
    if st.button('Download transcript (JSON)'):
        st.download_button(
            'Download JSON',
            data=agent.transcript_json(),
            file_name=f'{agent.session_id}-transcript.json'
        )

with st.expander('Admin: internal state'):
    st.write({
        'session_id': agent.session_id,
        'current_q_idx': agent.idx,
        'history_len': len(agent.history)
    })