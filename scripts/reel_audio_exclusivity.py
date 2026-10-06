from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old="A('[data-reel-sound]',e=>{const v=e.closest('.transfer-card')?.querySelector('video');if(!v)return;v.muted=!v.muted;v.volume=1;v.play().catch(()=>{});e.textContent=v.muted?'🔇':'🔊';e.setAttribute('aria-pressed',String(!v.muted))});"
new="A('[data-reel-sound]',e=>{const v=e.closest('.transfer-card')?.querySelector('video');if(!v)return;document.querySelectorAll('.reels-feed video').forEach(x=>{if(x!==v){x.pause();x.muted=true}});v.muted=!v.muted;v.volume=1;v.play().catch(()=>{});e.textContent=v.muted?'🔇':'🔊';e.setAttribute('aria-pressed',String(!v.muted))});"
if old not in s: raise SystemExit('sound handler not found')
s=s.replace(old,new,1)
old2="if(active){active.muted=false;active.volume=1;active.play().catch(()=>{})}"
new2="if(active){feed.querySelectorAll('video').forEach(x=>{if(x!==active){x.pause();x.muted=true}});active.muted=false;active.volume=1;active.play().catch(()=>{})}"
if old2 not in s: raise SystemExit('pointer unlock block not found')
s=s.replace(old2,new2,1)
old3="document.addEventListener('pointerdown',e=>{if(e.target.closest('button'))soundTap(classifyTap(e.target))},{passive:true});"
new3="document.addEventListener('pointerdown',e=>{if(e.target.closest('[data-reel-sound],.reels-feed video'))return;if(e.target.closest('button'))soundTap(classifyTap(e.target))},{passive:true});"
if old3 not in s: raise SystemExit('global sound listener not found')
s=s.replace(old3,new3,1)
p.write_text(s)
print('reel audio exclusivity and click-sound isolation applied')
