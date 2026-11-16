/* Project scenes: one small SVG animation per project, built from what it does.
   Ported unchanged from the original homepage. A box <div class="proj-viz" data-viz="key">
   gets its scene drawn here; it builds once when it scrolls into view, loops only while
   on screen, and replays on hover. Without JS the box is just an empty decorative panel
   (the project's text is all in the HTML). */
(function () {
'use strict';
const motion = document.documentElement.classList.contains('js-motion');
const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
const $ = (s, c) => (c || document).querySelector(s), $$ = (s, c) => [...(c || document).querySelectorAll(s)];
const st=(d,x)=>' style="--d:'+d+'s'+(x?';'+x:'')+'"';
const T=(x,y,s,c,d,a)=>'<text x="'+x+'" y="'+y+'" class="vt '+(c||'')+'"'+(d!=null?st(d):'')+(a?' '+a:'')+'>'+s+'</text>';
const Rc=(x,y,w,h,c,d,rx,a)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+(rx==null?4:rx)+'" class="'+c+'"'+(d!=null?st(d):'')+(a?' '+a:'')+'/>';
const P=(d,c,dl,a)=>'<path d="'+d+'" class="'+c+'" pathLength="1"'+(dl!=null?st(dl):'')+(a?' '+a:'')+'/>';
const C=(x,y,r,c,dl,a)=>'<circle cx="'+x+'" cy="'+y+'" r="'+r+'" class="'+c+'"'+(dl!=null?st(dl):'')+(a?' '+a:'')+'/>';
const G=(c,d,inner,x)=>'<g class="'+c+'"'+st(d,x)+'>'+inner+'</g>';
const MID='text-anchor="middle"', END='text-anchor="end"';
const wave=(x0,n,gap,cy,amp,seed)=>{let s='';for(let i=0;i<n;i++){const h=5+Math.abs(Math.sin(i*1.7+seed))*amp;s+=Rc(x0+i*gap,cy-h/2,2.6,h,'vb s-wave',-(i*.13).toFixed(2),1.3,'opacity=".85"');}return s;};

const SCENES={
research:()=>
  Rc(18,16,196,20,'vp s-in',0,6)+T(28,29.5,'acme-logistics.com','hi s-type',.15)+T(204,29.5,'↵','lo s-in',.9,END)+
  Rc(18,48,150,5,'vg s-gx',1,2.5)+Rc(18,60,118,5,'vg s-gx',1.1,2.5)+Rc(18,72,136,5,'vg s-gx',1.2,2.5)+
  T(18,94,'hiring · funding · new warehouse','s-in',1.35)+
  C(266,60,30,'vl',null,'stroke-width="5" opacity=".45"')+
  '<g transform="rotate(-90 266 60)">'+C(266,60,30,'va s-arc',null,'stroke-width="5" pathLength="100" stroke-dasharray="87 100" style="--d:1.2s;--len:87"')+'</g>'+
  T(266,65,'87','big hi s-pop',1.8,MID)+T(266,108,'LEAD SCORE','sm lo s-in',1.8,MID)+
  T(18,124,'✓ outreach email drafted','gn s-in',2.2),

voice:()=>
  T(18,22,'INBOUND CALL · 00:42','sm lo')+wave(18,26,6,62,30,0)+
  T(18,118,'“Thursday afternoon?”','hi s-type',.3)+
  T(196,22,'THU 26 SEP','sm lo')+
  [0,1,2].map(r=>[0,1,2,3].map(c=>Rc(196+c*27,30+r*21,23,17,'vp',null,3)).join('')).join('')+
  G('s-pop',1.2,Rc(223,51,23,17,'vf',null,3)+T(234.5,62.5,'14:30','sm hi',null,MID))+
  T(196,118,'✓ booked · email sent','gn s-in',1.6),

zephra:()=>{
  const prof=[[18,9],[26,30],[40,28],[56,18],[70,24],[90,34],[114,44]];
  const R=prof.map(([y,w])=>(110+w)+' '+y).join(' L'), L=prof.slice().reverse().map(([y,w])=>(110-w)+' '+y).join(' L');
  const out='M'+R+' L'+L+' Z';
  let s='';
  prof.forEach(([y,w],i)=>{s+='<ellipse cx="110" cy="'+y+'" rx="'+w+'" ry="'+(w*.2).toFixed(1)+'" class="vl s-in"'+st(i*.07)+'/>';});
  [0,-1.25,-2.5,-3.75].forEach(d=>{s+='<path d="'+out+'" class="va s-mer" opacity=".55"'+st(d)+'/>';});
  s+=T(204,28,'SILHOUETTE','sm lo');
  ['A-LINE','SHIFT','WRAP'].forEach((n,i)=>{s+=G('s-pop',.3+i*.12,Rc(204,36+i*22,70,17,i===0?'vf':'vp',null,4)+T(239,47.5+i*22,n,'sm hi',null,MID));});
  s+=T(204,114,'webgl · drag to rotate','ac s-in',1);
  return s;},

ahl:()=>
  Rc(18,10,284,120,'vp',null,8)+C(30,21,2.5,'vg')+C(38,21,2.5,'vg')+C(46,21,2.5,'vg')+T(60,24,'AI Human Labs demo','sm lo')+
  '<path d="M18 31H302" class="vl"/>'+
  Rc(34,46,124,8,'vb s-gx',.3,2)+Rc(34,60,92,8,'vg s-gx',.45,2)+Rc(34,76,150,3,'vg s-gx',.6,1.5)+Rc(34,83,120,3,'vg s-gx',.66,1.5)+
  G('s-pop',.8,Rc(34,92,50,13,'vf',null,6.5)+T(59,101,'Book a call','sm hi',null,MID))+
  C(248,68,20,'vg s-pop',.5)+C(248,68,20,'va s-ring',0)+C(248,68,6,'vb s-pop',.7)+
  '<clipPath id="ahlc"><rect x="18" y="110" width="284" height="18"/></clipPath><g clip-path="url(#ahlc)"><g class="s-slide">'+
  Array.from({length:12},(_,i)=>Rc(34+i*48,112,42,13,'vp',null,3)+T(55+i*48,121,['LAW','CLINIC','RETAIL','ESTATE','LOGISTIC','EDU'][i%6],'sm lo',null,MID)).join('')+'</g></g>',

leadforge:()=>{
  let s='';
  ['IG','YT','IN','X','TH','UP'].forEach((n,i)=>{const y=12+i*20;
    s+=Rc(18,y,34,14,'vp s-in',i*.07,4)+T(35,y+9.8,n,'sm hi s-in',i*.07,MID)+
      P('M52 '+(y+7)+'H198','vl s-draw',.35+i*.06)+C(52,y+7,1.8,'vb s-flow',null,'style="--d:-'+(i*.4).toFixed(1)+'s;--dx:146px"');});
  s+=Rc(198,12,5,114,'vf s-gy',.9,2.5)+T(209,20,'DEDUPE','sm lo s-in',1);
  s+=G('s-pop',1.05,'<ellipse cx="264" cy="44" rx="34" ry="8" class="vp"/>'+Rc(230,44,68,46,'vp',null,0)+'<path d="M230 44V90A34 8 0 0 0 298 90V44" class="vp"/>'+'<ellipse cx="264" cy="44" rx="34" ry="8" class="vp"/>');
  s+=T(264,74,'12,480','big hi s-pop',1.35,MID)+T(264,112,'unified · −3,112 dupes','sm lo s-in',1.55,MID);
  return s;},

munirquote:()=>{
  const X=[40,120,200,280], L=['CALL','SHEET','QUOTE','WHATSAPP'];
  const icon=[ (x)=>Rc(x-6,54,2.4,8,'vb',null,1)+Rc(x-1.5,51,2.4,14,'vb',null,1)+Rc(x+3,55,2.4,6,'vb',null,1),
    (x)=>Rc(x-8,50,16,16,'vl',null,2)+'<path d="M'+(x-8)+' 55.3H'+(x+8)+'M'+(x-8)+' 60.6H'+(x+8)+'M'+(x-2.7)+' 50V66M'+(x+2.7)+' 50V66" class="vl"/>',
    (x)=>Rc(x-6,49,12,17,'vl',null,2)+Rc(x-3,53,6,1.6,'vb',null,.8)+Rc(x-3,57,6,1.6,'vg',null,.8)+Rc(x-3,61,4,1.6,'vg',null,.8),
    (x)=>C(x,57,7,'vl')+'<path d="M'+(x-5)+' 62L'+(x-7)+' 66L'+(x-2)+' 64" class="vl"/>' ];
  let s='';
  X.forEach((x,i)=>{ if(i) s+=P('M'+(X[i-1]+18)+' 58H'+(x-18),'va s-draw',.15+i*.35);
    s+=G('s-pop',i*.35,C(x,58,17,'vp')+icon[i](x))+T(x,92,L[i],'sm lo s-in',i*.35+.1,MID);});
  s+=G('s-in',1.5,Rc(150,104,152,22,'vp',null,6))+T(160,118,'Quote #A-219 · PKR 184,500','hi sm s-type',1.6)+T(296,118,'✓✓','ac sm s-in',2.1,END);
  s+=T(18,118,'0 manual steps','ac s-in',1.8);
  return s;},

bresco:()=>{
  let s=Rc(18,14,152,14,'vg',null,3)+T(24,23.5,'NAME','sm lo')+T(78,23.5,'PHONE','sm lo')+T(140,23.5,'SRC','sm lo');
  [0,1,2].forEach(i=>{const y=31+i*16;s+=Rc(18,y,152,13,'vp',null,3)+Rc(24,y+5,34,3,'vg',null,1.5)+Rc(78,y+5,48,3,'vg',null,1.5)+Rc(140,y+5,20,3,'vg',null,1.5);});
  s+=G('s-in',.5,Rc(18,80,152,13,'vp',null,3)+Rc(18,80,152,13,'vf',null,3,'opacity=".18"')+T(24,89,'Hamza R.','sm hi')+T(78,89,'+92 3·· ···4417','sm hi')+T(140,89,'NEW','sm ac'));
  s+=P('M172 86 C194 86 200 60 222 60','va s-draw',.9);
  s+=C(248,60,17,'va s-ring',1.3)+C(248,60,17,'va s-ring',2.4)+G('s-pop',1.2,C(248,60,17,'vp')+'<path d="M242 54c1.5 4 4 7 8 9l2.4-2.4 4 1.8-.8 3.6c-7 0-15-8-15-15l3.6-.8 1.8 4z" class="vb"/>');
  s+=T(214,100,'dialing…','hi s-type',1.4)+T(214,116,'0.8s after the row landed','ac sm s-in',1.9);
  return s;},

whatsapp:()=>
  Rc(18,10,178,120,'vp',null,10)+
  G('s-pop',.2,Rc(28,20,122,18,'vg',null,7)+T(35,32,'Is the 3-bed still available?','sm hi'))+
  G('s-pop',.7,Rc(78,44,108,18,'vf',null,7)+T(85,56,'Yes! Budget and area?','sm hi'))+
  G('s-pop',1.2,Rc(28,68,92,18,'vg',null,7)+T(35,80,'~50 lakh · DHA Ph 6','sm hi'))+
  G('s-in',1.5,Rc(28,94,40,16,'vg',null,8)+C(39,102,2,'vb s-blink',0)+C(48,102,2,'vb s-blink',.2)+C(57,102,2,'vb s-blink',.4))+
  P('M196 70 C212 70 210 32 228 32','vl s-draw',1.6)+P('M196 70H228','va s-draw',1.6)+P('M196 70 C212 70 210 108 228 108','vl s-draw',1.6)+
  G('s-in',1.8,Rc(228,24,76,16,'vp',null,4)+T(235,35,'Sana · busy','sm lo'))+
  G('s-pop',2,Rc(228,62,76,16,'vp',null,4,'style="stroke:#3B7DE0"')+T(235,73,'Ali · assigned','sm hi'))+
  G('s-in',1.8,Rc(228,100,76,16,'vp',null,4)+T(235,111,'Umer · away','sm lo')),

sdr:()=>
  Rc(18,12,152,94,'vp s-in',0,8)+T(28,28,'to: ops@northwind.io','sm lo s-in',.1)+
  Rc(28,38,120,4,'vb s-gx',.3,2)+Rc(28,49,132,4,'vg s-gx',.42,2)+Rc(28,60,98,4,'vg s-gx',.54,2)+Rc(28,71,114,4,'vg s-gx',.66,2)+
  G('s-pop',1.1,Rc(116,84,44,15,'vl',null,4,'style="stroke:#3B7DE0"')+T(138,94.5,'SENT','sm ac',null,MID))+
  Rc(18,120,284,2,'vg',null,1)+Rc(18,120,284,2,'vf s-gx',1.3,1)+C(18,121,3,'vb')+C(302,121,3,'vb s-pop',2.1)+T(302,114,'+48h','sm ac s-in',1.9,END)+
  G('s-pop',2.1,Rc(188,26,114,64,'vp',null,8)+T(198,42,'follow-up #2','sm hi')+Rc(198,50,84,3,'vg',null,1.5)+Rc(198,58,92,3,'vg',null,1.5)+T(198,80,'new angle: they’re hiring','sm ac')),

content:()=>{
  let s=G('s-pop',0,Rc(18,44,70,52,'vp',null,8)+'<path d="M47 60v20l16-10z" class="vb"/>')+T(53,110,'1 video','sm hi s-in',.1,MID);
  s+=P('M88 70H112','va s-draw',.3)+G('s-pop',.5,Rc(112,58,40,24,'vp',null,6)+T(132,73,'REVIEW','sm ac',null,MID));
  const Y=[18,44,70,96,122], N=['short · 0:45','linkedin post','x thread','newsletter','voiceover'];
  Y.forEach((y,i)=>{s+=P('M152 70 C176 70 182 '+y+' 206 '+y,'vl s-draw',.8+i*.07)+G('s-in',1.05+i*.1,Rc(206,y-9,96,18,'vp',null,5)+T(214,y+3.5,N[i],'sm hi'));});
  return s;},

receptionist:()=>
  C(160,60,20,'va s-ring',0)+C(160,60,20,'va s-ring',-.73)+C(160,60,20,'va s-ring',-1.46)+
  G('s-pop',.1,C(160,60,20,'vf')+Rc(156,49,8,14,'vt-fill',null,4)+'<path d="M151 60a9 9 0 0 0 18 0M160 69v5" class="vw"/>')+
  T(18,28,'“Hi, I need to book a','hi sm s-type',.4)+T(18,40,'cleaning for Friday.”','hi sm s-type',.9)+
  G('s-pop',1.6,Rc(222,22,82,18,'vp',null,5,'style="stroke:#3B7DE0"')+T(230,34,'→ bookings','sm ac'))+
  T(160,118,'webrtc · no phone line','sm lo s-in',.2,MID),

sentry:()=>
  Rc(18,12,96,116,'vp',null,8)+T(28,28,'rules.md','sm ac')+
  T(28,46,'refunds < 14 days','sm lo s-in',.1)+T(28,60,'no legal advice','sm lo s-in',.2)+T(28,74,'billing → human','sm lo s-in',.3)+Rc(28,86,60,3,'vg s-gx',.4,1.5)+Rc(28,94,48,3,'vg s-gx',.5,1.5)+
  G('s-pop',.5,Rc(126,14,124,18,'vg',null,7)+T(133,26,'Where is order #884?','sm hi'))+
  G('s-pop',.9,Rc(162,38,140,18,'vf',null,7)+T(169,50,'Shipped today · arrives Thu','sm hi'))+
  T(302,70,'✓ resolved','sm gn s-in',1.2,END)+
  G('s-pop',1.5,Rc(126,80,124,18,'vg',null,7)+T(133,92,'Can I dispute this charge?','sm hi'))+
  G('s-pop',2.1,Rc(186,104,116,18,'vp',null,7,'style="stroke:#E01E33"')+T(194,116,'escalated → human','sm rd')),

vape:()=>
  '<path d="M18 26V14H30M290 14H302V26M302 114V126H290M30 126H18V114" class="vl"/>'+
  C(28,22,2.6,'vb s-blink',0)+T(35,25,'CAM 04 · HALL B','sm lo')+
  [70,152,234].map(x=>C(x,50,9,'vd')+Rc(x-13,62,26,48,'vd',null,9)).join('')+
  G('s-scan',0,Rc(18,16,284,1.5,'vb',null,.5,'opacity=".7"'),'--dy:106px')+
  Rc(132,34,40,82,'vr s-draw',1,3,'pathLength="1"')+
  G('s-pop',1.6,Rc(132,22,52,11,'vrf',null,2)+T(136,30.5,'VAPE 0.94','sm hi'))+
  T(296,134,'→ WhatsApp alert sent','sm hi s-type',1.9,END),

bridge:()=>{
  let s=Rc(18,12,190,20,'vp',null,6)+T(28,25.5,'coffee · atlanta, GA','hi s-type',.2)+T(218,25,'FOOD','sm ac s-in',.4)+T(248,25,'BEAUTY','sm lo s-in',.45)+T(286,25,'LAW','sm lo s-in',.5);
  for(let i=0;i<10;i++){const x=18+(i%5)*58,y=i<5?42:84;s+=G('s-pop',.6+i*.05,Rc(x,y,52,36,'vp',null,6)+C(x+11,y+11,5,'vg')+Rc(x+7,y+22,34,3,'vg',null,1.5)+Rc(x+7,y+28,22,3,'vg',null,1.5));
    if([1,4,7].includes(i)) s+=Rc(x,y,52,36,'va s-draw',1.3+i*.05,6,'pathLength="1"');}
  s+=T(18,134,'3 of 214 Black-owned businesses match','sm ac s-in',1.7);
  return s;},

echo:()=>
  C(24,26,7,'vg')+C(29,31,2.6,'vgn s-blink',0)+
  G('s-pop',.2,Rc(38,16,128,18,'vg',null,7)+T(45,28,'did the deploy go out?','sm hi'))+
  G('s-pop',.7,Rc(160,42,142,18,'vf',null,7)+T(167,54,'yep, live 2 min ago','sm hi'))+
  T(302,72,'✓✓ read','sm ac s-in',1.1,END)+
  G('s-pop',1.5,Rc(248,62,26,13,'vp',null,6.5)+T(261,71.5,'+1','sm hi',null,MID))+
  G('s-in',1.3,Rc(38,84,44,16,'vg',null,8)+C(50,92,2,'vb s-blink',0)+C(60,92,2,'vb s-blink',.2)+C(70,92,2,'vb s-blink',.4))+
  T(18,124,'4 online · #launch','sm lo'),

aura:()=>
  Rc(18,14,100,84,'vp',null,8)+C(68,52,20,'vl')+
  P('M44 34V28H50M86 28H92V34M92 70V76H86M50 76H44V70','va s-draw',.3)+
  T(68,114,'calm · 0.82','sm ac s-in',1.1,MID)+
  '<path d="M132 104H302M132 20V104" class="vl"/>'+
  P('M132 80 C150 60 160 90 178 70 S206 40 222 58 S250 84 266 52 S290 34 302 44','vs s-draw',.4)+
  C(302,44,3,'vb s-pop',1.3)+T(302,124,'mood · 14 days','sm lo',null,END),

groupxam:()=>
  Rc(18,12,284,116,'vp',null,8)+T(28,27,'Q4/20 · integrals','sm lo')+T(292,27,'02:14','sm ac',null,END)+
  P('M40 58 C60 40 80 76 100 58 S140 44 150 62','vs s-draw',.3)+
  T(40,84,'∫ x² dx = x³/3 + C','hi s-type',.9)+
  P('M190 96 C210 70 240 110 260 80 S284 70 290 88','va s-draw',1.3)+
  G('s-drift',0,'<path d="M170 60l0 12 3.4-3.2 2.6 5.4 2-1-2.6-5.2 4.6-.4z" class="vb"/>'+Rc(180,72,26,11,'vf',null,3)+T(193,80,'Sara','sm hi',null,MID),'--px:14px')+
  G('s-drift',-3,'<path d="M236 100l0 12 3.4-3.2 2.6 5.4 2-1-2.6-5.2 4.6-.4z" class="vb"/>'+Rc(246,112,28,11,'vp',null,3)+T(260,120,'Omar','sm hi',null,MID),'--px:10px'),

flowstate:()=>{
  const rows=[[0,'Launch v2',1],[1,'Landing page',1],[2,'Hero copy',1],[2,'Pricing table',0],[1,'Email sequence',0],[0,'Hire designer',0]];
  let s='<path d="M28 30V88M46 48V80" class="vl"/>';
  rows.forEach(([l,n,done],i)=>{const x=22+l*18,y=16+i*18;
    s+=G('s-in',i*.08,Rc(x,y,9,9,'vp',null,2)+T(x+15,y+8,n,'sm '+(done?'lo':'hi')));
    if(done) s+=P('M'+(x+2)+' '+(y+4.6)+'l2.2 2.4 4.4-5','va s-draw',.6+i*.28);});
  s+=T(302,24,'3 / 6','ac s-in',1.5,END)+Rc(242,32,60,3,'vg',null,1.5)+Rc(242,32,30,3,'vf s-gx',1.5,1.5);
  return s;},

corecast:()=>
  '<path d="M18 112H302M18 14V112" class="vl"/>'+
  '<path d="M200 62 L250 44 L302 36 L302 70 L250 72 L200 70Z" class="vg s-in"'+st(.9)+'/>'+
  P('M18 88 L36 80 L54 84 L72 70 L90 76 L108 64 L126 70 L144 58 L162 66 L180 56 L200 66','vs s-draw',.2)+
  P('M200 66 L250 58 L302 52','va s-draw',1,'stroke-dasharray="3 3"')+
  T(200,126,'today','sm lo',null,MID)+'<path d="M200 14V112" class="vl" stroke-dasharray="2 3"/>'+
  G('s-pop',1.5,Rc(226,16,76,18,'vp',null,5)+T(264,28,'−15% error','sm gn',null,MID)),

aurelle:()=>
  G('s-drift',0,Rc(56,30,118,78,'vp',null,3),'--px:4px')+
  G('s-drift',-2,Rc(110,20,112,90,'vp',null,3,'opacity=".9"'),'--px:9px')+
  G('s-drift',-4,Rc(164,42,96,64,'vg',null,3),'--px:15px')+
  T(160,70,'MAISON AURELLE','ws hi s-type',.4,MID)+
  Rc(300,14,2,112,'vg',null,1)+Rc(300,14,2,44,'vb s-gy',.6,1)+
  T(18,132,'scroll · 03 / 07','sm lo')
};

$$('.proj-viz').forEach(box => {
  const fn = SCENES[box.dataset.viz]; if (!fn) return;
  box.innerHTML = '<svg viewBox="0 0 320 140" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">' + fn() + '</svg>';
});
function runScene(v) { v.classList.toggle('run', false); void v.offsetWidth; v.classList.add('run'); v.dataset.t = performance.now(); }
if (!('IntersectionObserver' in window)) { $$('.proj-viz').forEach(runScene); return; }
const vio = new IntersectionObserver(es => es.forEach(e => {
  const v = e.target;
  v.classList.toggle('live', e.isIntersecting);
  if (e.isIntersecting && !v.dataset.ran) { v.dataset.ran = '1'; setTimeout(() => runScene(v), motion ? 260 : 0); }
}), { threshold: .3 });
$$('.proj-viz').forEach(v => vio.observe(v));
if (fine && motion) $$('.pj,.pcard').forEach(c => c.addEventListener('mouseenter', () => {
  const v = $('.proj-viz', c); if (v && v.dataset.ran && performance.now() - (+v.dataset.t || 0) > 3500) runScene(v);
}));
})();
