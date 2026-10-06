from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old="<button class=\"${S.reelReposts[i]?'active':''}\" data-reel-repost=\"${i}\" aria-label=\"${T('share')}\">↻</button></div></article>`}"
new="<button class=\"${S.reelReposts[i]?'active':''}\" data-reel-repost=\"${i}\" aria-label=\"${T('share')}\">↻</button><button data-reel-sound=\"${i}\" aria-label=\"صوت الفيديو\">🔊</button></div></article>`}"
if old not in s: raise SystemExit('transferCard action markup not found')
s=s.replace(old,new,1)
# Do not force the reminder video muted at markup time; the user can hear it after the play gesture.
s=s.replace('<video class="reel-ad-video" autoplay controls muted playsinline volume="1"', '<video class="reel-ad-video" autoplay controls playsinline volume="1"',1)
# Add a delegated sound control next to the like/repost handlers.
oldb="A('[data-reel-repost]',e=>{const i=e.dataset.reelRepost;S.reelReposts[i]=!S.reelReposts[i];e.classList.toggle('active',!!S.reelReposts[i]);e.setAttribute('aria-pressed',String(!!S.reelReposts[i]));localStorage.setItem('yawaqit-reel-reposts',JSON.stringify(S.reelReposts))});"
newb=oldb+"A('[data-reel-sound]',e=>{const v=e.closest('.transfer-card')?.querySelector('video');if(!v)return;v.muted=!v.muted;v.volume=1;v.play().catch(()=>{});e.textContent=v.muted?'🔇':'🔊';e.setAttribute('aria-pressed',String(!v.muted))});"
if oldb not in s: raise SystemExit('repost binding not found')
s=s.replace(oldb,newb,1)
# Make the floating back control compact and not a bar.
css='.reels-back{pointer-events:auto!important}.reels-back .ib{width:34px;height:34px;padding:0;border-radius:50%!important}'
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('per-reel sound control and audible reminder video applied')
