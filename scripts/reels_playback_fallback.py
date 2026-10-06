from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old="feed.querySelectorAll('video').forEach(v=>io.observe(v))}"
new="feed.querySelectorAll('video').forEach(v=>{v.onclick=()=>{feed.querySelectorAll('video').forEach(x=>{if(x!==v){x.pause();x.muted=true}});v.muted=!v.muted;v.volume=1;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})})};io.observe(v)})}"
if old not in s: raise SystemExit('observer tail not found')
s=s.replace(old,new,1)
old2="v.volume=1;v.play().catch(()=>{})}else if(!e.isIntersecting)v.pause()"
new2="v.volume=1;v.muted=false;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})})}else if(!e.isIntersecting)v.pause()"
if old2 not in s: raise SystemExit('observer play call not found')
s=s.replace(old2,new2,1)
p.write_text(s)
print('reel playback fallback applied')
