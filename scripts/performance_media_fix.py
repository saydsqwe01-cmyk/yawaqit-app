from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Show the video notice immediately instead of waiting for all APIs/data to finish.
s=s.replace("reelPrompt:false,reelIndex:0", "reelPrompt:true,reelIndex:0")
# Avoid downloading all local reels at first paint; the observer loads only the visible one.
s=s.replace("<video class=\"transfer-video\" autoplay loop preload=\"metadata\" playsinline", "<video class=\"transfer-video\" autoplay loop muted preload=\"none\" playsinline")
s=s.replace("<video class=\"reel-ad-video\" autoplay controls playsinline volume=\"1\"", "<video class=\"reel-ad-video\" autoplay controls muted playsinline volume=\"1\"")
# Use lazy image elements instead of 30 eager YouTube thumbnail background requests.
s=s.replace("<div class=\"thumb th\" style=\"background-image:url('https://i.ytimg.com/vi/${x[3]}/mqdefault.jpg');background-size:cover\"></div>", "<div class=\"thumb th\"><img class=\"yt-thumb\" loading=\"lazy\" decoding=\"async\" src=\"https://i.ytimg.com/vi/${x[3]}/mqdefault.jpg\" alt=\"\"></div>")
# Lazy-load generated page images/iframes centrally after each render, without changing layout.
needle="sc.innerHTML=scr[k]();"
replacement=needle+"sc.querySelectorAll('img').forEach((img,i)=>{if(!img.loading)img.loading=i<2?'eager':'lazy';img.decoding='async'});sc.querySelectorAll('iframe').forEach(f=>{if(!f.loading)f.loading='lazy'});"
s=s.replace(needle,replacement,1)
# Keep thumbnails visually identical to the previous background treatment.
s=s.replace(".ytframe{width:100%;height:100%;border:0", ".yt-thumb{display:block;width:100%;height:100%;object-fit:cover;border-radius:6px;background:#111}.ytframe{width:100%;height:100%;border:0")
# Prevent the post-render video pass from trying to start every media element.
s=s.replace("v.volume=1;v.muted=false;if(!v.closest('.reels-feed'))v.play().catch(()=>{});", "v.volume=1;if(!v.closest('.reels-feed')){v.muted=false}")
p.write_text(s)
print('performance/media fixes applied')
