/* Homepage hero: the 3D systems network (Three.js), ported unchanged from the original homepage.
   Loaded as a module on the homepage only. It waits for the hero intro ('hero:intro' event from
   site.js, or 5 s at most), renders only while on screen and the tab is visible, and falls back
   to nothing (class no-gl) if WebGL fails. Decorative: everything it shows is aria-hidden.
   Three.js itself (~600 KB) is only downloaded after `load`, and setup (WebGL context, shaders,
   the neighbour graph) runs at an idle moment, so neither competes with the first paint.
   IDLE_TIMEOUT_MS caps the wait. */
const THREE_URL='https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
const IDLE_TIMEOUT_MS=1200;
let THREE=null;
const wrap=document.getElementById('net'), canvas=document.getElementById('netCanvas');
const fail=e=>{ console.warn('network disabled',e); wrap.classList.add('no-gl'); };
const safeInit=()=>import(THREE_URL).then(m=>{ THREE=m; try{ init(); }catch(e){ fail(e); } },fail);
const whenIdle=f=>window.requestIdleCallback?requestIdleCallback(f,{timeout:IDLE_TIMEOUT_MS}):setTimeout(f,200);
if(wrap&&canvas){ if(document.readyState==='complete') whenIdle(safeInit); else addEventListener('load',()=>whenIdle(safeInit),{once:true}); }

function init(){
  const rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine=matchMedia('(hover: hover) and (pointer: fine)').matches;
  const small=innerWidth<760;
  const renderer=new THREE.WebGLRenderer({canvas,antialias:!small,alpha:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,small?1.5:1.75));
  renderer.setClearColor(0x000000,0);
  const scene=new THREE.Scene();
  scene.fog=new THREE.Fog(0x05070c,5.4,8.8);
  const camera=new THREE.PerspectiveCamera(38,1,.1,40);
  const group=new THREE.Group(); scene.add(group);

  const sprite=ring=>{
    const c=document.createElement('canvas'); c.width=c.height=64; const g=c.getContext('2d');
    if(ring){ g.strokeStyle='#fff'; g.lineWidth=3; g.beginPath(); g.arc(32,32,26,0,Math.PI*2); g.stroke(); }
    else{ const gr=g.createRadialGradient(32,32,0,32,32,32); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(.22,'rgba(255,255,255,.85)'); gr.addColorStop(1,'rgba(255,255,255,0)'); g.fillStyle=gr; g.fillRect(0,0,64,64); }
    const t=new THREE.CanvasTexture(c); t.colorSpace=THREE.SRGBColorSpace; return t;
  };
  const dot=sprite(false), ringTex=sprite(true);
  const mat=(size,color,map)=>new THREE.PointsMaterial({size,map:map||dot,color,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending,sizeAttenuation:true});

  /* nodes: fibonacci shell + a loose core */
  const N=small?72:130, R=1.7, pts=[], golden=Math.PI*(3-Math.sqrt(5));
  for(let i=0;i<N;i++){ const y=1-(i/(N-1))*2, r=Math.sqrt(1-y*y), th=golden*i, j=1+(Math.random()-.5)*.14;
    pts.push(new THREE.Vector3(Math.cos(th)*r*R*j,y*R*j,Math.sin(th)*r*R*j)); }
  for(let i=0;i<(small?8:16);i++) pts.push(new THREE.Vector3().randomDirection().multiplyScalar(.5+Math.random()*.65));
  const count=pts.length, pos=new Float32Array(count*3); pts.forEach((v,i)=>v.toArray(pos,i*3));
  const nodeGeo=new THREE.BufferGeometry(); nodeGeo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  const nodeMat=mat(.075,0x6ba6f5); group.add(new THREE.Points(nodeGeo,nodeMat));

  /* edges: 3 nearest neighbours */
  const adj=Array.from({length:count},()=>[]), seen=new Set(), edges=[];
  for(let i=0;i<count;i++){
    const d=[]; for(let j=0;j<count;j++) if(j!==i) d.push([pts[i].distanceToSquared(pts[j]),j]);
    d.sort((a,b)=>a[0]-b[0]);
    for(let k=0;k<3;k++){ const j=d[k][1], id=i<j?i+'-'+j:j+'-'+i; if(seen.has(id)) continue; seen.add(id); edges.push([i,j]); adj[i].push(j); adj[j].push(i); }
  }
  /* four named hubs, front-facing */
  const hubs=[[-.85,.55,.75],[.9,.45,.6],[-.6,-.7,.7],[.75,-.55,.75]].map(d=>{
    const v=new THREE.Vector3(...d).normalize().multiplyScalar(R); let best=0,bd=1e9;
    for(let i=0;i<N;i++){ const dd=pts[i].distanceToSquared(v); if(dd<bd){bd=dd;best=i;} } return best; });
  /* edges build outward from the first hub */
  const o=pts[hubs[0]], near=e=>Math.min(pts[e[0]].distanceTo(o),pts[e[1]].distanceTo(o));
  edges.sort((a,b)=>near(a)-near(b));
  const ep=new Float32Array(edges.length*6); edges.forEach(([a,b],i)=>{ pts[a].toArray(ep,i*6); pts[b].toArray(ep,i*6+3); });
  const edgeGeo=new THREE.BufferGeometry(); edgeGeo.setAttribute('position',new THREE.BufferAttribute(ep,3));
  const edgeMat=new THREE.LineBasicMaterial({color:0x3b7de0,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending});
  const lines=new THREE.LineSegments(edgeGeo,edgeMat); group.add(lines);

  const hp=new Float32Array(hubs.length*3); hubs.forEach((h,i)=>pts[h].toArray(hp,i*3));
  const hubGeo=new THREE.BufferGeometry(); hubGeo.setAttribute('position',new THREE.BufferAttribute(hp,3));
  const hubMat=mat(.2,0xeef3fb); group.add(new THREE.Points(hubGeo,hubMat));

  const ringGeo=new THREE.BufferGeometry(); ringGeo.setAttribute('position',new THREE.BufferAttribute(new Float32Array(3),3));
  const ringMat=mat(.2,0xe01e33,ringTex); group.add(new THREE.Points(ringGeo,ringMat));

  /* data pulses travelling the edges; one red pulse leaves the live hub */
  const pulses=(n,color,size)=>{
    const arr=new Float32Array(n*3), g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.BufferAttribute(arr,3));
    const m=mat(size,color); group.add(new THREE.Points(g,m));
    const list=[]; for(let i=0;i<n;i++){ const a=(Math.random()*count)|0; list.push({a,b:adj[a][(Math.random()*adj[a].length)|0],t:Math.random(),s:.55+Math.random()*.7}); }
    return {arr,g,m,list};
  };
  const blue=pulses(small?14:30,0xb9d3f8,.085), red=pulses(1,0xe01e33,.14);
  const advance=(pl,dt)=>{
    pl.list.forEach((q,i)=>{
      q.t+=dt*q.s;
      if(q.t>=1){ const prev=q.a; q.a=q.b; const nb=adj[q.a]; let nx=nb[(Math.random()*nb.length)|0]; if(nx===prev&&nb.length>1) nx=nb[(nb.indexOf(nx)+1)%nb.length]; q.b=nx; q.t=0; }
      const A=pts[q.a], B=pts[q.b];
      pl.arr[i*3]=A.x+(B.x-A.x)*q.t; pl.arr[i*3+1]=A.y+(B.y-A.y)*q.t; pl.arr[i*3+2]=A.z+(B.z-A.z)*q.t;
    });
    pl.g.attributes.position.needsUpdate=true;
  };

  /* HUD tags pinned to hubs */
  const tags=[...wrap.querySelectorAll('.hud-tag')];
  const MSG=[['new lead · WhatsApp','new lead · web form','new lead · Instagram ad'],['intent 87/100','budget + timeline captured','intent 64/100'],['contact + notes written','deal stage updated','owner assigned'],['call booked 14:30','task → Ali','quote sent on WhatsApp']];
  let active=-1, cyc=0, ringT=1, events=0;
  function fire(){
    active=(active+1)%4; if(active===0) cyc++; events++;
    tags.forEach((t,i)=>t.classList.toggle('on',i===active));
    tags[active].querySelector('span').textContent=MSG[active][cyc%3]; tw_.length=0;
    pts[hubs[active]].toArray(ringGeo.attributes.position.array,0); ringGeo.attributes.position.needsUpdate=true; ringT=0;
    const nb=adj[hubs[active]];
    for(let k=0;k<4;k++){ const q=blue.list[(Math.random()*blue.list.length)|0]; q.a=hubs[active]; q.b=nb[k%nb.length]; q.t=0; }
    Object.assign(red.list[0],{a:hubs[active],b:nb[0],t:0});
  }

  const read={rot:document.getElementById('nrRot'),links:document.getElementById('nrLinks'),ev:document.getElementById('nrEv')};
  if(read.links) read.links.textContent=String(edges.length).padStart(3,'0');

  let camBase=6.6;
  const resize=()=>{
    const w=wrap.clientWidth, h=wrap.clientHeight; if(!w||!h) return;
    renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix();
    camBase=Math.min(10,6.6/Math.min(1,(w/h)/1.05));
    group.position.x=w>760?-.25:0;
  };
  new ResizeObserver(()=>{ resize(); if(!raf) draw(performance.now()); }).observe(wrap); resize();

  const v=new THREE.Vector3(), tw_=[];
  function placeTags(alpha){
    const w=wrap.clientWidth, h=wrap.clientHeight;
    hubs.forEach((hi,i)=>{
      v.copy(pts[hi]).applyMatrix4(group.matrixWorld); const facing=v.z; v.project(camera);
      const x=(v.x*.5+.5)*w, y=(-v.y*.5+.5)*h, t=tags[i], tw=tw_[i]||(tw_[i]=t.offsetWidth);
      /* sit right of the node, flip left if it would clip, and never leave the canvas */
      const flip=x+14+tw>w-8;
      const left=Math.max(8,Math.min(w-tw-8,flip?x-14-tw:x+14));
      t.style.transform='translate3d('+left.toFixed(1)+'px,'+y.toFixed(1)+'px,0)';
      t.classList.toggle('flip',flip);
      const face=Math.max(0,Math.min(1,(facing+.3)*1.4));
      t.style.opacity=(alpha*face*(t.classList.contains('on')?1:.7)).toFixed(2);
    });
  }

  const mouse={x:0,y:0}, cur={x:0,y:0};
  if(fine&&!rm) addEventListener('pointermove',e=>{ mouse.x=e.clientX/innerWidth*2-1; mouse.y=e.clientY/innerHeight*2-1; },{passive:true});
  let introP=rm?1:0, introStart=null, base=.6, last=performance.now(), raf=0, onScreen=true, tabOn=!document.hidden, rd=0;
  const ease=p=>1-Math.pow(1-p,4);

  function draw(now){
    const dt=Math.min(.05,(now-last)/1000); last=now;
    if(introStart!==null&&introP<1) introP=Math.min(1,(now-introStart)/1900);
    const e=ease(introP);
    nodeMat.opacity=.95*e; hubMat.opacity=e; edgeMat.opacity=.28*e;
    blue.m.opacity=red.m.opacity=.95*Math.max(0,(introP-.45)/.55);
    lines.geometry.setDrawRange(0,Math.floor(edges.length*e)*2);
    group.scale.setScalar(.82+.18*e);
    if(!rm){ base+=dt*.09; cur.x+=(mouse.x-cur.x)*.05; cur.y+=(mouse.y-cur.y)*.05; advance(blue,dt); advance(red,dt*1.4); }
    const sp=Math.min(1,scrollY/innerHeight);
    group.rotation.y=base+cur.x*.35; group.rotation.x=.18+cur.y*.22+sp*.55;
    camera.position.z=camBase+sp*1.5;
    if(ringT<1){ ringT=Math.min(1,ringT+dt/1.1); ringMat.size=.18+ringT*.6; ringMat.opacity=(1-ringT)*.95*e; }
    group.updateMatrixWorld(); renderer.render(scene,camera);
    placeTags(introP>.6?Math.min(1,(introP-.6)/.4):0);
    if(read.rot && now-rd>250){ rd=now; read.rot.textContent=((group.rotation.y*57.2958)%360).toFixed(1).padStart(5,'0'); read.ev.textContent=String(events).padStart(4,'0'); }
  }
  function loop(now){ draw(now); raf=(onScreen&&tabOn)?requestAnimationFrame(loop):0; }
  const start=()=>{ if(!raf&&!rm&&onScreen&&tabOn){ last=performance.now(); raf=requestAnimationFrame(loop); } };
  new IntersectionObserver(es=>{ onScreen=es[0].isIntersecting; start(); }).observe(wrap);
  document.addEventListener('visibilitychange',()=>{ tabOn=!document.hidden; start(); });

  const go=()=>{
    if(introStart!==null) return; introStart=performance.now();
    if(rm){ fire(); draw(performance.now()); return; }
    setTimeout(fire,1300);
    setInterval(()=>{ if(onScreen&&tabOn) fire(); },2300);
    start();
  };
  if(rm){ fire(); draw(performance.now()); }
  else if(window.__heroGo) go();
  else { addEventListener('hero:intro',go,{once:true}); setTimeout(go,5000); draw(performance.now()); }
}
