const form = document.getElementById('gen-form');
const output = document.getElementById('output');

async function generate(e) {
  e.preventDefault();
  const prompt = document.getElementById('prompt').value.trim();
  const max_tokens = parseInt(document.getElementById('max_tokens').value || '50', 10);
  const backend = document.getElementById('backend').value;
  const mode = document.getElementById('mode').value;

  if (mode === 'command') {
    return runCommand();
  }

  output.textContent = 'Generating...';
  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, max_tokens, backend })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    const data = await res.json();
    output.textContent = data.text ?? String(data);
  } catch (err) {
    output.textContent = `Error: ${err.message || err}`;
  }
}

form.addEventListener('submit', generate);

// Suggestions UI
const btnSuggest = document.getElementById('btn-suggest');
const privacySel = document.getElementById('privacy');
const suggestList = document.getElementById('suggest-list');

async function fetchSuggestions() {
  const privacy = privacySel.value;
  suggestList.innerHTML = '';
  const li = document.createElement('li');
  li.textContent = 'Fetching suggestions...';
  suggestList.appendChild(li);
  try {
    const res = await fetch(`/api/suggest?privacy=${encodeURIComponent(privacy)}`);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const data = await res.json();
    const items = Array.isArray(data.suggestions) ? data.suggestions : [];
    suggestList.innerHTML = '';
    if (!items.length) {
      const liEmpty = document.createElement('li');
      liEmpty.textContent = 'No suggestions at the moment.';
      suggestList.appendChild(liEmpty);
      return;
    }
    for (const tip of items) {
      const liTip = document.createElement('li');
      liTip.textContent = tip;
      suggestList.appendChild(liTip);
    }
  } catch (err) {
    suggestList.innerHTML = '';
    const liErr = document.createElement('li');
    liErr.textContent = `Error: ${err.message || err}`;
    suggestList.appendChild(liErr);
  }
}

if (btnSuggest) {
  btnSuggest.addEventListener('click', fetchSuggestions);
}

// Command mode
const btnCommand = document.getElementById('btn-command');

async function runCommand() {
  const text = document.getElementById('prompt').value.trim();
  if (!text) {
    output.textContent = 'Please enter a command.';
    return;
  }
  output.textContent = 'Running command...';
  try {
    const res = await fetch('/api/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    const data = await res.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    output.textContent = `Error: ${err.message || err}`;
  }
}

if (btnCommand) {
  btnCommand.addEventListener('click', runCommand);
}


