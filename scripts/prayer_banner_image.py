from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old='</svg></div></div>\n <div class="pb-sub">'
new='</svg></div><img class="prayer-mosque-art" src="/assets/prayer-mosque.png" alt="المسجد"></div>\n <div class="pb-sub">'
if old not in s: raise SystemExit('prayer banner boundary not found')
s=s.replace(old,new,1)
css='''.prayer-mosque-art{position:absolute;left:50%;bottom:3px;z-index:1;width:116px;height:108px;transform:translateX(-50%);object-fit:contain;opacity:.72;filter:drop-shadow(0 3px 8px rgba(0,0,0,.35));pointer-events:none}.prayer-banner .pb-count,.prayer-banner .pb-loc,.prayer-banner .pb-badge{z-index:2}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('prayer banner image applied')
