from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old="function transferCard(name,i,compact=false){const src=TRANSFER_URLS[i]||TRANSFER_START;return `<article class=\"transfer-card ${compact?'compact':''}\"><video class=\"transfer-video\" autoplay loop muted preload=\"none\" playsinline src=\"${src}\" volume=\"1\" aria-label=\"${name}\"></video><div class=\"reel-actions\"><button class=\"${S.reelLikes[i]?'active':''}\" data-reel-like=\"${i}\" aria-label=\"${T('like')}\">♥</button><button class=\"${S.reelReposts[i]?'active':''}\" data-reel-repost=\"${i}\" aria-label=\"${T('share')}\">↻</button></div></article>`}"
new="function transferCard(name,i,compact=false){const src=TRANSFER_URLS[i]||TRANSFER_START;const priority=i===S.reelIndex?'auto':'none';return `<article class=\"transfer-card ${compact?'compact':''}\"><video class=\"transfer-video\" autoplay loop muted preload=\"${priority}\" playsinline data-reel-index=\"${i}\" src=\"${src}\" volume=\"1\" aria-label=\"${name}\"></video><div class=\"reel-actions\"><button class=\"${S.reelLikes[i]?'active':''}\" data-reel-like=\"${i}\" aria-label=\"${T('like')}\">♥</button><button class=\"${S.reelReposts[i]?'active':''}\" data-reel-repost=\"${i}\" aria-label=\"${T('share')}\">↻</button></div></article>`}"
if old not in s: raise SystemExit('transferCard pattern not found')
s=s.replace(old,new)
old2="sc.querySelectorAll('video').forEach(v=>{v.volume=1;v.muted=false});const feed=sc.querySelector('.reels-feed');"
new2="sc.querySelectorAll('video').forEach(v=>{v.volume=1;v.muted=!!v.closest('.reels-feed')});const feed=sc.querySelector('.reels-feed');"
if old2 not in s: raise SystemExit('video pass pattern not found')
s=s.replace(old2,new2)
old3="feed.querySelectorAll('video').forEach(v=>io.observe(v))}"
new3="feed.querySelectorAll('video').forEach(v=>{v.onclick=()=>{v.muted=!v.muted;if(v.paused)v.play().catch(()=>{})};io.observe(v)})}"
if old3 not in s: raise SystemExit('observer pattern not found')
s=s.replace(old3,new3)
# Make the final single quick-action tile centered in the existing grid.
css=".home-quick-grid button:last-child{grid-column:1 / -1;justify-self:center;width:calc(50% - 3px)!important}"
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('video priority and audio centering fixes applied')
