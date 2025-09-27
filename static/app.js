const messagesDiv = document.getElementById('messages');
const form = document.getElementById('chatForm');
const input = document.getElementById('input');
const darkToggle = document.getElementById('darkModeToggle');
const musicGodToggle = document.getElementById('musicGodToggle');
const portrait = document.getElementById('bachPortrait');

// Load preferences
const prefs = JSON.parse(localStorage.getItem('bach_prefs') || '{}');
// Session id for rolling memory
let sessionId = localStorage.getItem('bach_session_id') || null;
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

function appendMessage(author, text, cls = '', opts = {}) {
  const el = document.createElement('div');
  el.className = 'message ' + (author === 'Bach' ? 'bach' : 'user') + (cls ? ' ' + cls : '');
  if (opts.id) el.id = opts.id;
  el.innerHTML = `<strong>${author}:</strong> <span>${text}</span>`;
  messagesDiv.appendChild(el);
  // ensure we scroll to bottom when a new message arrives
  requestAnimationFrame(() => {
    // prefer scrollIntoView for reliability inside flex containers
    el.scrollIntoView({ behavior: 'smooth', block: 'end' });
  });
  return el;
}

function setTyping(on = true) {
  const exists = document.getElementById('typing');
  if (on && !exists) {
    appendMessage('Bach', '…thinking…', 'typing', { id: 'typing' });
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
    body: JSON.stringify({ message: text, music_god: !!prefs.musicGod, session_id: sessionId }),
  });

  const data = await res.json();
  setTyping(false);
  if (data.error) {
    appendMessage('System', data.error);
  } else {
    appendMessage('Bach', data.reply);
    // persist session id if server returned one
    if (data.session_id) {
      sessionId = data.session_id;
      localStorage.setItem('bach_session_id', sessionId);
    }
  }
});

// Ensure we start scrolled to the bottom on page load
window.addEventListener('load', () => {
  requestAnimationFrame(() => {
    // if there are messages, scroll to the last one
    const last = messagesDiv.lastElementChild;
    if (last) last.scrollIntoView({ block: 'end' });
  });
});

// When the input gains focus, make sure the last message is visible so the input remains on-screen
input.addEventListener('focus', () => {
  requestAnimationFrame(() => {
    const last = messagesDiv.lastElementChild;
    if (last) last.scrollIntoView({ block: 'end' });
  });
});
