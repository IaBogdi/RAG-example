from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from utils import RAG

app = Flask(__name__)

UPLOAD_FOLDER = Path('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
rag = RAG()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-question', methods=['POST'])
def submit_question():
    question = request.form.get('question')
    file = request.files.get('document')
    answer = None
    if file:
        filename = secure_filename(file.filename)
        file_path = app.config['UPLOAD_FOLDER'] / filename
        file.save(file_path)
        answer = rag.GetAnswer(file_path, question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)