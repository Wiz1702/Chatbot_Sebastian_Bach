const messagesDiv = document.getElementById('messages');
const form = document.getElementById('chatForm');
const input = document.getElementById('input');
const darkToggle = document.getElementById('darkModeToggle');
const musicGodToggle = document.getElementById('musicGodToggle');
const portrait = document.getElementById('bachPortrait');

// Load preferences
const prefs = JSON.parse(localStorage.getItem('bach_prefs') || '{}');
if (prefs.dark) {
  document.documentElement.classList.add('dark');
  if (darkToggle) darkToggle.checked = true;
}
if (prefs.musicGod) {
  if (musicGodToggle) musicGodToggle.checked = true;
}

if (darkToggle) {
  darkToggle.addEventListener('change', (e) => {
    document.documentElement.classList.toggle('dark', e.target.checked);
    prefs.dark = e.target.checked;
    localStorage.setItem('bach_prefs', JSON.stringify(prefs));
  });
}

if (musicGodToggle) {
  musicGodToggle.addEventListener('change', (e) => {
    prefs.musicGod = e.target.checked;
    localStorage.setItem('bach_prefs', JSON.stringify(prefs));
    // Announce mode change to the user
    if (prefs.musicGod) {
      appendMessage('Bach', 'I am now fully focused on musical questions only. Ask me anything about music.');
    } else {
      appendMessage('Bach', 'I have resumed normal conversation and may answer non-musical questions.');
    }
  });
}

function appendMessage(author, text, cls = '') {
  const el = document.createElement('div');
  el.className = 'message ' + (author === 'Bach' ? 'bach' : 'user') + (cls ? ' ' + cls : '');
  el.innerHTML = `<strong>${author}:</strong> <span>${text}</span>`;
  messagesDiv.appendChild(el);
  // ensure we scroll to bottom when a new message arrives
  requestAnimationFrame(() => {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  });
}

function setTyping(on = true) {
  const exists = document.getElementById('typing');
  if (on && !exists) {
    appendMessage('Bach', '…thinking…', 'typing');
  } else if (!on && exists) {
    exists.remove();
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  appendMessage('You', text);
  input.value = '';
  // show typing indicator
  setTyping(true);

  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text, music_god: !!prefs.musicGod }),
  });

  const data = await res.json();
  setTyping(false);
  if (data.error) {
    appendMessage('System', data.error);
  } else {
    appendMessage('Bach', data.reply);
  }
});
