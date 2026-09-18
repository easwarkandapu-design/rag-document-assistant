const uploadForm = document.getElementById('uploadForm');
const uploadStatus = document.getElementById('uploadStatus');
const chatForm = document.getElementById('chatForm');
const chat = document.getElementById('chat');

function addMessage(text, cls, small='') {
  const div = document.createElement('div');
  div.className = `msg ${cls}`;
  div.textContent = text;
  chat.appendChild(div);
  if (small) {
    const meta = document.createElement('div');
    meta.className = 'small';
    meta.textContent = small;
    chat.appendChild(meta);
  }
  chat.scrollTop = chat.scrollHeight;
}

uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = document.getElementById('file').files[0];
  if (!file) return;
  uploadStatus.textContent = 'Indexing document...';
  const fd = new FormData();
  fd.append('file', file);
  try {
    const res = await fetch('/upload', {method: 'POST', body: fd});
    const data = await res.json();
    uploadStatus.textContent = data.error || `${data.message} Chunks: ${data.chunks}`;
  } catch (err) {
    uploadStatus.textContent = 'Upload failed: ' + err.message;
  }
});

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('question');
  const question = input.value.trim();
  if (!question) return;
  addMessage(question, 'user');
  input.value = '';
  try {
    const res = await fetch('/chat', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question})
    });
    const data = await res.json();
    if (data.error) addMessage(data.error, 'bot');
    else {
      const sources = (data.sources || []).map(s => `${s.filename} (chunk ${s.chunk_index})`).join(', ');
      addMessage(data.answer, 'bot', `Validated: ${data.validated} · Sources: ${sources}`);
    }
  } catch (err) {
    addMessage('Request failed: ' + err.message, 'bot');
  }
});
