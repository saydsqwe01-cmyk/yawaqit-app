from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Let autoplay start reliably; audio is unlocked by the user's tap/pointer gesture below.
s=s.replace('<video class="transfer-video" autoplay loop preload="${priority}" playsinline', '<video class="transfer-video" autoplay loop muted preload="${priority}" playsinline',1)
# Never force unmuting during render/intersection; this was causing browsers to reject playback and leave audio in a broken state.
s=s.replace("sc.querySelectorAll('video').forEach(v=>{v.volume=1;if(v.closest('.reels-feed'))v.muted=false});", "sc.querySelectorAll('video').forEach(v=>{v.volume=1});",1)
s=s.replace("v.volume=1;v.muted=false;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})})}else if(!e.isIntersecting)v.pause()", "v.volume=1;v.muted=true;v.play().catch(()=>{})}else if(!e.isIntersecting)v.pause()",1)
# Add a genuine pointer gesture unlock on the active reel; browser autoplay restrictions allow this path.
old="feed.querySelectorAll('video').forEach(v=>{v.onclick=()=>{v.muted=!v.muted;if(v.paused)v.play().catch(()=>{})};io.observe(v)})}"
new="feed.querySelectorAll('video').forEach(v=>{v.onclick=()=>{v.muted=!v.muted;v.volume=1;if(v.paused)v.play().catch(()=>{})};io.observe(v)});feed.addEventListener('pointerdown',e=>{if(e.target.closest('.reel-actions'))return;const active=[...feed.querySelectorAll('video')].find(v=>{const r=v.getBoundingClientRect();return r.top<innerHeight*.65&&r.bottom>innerHeight*.35})||feed.querySelector('video');if(active){active.muted=false;active.volume=1;active.play().catch(()=>{})}},{passive:true})}"
if old not in s: raise SystemExit('reel observer block not found')
s=s.replace(old,new,1)
p.write_text(s)
print('reel audio policy fixed with user-gesture unlock')
