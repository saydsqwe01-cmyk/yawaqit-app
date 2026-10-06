from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
css=r'''
/* شاشة التحميل الأولى */
#loadingScreen{position:fixed;inset:0;z-index:9999;display:grid;place-items:center;background:#fff;color:#27323b;opacity:1;visibility:visible;transition:opacity .45s ease,visibility .45s ease}#loadingScreen.loaded{opacity:0;visibility:hidden;pointer-events:none}.loading-inner{width:min(92vw,520px);height:min(92dvh,760px);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.loading-mosque{display:block;width:min(72vw,360px);height:min(60dvh,540px);object-fit:cover;object-position:center;border-radius:28px;filter:saturate(.82) brightness(1.04);mask-image:linear-gradient(to bottom,#000 0%,#000 78%,transparent 100%);-webkit-mask-image:linear-gradient(to bottom,#000 0%,#000 78%,transparent 100%)}.loading-copy{margin-top:-34px;font-family:'Noto Kufi Arabic',system-ui,sans-serif;font-size:14px;font-weight:600;color:#27323b}.loading-orbit{position:relative;width:58px;height:58px;margin-top:13px;border:2px solid transparent;border-radius:50%}.loading-orbit i{position:absolute;left:calc(50% - 4px);top:-5px;width:8px;height:8px;border-radius:50%;background:#0b86c9;box-shadow:0 0 10px rgba(11,134,201,.28);transform-origin:4px 33px;animation:loadingOrbit 1.25s linear infinite}.loading-orbit i:nth-child(2){animation-delay:-.42s;background:#6c63d9}.loading-orbit i:nth-child(3){animation-delay:-.84s;background:#f6b93b}@keyframes loadingOrbit{to{transform:rotate(360deg)}}
'''
s=s.replace('</style>',css+'</style>',1)
old='<body>\n<div id="app">'
new='<body>\n<div id="loadingScreen" role="status" aria-live="polite"><div class="loading-inner"><img class="loading-mosque" src="/assets/loading-mosque.jpg" alt=""><div class="loading-copy">جاري التحميل</div><div class="loading-orbit" aria-hidden="true"><i></i><i></i><i></i></div></div></div>\n<div id="app">'
if old not in s: raise SystemExit('body marker not found')
s=s.replace(old,new,1)
# Add a safe hide helper before data loading starts.
marker='async function loadCollectedData(){'
helper="function finishInitialLoading(){const el=document.querySelector('#loadingScreen');if(!el)return;el.classList.add('loaded');setTimeout(()=>el.remove(),650)}\n"
if marker not in s: raise SystemExit('loadCollectedData marker not found')
s=s.replace(marker,helper+marker,1)
# Hide after both successful and failed initial data loading, without leaving the overlay stuck offline.
s=s.replace("render(true);\n  }catch(e){console.warn('Yawaqit data load failed',e)}\n}", "render(true);\n    finishInitialLoading();\n  }catch(e){console.warn('Yawaqit data load failed',e);finishInitialLoading()}\n}",1)
p.write_text(s)
print('loading screen applied')
