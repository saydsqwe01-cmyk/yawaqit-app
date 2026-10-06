from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Keep exactly twelve orbiting pieces.
pat=r'(<div id="loadingScreen"[^>]*>.*?<div class="loading-orbit"[^>]*>).*?(</div></div></div>)'
m=re.search(pat,s,flags=re.S)
if not m: raise SystemExit('loading screen markup not found')
dots=''.join(f'<i style="--i:{i}"></i>' for i in range(12))
s=s[:m.start(1)]+m.group(1)+dots+m.group(2)+s[m.end(2):]
# Give the twelve circles a larger orbit and a smaller footprint so no adjacent pieces touch.
css='''.loading-orbit{width:86px;height:86px;margin-top:13px}.loading-orbit i{width:6px!important;height:6px!important;left:calc(50% - 3px)!important;top:-4px!important;transform-origin:3px 47px!important}.loading-orbit i:nth-child(n){animation-delay:calc(var(--i)*-.35s)!important;background:#08080a!important;box-shadow:0 0 7px rgba(0,0,0,.18)!important}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('twelve separated loading circles applied')
