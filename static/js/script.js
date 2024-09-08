const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const uploaderText = document.getElementById("uploader-text");
const uploaderIcon = document.getElementById("uploader-icon");
const answerParagraph = document.getElementById("answer");
const spinner = document.getElementById('loading-spinner');
const submitButton = document.getElementById('submit-btn');

let formData = new FormData();

inputFile.addEventListener("change", uploadFile);

dropArea.addEventListener("dragover", function(e){
  e.preventDefault();
});

dropArea.addEventListener("drop", function(e){
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadFile();
});

document.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.key === 'Enter') {
      document.getElementById('submit-btn').click();
  }
});

function uploadFile() {
  if (inputFile.files.length == 1) { 
    file = inputFile.files[0];
    formData.set('document', file);
    uploaderText.textContent = `File: ${file.name}`;
  }
}

async function submitQuestion() {
  formData.set('question', document.getElementById('question').value);
  try {
    spinner.classList.remove('d-none');
    submitButton.disabled = true;
    const response = await fetch('/submit-question', {
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      throw new Error(`${response.status}`);
    }
    const result = await response.json();
    answerParagraph.textContent = result.answer;
  } catch (error) {
    answerParagraph.textContent = 'Error submitting the question.';
  } finally {
    spinner.classList.add('d-none');
    submitButton.disabled = false;
    answerParagraph.classList.remove('d-none');
  }
}