from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
old="<div class=\"gift-hint\">اضغط على الصندوق لفتح البشارة</div>`}</div></div>`:'';return"
new="<div class=\"gift-hint\">اضغط على الصندوق 3 مرات لفتح البشارة</div><div class=\"gift-progress\" id=\"giftProgress\">0 / 3</div>`}</div></div>`:'';return"
if old not in s: raise SystemExit('gift hint markup not found')
s=s.replace(old,new,1)
oldh="A('#giftBox',()=>{S.giftOpened=true;render();requestAnimationFrame(()=>playEffect('giftOpen'))});"
newh="A('#giftBox',()=>{S.giftClicks=(S.giftClicks||0)+1;const box=$('#giftBox');if(S.giftClicks<3){playEffect('click');box?.classList.remove('bump');void box?.offsetWidth;box?.classList.add('bump');const p=$('#giftProgress');if(p)p.textContent=`${S.giftClicks} / 3`;return}S.giftOpened=true;render();requestAnimationFrame(()=>playEffect('giftOpen'))});"
if oldh not in s: raise SystemExit('gift handler not found')
s=s.replace(oldh,newh,1)
css=r'''
/* عجلة البشارة: واجهة زجاجية متوافقة مع الوضعين */
.wheel-gift-overlay{background:rgba(8,18,30,.24)!important;backdrop-filter:blur(16px) saturate(125%)!important;-webkit-backdrop-filter:blur(16px) saturate(125%)!important}.wheel-gift-modal{background:rgba(255,255,255,.18)!important;border:1px solid rgba(255,255,255,.52)!important;border-radius:24px!important;box-shadow:0 24px 70px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.55)!important;backdrop-filter:blur(22px) saturate(140%)!important;-webkit-backdrop-filter:blur(22px) saturate(140%)!important;color:var(--ink)!important}.wheel-gift-title{color:var(--ink)!important;text-shadow:0 1px 8px rgba(255,255,255,.28)}.wheel-gift-modal .gift-box .gift-body{background:linear-gradient(135deg,#147dc1,#2756a5)!important;border-color:rgba(255,255,255,.7)!important;box-shadow:inset 20px 0 0 rgba(255,255,255,.12),0 10px 25px rgba(20,125,193,.28)!important}.wheel-gift-modal .gift-box .gift-body:after{background:rgba(255,255,255,.72)!important;border:0!important;width:18px!important}.wheel-gift-modal .gift-box .gift-lid{background:linear-gradient(135deg,#2a9bd2,#354eb5)!important;border-color:rgba(255,255,255,.7)!important;box-shadow:inset 20px 0 0 rgba(255,255,255,.12)!important}.wheel-gift-modal .gift-box .gift-lid:after{background:rgba(255,255,255,.72)!important;border:0!important;width:18px!important}.wheel-gift-modal .gift-bow{color:#fff!important;text-shadow:0 2px 8px rgba(20,125,193,.55)!important}.wheel-gift-modal .gift-paper{background:rgba(255,255,255,.42)!important;border:1px solid rgba(255,255,255,.7)!important;box-shadow:0 8px 20px rgba(0,0,0,.18)!important;color:var(--ink)!important}.wheel-gift-modal .gift-hint,.wheel-gift-modal .gift-progress{color:var(--mut)!important}.wheel-blessing-result{color:var(--ink)!important;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.38);border-radius:18px;padding:42px 18px 20px!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.35)}.wheel-blessing-result>b{color:var(--blue)!important}.wheel-blessing-result>div:not(.paper-seal){color:var(--ink)!important}.wheel-blessing-result>small{color:var(--mut)!important}.wheel-blessing-result .paper-seal{background:var(--blue)!important;border-color:rgba(255,255,255,.75)!important;color:#fff!important;box-shadow:0 5px 16px rgba(20,125,193,.32)!important}
body.light .wheel-gift-modal{background:rgba(255,255,255,.58)!important;border-color:rgba(255,255,255,.9)!important}body:not(.light) .wheel-gift-modal{background:rgba(20,34,46,.58)!important;border-color:rgba(145,200,225,.42)!important}.wheel-gift-modal .gift-box{filter:drop-shadow(0 12px 14px rgba(20,125,193,.22))}
'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('three-tap glass wheel applied')
