from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old='<div id="loadingScreen" role="status" aria-live="polite"><div class="loading-inner"><img class="loading-mosque" src="/assets/loading-mosque.png" alt=""><div class="loading-copy">جاري التحميل</div>'
new='<div id="loadingScreen" role="status" aria-live="polite"><div class="loading-inner"><img class="loading-brand-logo" src="/assets/logo.png" alt="شعار يواقيت"><div class="loading-brand-name">يَوَاقِيت</div><img class="loading-mosque" src="/assets/loading-mosque.png" alt=""><div class="loading-copy">جاري التحميل</div>'
if old not in s: raise SystemExit('loading markup marker not found')
s=s.replace(old,new,1)
css='''.loading-brand-logo{width:54px;height:54px;object-fit:contain;margin-bottom:4px}.loading-brand-name{font-family:'Noto Kufi Arabic',system-ui,sans-serif;font-size:18px;font-weight:700;letter-spacing:.04em;color:#08080a;margin-bottom:8px}.loading-orbit i:nth-child(n){background:#08080a!important;box-shadow:0 0 8px rgba(0,0,0,.2)!important}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('loader branding and black dots applied')
