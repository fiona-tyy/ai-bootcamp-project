# Syariah Court Divorce Proceedings — Streamlit App

## Pages
1. **Home** — AI assistant (OpenAI) for general questions about the divorce process
2. **About** — site description (placeholder text)
3. **Resources** — placeholder for links and support services

## Setup
```bash
pip install -r requirements.txt
touch .env   # then add your API key OPENAI_API_KEY="" and OPENAI_MODEL="gpt-4o-mini"
streamlit run main.py
```

## Customising
- Assistant behaviour: edit `SYSTEM_PROMPT` in `pages/01_home.py`
- Model: set `OPENAI_MODEL` in `.env`
- Suggested questions: edit `SUGGESTIONS` in `pages/01_home.py`

## Structure
```
main.py          # entry point + navigation
pages/
  01_home.py
  02_about.py
  03_resources.py
helper_functions/
  llm.py

.env
requirements.txt
```
