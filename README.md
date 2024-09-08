# Test RAG app

A training project for learning Flask, high-level LLM libraries (such as Langchain and Ollama), and basic web development (HTML, Bootstrap, and JavaScript).

Install dependencies via pip:

```bash
pip install -r requirements.txt
```
Run the server using Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5002 app:app
```
