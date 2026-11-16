/* Chat widget: opens the panel, sends the last 8 messages to /api/chat, shows the reply.
   Every failure ends in a visible message with the WhatsApp number. */
(function () {
const BOT='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M8 14h.01M16 14h.01"/></svg>';
const WA='+92 321 8234852';
const bubble=document.getElementById('chatBubble'), panel=document.getElementById('chatPanel'),
      closeBtn=document.getElementById('chatClose'), input=document.getElementById('chatInput'),
      sendBtn=document.getElementById('chatSend'), messagesEl=document.getElementById('chatMessages'),
      sugEl=document.getElementById('chatSuggestions'), notif=document.getElementById('chatNotif');
let messages=[], greeted=false;

function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function add(role,content){
  const d=document.createElement('div');
  d.className='msg'+(role==='user'?' user':'');
  const body=esc(content).replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>');
  d.innerHTML = role==='assistant'
    ? '<div class="msg-avatar">'+BOT+'</div><div class="msg-bubble">'+body+'</div>'
    : '<div class="msg-bubble">'+body+'</div>';
  messagesEl.appendChild(d); messagesEl.scrollTop=messagesEl.scrollHeight;
}
function typing(on){
  if(on){
    const d=document.createElement('div'); d.className='msg'; d.id='typing';
    d.innerHTML='<div class="msg-avatar">'+BOT+'</div><div class="msg-bubble"><div class="typing"><span></span><span></span><span></span></div></div>';
    messagesEl.appendChild(d); messagesEl.scrollTop=messagesEl.scrollHeight;
  } else document.getElementById('typing')?.remove();
}
bubble.addEventListener('click',()=>{
  panel.classList.toggle('open');
  if(panel.classList.contains('open')){
    notif.style.display='none';
    if(!greeted){ greeted=true; add('assistant',"Hey! I'm Rayyan's assistant. Ask me about his AI systems, how he works, or what he could build for you."); }
    setTimeout(()=>input.focus(),260);
  }
});
closeBtn.addEventListener('click',()=>panel.classList.remove('open'));
sugEl.addEventListener('click',e=>{ const b=e.target.closest('.suggestion'); if(!b) return; input.value=b.textContent; sugEl.style.display='none'; send(); });
input.addEventListener('keydown',e=>{ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); send(); } });
input.addEventListener('input',()=>{ input.style.height='auto'; input.style.height=Math.min(input.scrollHeight,80)+'px'; });
sendBtn.addEventListener('click',send);

async function send(){
  const text=input.value.trim(); if(!text) return;
  input.value=''; input.style.height='auto'; sendBtn.disabled=true; sugEl.style.display='none';
  add('user',text); messages.push({role:'user',content:text}); typing(true);
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:messages.slice(-8)})});
    const data=await r.json();
    const reply=data.reply||("Sorry, I couldn't get a response. Reach Rayyan directly on WhatsApp: "+WA);
    typing(false); messages.push({role:'assistant',content:reply}); add('assistant',reply);
  }catch(err){
    typing(false); add('assistant',"I'm having trouble connecting. Reach Rayyan directly on WhatsApp: "+WA);
  }
  sendBtn.disabled=false; input.focus();
}
})();
