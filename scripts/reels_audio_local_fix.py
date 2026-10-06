from pathlib import Path
import base64,re
root=Path('/home/ubuntu/work/yawaqit_extract')
p=root/'index.html'; s=p.read_text()
# Remove the reels top bar completely; keep only the vertical video feed.
s=s.replace('function reelsPage(){return `<div class="reels-feed"><div class="reels-topbar"><button id="bk" class="ib" aria-label="رجوع">${I(\'back\')}</button><b>${U(\'reels\')}</b><span></span></div>${TRANSFER_REELS.map((name,i)=>transferCard(name,i)).join(\'\')}</div>`}', 'function reelsPage(){return `<div class="reels-feed"><div class="reels-back"><button id="bk" class="ib" aria-label="رجوع">${I(\'back\')}</button></div>${TRANSFER_REELS.map((name,i)=>transferCard(name,i)).join(\'\')}</div>`}',1)
# Make the first three local videos start fetching immediately and remove forced mute.
s=s.replace('const priority=i===S.reelIndex?\'auto\':\'none\';return `<article class="transfer-card ${compact?\'compact\':\'\'}"><video class="transfer-video" autoplay loop muted preload="${priority}"', 'const priority=i<3?\'auto\':\'metadata\';return `<article class="transfer-card ${compact?\'compact\':\'\'}"><video class="transfer-video" autoplay loop preload="${priority}"',1)
# Replace the feed's forced mute behavior with audible playback and a muted fallback only when browser autoplay policy blocks it.
s=s.replace("sc.querySelectorAll('video').forEach(v=>{v.volume=1;v.muted=!!v.closest('.reels-feed')});", "sc.querySelectorAll('video').forEach(v=>{v.volume=1;if(v.closest('.reels-feed'))v.muted=false});",1)
s=s.replace("v.volume=1;v.play().catch(()=>{})}else if(!e.isIntersecting)v.pause()", "v.volume=1;v.muted=false;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})})}else if(!e.isIntersecting)v.pause()",1)
# Add only a discreet back button at the corner, not a bar.
css='.reels-back{position:absolute;top:10px;right:10px;z-index:8}.reels-back .ib{color:#fff;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}.prayer-mosque-art{bottom:-6px!important;opacity:.58!important}'
s=s.replace('</style>',css+'</style>',1)
# Embed the small interaction sounds as data URIs so they do not wait on separate requests.
files={'click':'click.mp3','correct':'correct.mp3','wrong':'wrong.mp3','notify':'notify.mp3','high':'high-score.mp3','giftOpen':'gift-open.mp3'}
data={k:'data:audio/mpeg;base64,'+base64.b64encode((root/'public/assets/audio'/fn).read_bytes()).decode() for k,fn in files.items()}
old=re.search(r"const EFFECT_AUDIO=\{[^}]+\};",s)
if not old: raise SystemExit('EFFECT_AUDIO declaration missing')
new='const EFFECT_AUDIO='+repr(data).replace("'",'"')+';'
s=s[:old.start()]+new+s[old.end():]
# Reuse preloaded in-memory audio objects to avoid creating a new network-backed Audio on every click.
s=s.replace("function playEffect(kind,after){try{const a=new Audio(EFFECT_AUDIO[kind]||EFFECT_AUDIO.click);a.volume=0.82;a.onended=()=>after&&after();a.play().catch(()=>after&&after());return a}catch(e){after&&after()}}", "const EFFECT_POOL={};Object.keys(EFFECT_AUDIO).forEach(k=>{const a=new Audio(EFFECT_AUDIO[k]);a.preload='auto';a.load();EFFECT_POOL[k]=a});function playEffect(kind,after){try{const a=EFFECT_POOL[kind]||EFFECT_POOL.click;a.pause();a.currentTime=0;a.volume=.82;a.onended=()=>after&&after();const p=a.play();if(p&&p.catch)p.catch(()=>after&&after());return a}catch(e){after&&after()}}",1)
p.write_text(s)
print('local reel audio, faster preload, top bar removal, and mosque opacity applied')
