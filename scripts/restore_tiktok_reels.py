from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
pat=r'function reelsPage\(\)\{return `.*?`\}'
new=r'''function reelsPage(){return `<div class="reels-feed"><div class="reels-topbar"><button id="bk" class="ib" aria-label="رجوع">${I('back')}</button><b>${U('reels')}</b><span></span></div>${TRANSFER_REELS.map((name,i)=>transferCard(name,i)).join('')}</div>`}'''
s,n=re.subn(pat,new,s,count=1)
if n!=1: raise SystemExit('reelsPage function not found')
css='''.reels-feed{position:relative!important}.reels-topbar{position:absolute;top:10px;left:10px;right:10px;z-index:8;display:flex;align-items:center;justify-content:space-between;padding:7px 10px;border:1px solid rgba(255,255,255,.22);border-radius:13px;background:rgba(0,0,0,.38);color:#fff;backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px);pointer-events:auto}.reels-topbar b{font-size:13px}.reels-topbar .ib{color:#fff;background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.3)}.reels-feed .transfer-card{scroll-snap-align:start}.reels-feed .transfer-video{object-fit:contain!important}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('TikTok-style reels feed restored')
