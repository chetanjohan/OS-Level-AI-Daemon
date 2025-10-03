const form = document.getElementById('gen-form');
const output = document.getElementById('output');

async function generate(e) {
  e.preventDefault();
  const prompt = document.getElementById('prompt').value.trim();
  const max_tokens = parseInt(document.getElementById('max_tokens').value || '50', 10);
  const backend = document.getElementById('backend').value;

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


