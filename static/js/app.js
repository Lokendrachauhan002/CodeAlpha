/* Client-side chat UI: history is intentionally kept in this browser only. */
const chat = document.querySelector('#chatMessages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#messageInput');
const suggestions = document.querySelector('#suggestionBar');
let history = JSON.parse(localStorage.getItem('campusAssistHistory') || '[]');
const now = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
function escapeHtml(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }
function addMessage(role, text, extra = '') { const item = { role, text, time: now(), extra }; if (!extra) { history.push(item); localStorage.setItem('campusAssistHistory', JSON.stringify(history)); } renderMessage(item); }
function renderMessage(item) { const isUser = item.role === 'user'; chat.insertAdjacentHTML('beforeend', `<article class="message ${isUser ? 'user' : ''}"><div class="avatar">${isUser ? 'YOU' : 'CA'}</div><div><div class="bubble">${escapeHtml(item.text)}</div><div class="meta">${item.time}${item.extra}</div></div></article>`); chat.scrollTop = chat.scrollHeight; }
function renderHistory() { chat.innerHTML = ''; if (history.length) history.forEach(renderMessage); else addMessage('bot', 'Hello! I am CampusAssist. Ask me anything about admissions, fees, exams, hostel, placements, and more.'); }
function setSuggestions(items = []) { suggestions.innerHTML = items.map(x => `<button class="suggestion" data-q="${escapeHtml(x.question)}">${escapeHtml(x.question)}</button>`).join(''); }
function showTyping() { chat.insertAdjacentHTML('beforeend', '<article id="typing" class="message"><div class="avatar">CA</div><div class="bubble typing-dots"><span>●</span> <span>●</span> <span>●</span></div></article>'); chat.scrollTop = chat.scrollHeight; }
async function sendMessage(text) { addMessage('user', text); input.value = ''; setSuggestions(); showTyping(); try { const response = await fetch('/api/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:text}) }); const data = await response.json(); document.querySelector('#typing')?.remove(); if (!response.ok) throw new Error(data.error || 'Request failed.'); const detail = ` · <span class="confidence">${data.confidence}% confidence</span>`; addMessage('bot', data.answer, detail); setSuggestions(data.suggestions); } catch (error) { document.querySelector('#typing')?.remove(); addMessage('bot', `Error: ${error.message}`); } }
form.addEventListener('submit', event => { event.preventDefault(); const text = input.value.trim(); if (text) sendMessage(text); });
input.addEventListener('keydown', event => { if (event.key === 'Escape') input.value = ''; });
suggestions.addEventListener('click', event => { const question = event.target.dataset.q; if (question) sendMessage(question); });
document.querySelector('#clearButton').onclick = () => { history = []; localStorage.removeItem('campusAssistHistory'); setSuggestions(); renderHistory(); };
document.querySelector('#themeButton').onclick = () => { document.body.classList.toggle('dark'); localStorage.setItem('campusAssistTheme', document.body.classList.contains('dark') ? 'dark' : 'light'); };
if (localStorage.getItem('campusAssistTheme') === 'dark') document.body.classList.add('dark');
document.querySelector('#exportButton').onclick = () => { const text = history.map(x => `[${x.time}] ${x.role.toUpperCase()}: ${x.text}`).join('\n\n'); const link = document.createElement('a'); link.href = URL.createObjectURL(new Blob([text], {type:'text/plain'})); link.download = 'campusassist-chat.txt'; link.click(); URL.revokeObjectURL(link.href); };
const modalElement = document.querySelector('#faqModal');
const modal = window.bootstrap ? new bootstrap.Modal(modalElement) : { show: () => modalElement.classList.add('show') };
document.querySelector('#faqButton').onclick = () => { modal.show(); loadFaqs(); };
async function loadFaqs(term='') { const response = await fetch(`/api/faqs?search=${encodeURIComponent(term)}`); const data = await response.json(); document.querySelector('#faqResults').innerHTML = data.faqs.length ? data.faqs.map(f => `<div class="faq-item"><h3>${escapeHtml(f.question)}</h3><p>${escapeHtml(f.answer)}</p></div>`).join('') : '<p>No FAQs found.</p>'; }
let searchTimer; document.querySelector('#faqSearch').addEventListener('input', event => { clearTimeout(searchTimer); searchTimer=setTimeout(()=>loadFaqs(event.target.value), 250); });
renderHistory();
