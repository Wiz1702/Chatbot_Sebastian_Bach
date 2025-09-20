const messagesDiv = document.getElementById('messages');
const form = document.getElementById('chatForm');
const input = document.getElementById('input');

function appendMessage(author, text) {
  const el = document.createElement('div');
  el.className = 'message ' + (author === 'Bach' ? 'bach' : 'user');
  el.innerHTML = `<strong>${author}:</strong> <span>${text}</span>`;
  messagesDiv.appendChild(el);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  appendMessage('You', text);
  input.value = '';

  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text }),
  });

  const data = await res.json();
  if (data.error) {
    appendMessage('System', data.error);
  } else {
    appendMessage('Bach', data.reply);
  }
});
