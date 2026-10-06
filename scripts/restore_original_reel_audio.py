from pathlib import Path
import re, shutil
root=Path('/home/ubuntu/work/yawaqit_extract')
orig=Path('/tmp/yawaqit-original-full')
cur=(root/'index.html').read_text()
old=(orig/'index.html').read_text()
# Restore the original source media exactly; the original project used these with autoplay audio.
for src in (orig/'public/assets/transfer').glob('*.mp4'):
    shutil.copy2(src, root/'public/assets/transfer'/src.name)
# Restore the original transfer card: autoplay, no forced mute, no extra sound-button layer.
def fn(src,name):
    m=re.search(r'function '+name+r'\(.*?(?=\n(?:function|const) )',src,re.S)
    if not m: raise SystemExit(name+' not found')
    return m.group(0)
orig_card=fn(old,'transferCard')
cur_card=fn(cur,'transferCard')
cur=cur.replace(cur_card,orig_card,1)
# Restore the original render-time audio behavior and observer, which starts the active reel with audio.
start="const adVideo=sc.querySelector('.reel-ad-video');"
end="\n  buildNav();moveDot(anim);bind(k);"
a=cur.find(start); b=cur.find(end,a)
if a<0 or b<0: raise SystemExit('current media block not found')
orig_a=old.find(start); orig_b=old.find(end,orig_a)
if orig_a<0 or orig_b<0: raise SystemExit('original media block not found')
cur=cur[:a]+old[orig_a:orig_b]+cur[b:]
# Remove the added sound-button delegated handler; the old system has no second audio layer.
cur=re.sub(r"A\('\[data-reel-sound\]',e=>\{.*?\}\);",'',cur,count=1)
# Keep interface click sounds away from video pointer taps so they cannot create audible crackle/overlap.
cur=cur.replace("document.addEventListener('pointerdown',e=>{if(e.target.closest('[data-reel-sound],.reels-feed video'))return;if(e.target.closest('button'))soundTap(classifyTap(e.target))},{passive:true});", "document.addEventListener('pointerdown',e=>{if(e.target.closest('.reels-feed video'))return;if(e.target.closest('button'))soundTap(classifyTap(e.target))},{passive:true});",1)
# Remove the visual sound buttons left in any already-modified markup if the replacement did not catch it.
cur=cur.replace('<button data-reel-sound="${i}" aria-label="صوت الفيديو">🔊</button>','')
(root/'index.html').write_text(cur)
print('restored original reel files and autoplay audio system')
