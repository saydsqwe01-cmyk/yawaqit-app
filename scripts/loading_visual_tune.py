from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

root=Path('/home/ubuntu/work/yawaqit_extract')
src=root/'public/assets/loading-mosque.jpg'
out=root/'public/assets/loading-mosque.png'
im=Image.open(src).convert('RGBA')
w,h=im.size
# A soft cutout around the central minaret, excluding the sky, birds and white page background.
pts=[(w*.47,h*.07),(w*.54,h*.07),(w*.55,h*.14),(w*.59,h*.20),(w*.59,h*.30),(w*.57,h*.38),(w*.62,h*.43),(w*.64,h*.57),(w*.69,h*.68),(w*.75,h*.86),(w*.85,h*.98),(w*.18,h*.98),(w*.28,h*.86),(w*.32,h*.68),(w*.36,h*.57),(w*.38,h*.43),(w*.43,h*.38),(w*.41,h*.30),(w*.41,h*.20),(w*.45,h*.14)]
mask=Image.new('L',(w,h),0)
ImageDraw.Draw(mask).polygon([(int(x),int(y)) for x,y in pts],fill=255)
# Soften only the cutout edge so it blends naturally on the white loader.
mask=mask.filter(ImageFilter.GaussianBlur(3.0))
im.putalpha(mask)
im.save(out,optimize=True)

p=root/'index.html'
s=p.read_text()
s=s.replace('src="/assets/loading-mosque.jpg"','src="/assets/loading-mosque.png"',1)
# Eight orbiting dots instead of three; the circle itself remains transparent.
s=s.replace('<i></i><i></i><i></i></div></div></div>','<i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div></div>',1)
s=s.replace('animation:loadingOrbit 1.25s linear infinite','animation:loadingOrbit 2.1s linear infinite',1)
s=s.replace('.loading-orbit i:nth-child(2){animation-delay:-.42s;background:#6c63d9}.loading-orbit i:nth-child(3){animation-delay:-.84s;background:#f6b93b}', '.loading-orbit i:nth-child(2){animation-delay:-.2625s;background:#6c63d9}.loading-orbit i:nth-child(3){animation-delay:-.525s;background:#f6b93b}.loading-orbit i:nth-child(4){animation-delay:-.7875s;background:#2fb5a5}.loading-orbit i:nth-child(5){animation-delay:-1.05s;background:#ef6f91}.loading-orbit i:nth-child(6){animation-delay:-1.3125s;background:#8d72d8}.loading-orbit i:nth-child(7){animation-delay:-1.575s;background:#55a6d9}.loading-orbit i:nth-child(8){animation-delay:-1.8375s;background:#e8a83e}')
# Keep the loader visible briefly even if cached data returns immediately.
s=s.replace("function finishInitialLoading(){const el=document.querySelector('#loadingScreen');if(!el)return;el.classList.add('loaded');setTimeout(()=>el.remove(),650)}", "const loadingStartedAt=performance.now();function finishInitialLoading(){const el=document.querySelector('#loadingScreen');if(!el)return;const wait=Math.max(0,1100-(performance.now()-loadingStartedAt));setTimeout(()=>{el.classList.add('loaded');setTimeout(()=>el.remove(),650)},wait)}")
p.write_text(s)
print(f'created {out} ({out.stat().st_size} bytes) and tuned loader')
