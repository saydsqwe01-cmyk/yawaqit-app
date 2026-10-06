from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
a=s.find("A('[data-reel-like]'")
b=s.find("A('[data-x]'",a)
if a<0 or b<0: raise SystemExit('reel bindings not found')
fixed="A('[data-reel-like]',e=>{const i=e.dataset.reelLike;S.reelLikes[i]=!S.reelLikes[i];e.classList.toggle('active',!!S.reelLikes[i]);e.setAttribute('aria-pressed',String(!!S.reelLikes[i]));localStorage.setItem('yawaqit-reel-likes',JSON.stringify(S.reelLikes))});A('[data-reel-repost]',e=>{const i=e.dataset.reelRepost;S.reelReposts[i]=!S.reelReposts[i];e.classList.toggle('active',!!S.reelReposts[i]);e.setAttribute('aria-pressed',String(!!S.reelReposts[i]));localStorage.setItem('yawaqit-reel-reposts',JSON.stringify(S.reelReposts))});"
s=s[:a]+fixed+s[b:]
p.write_text(s)
print('reel bindings repaired')
