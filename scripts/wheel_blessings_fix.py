from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
start=s.index('const GLAD_TIDINGS=')
end=s.index('\nfunction dayIndex', start)
block="""const GLAD_TIDINGS=[
 ['آية تبشّر بالفرج','فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ إِنَّ مَعَ الْعُسْرِ يُسْرًا','سورة الشرح: 5-6'],
 ['آية تبشّر بالرزق','وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا ۝ وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ','سورة الطلاق: 2-3'],
 ['آية تبشّر برحمة الله','قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَى أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ','سورة الزمر: 53'],
 ['آية تبشّر للصابرين','وَبَشِّرِ الصَّابِرِينَ ۝ الَّذِينَ إِذَا أَصَابَتْهُم مُّصِيبَةٌ قَالُوا إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ','سورة البقرة: 155-156'],
 ['حديث يبشّر بالخير','مَن يُرِدِ اللَّهُ به خَيْرًا يُفَقِّهْهُ في الدِّينِ','صحيح البخاري وصحيح مسلم'],
 ['حديث يبشّر بالأجر','مَن سَلَكَ طَرِيقًا يَلْتَمِسُ فيه عِلْمًا سَهَّلَ اللَّهُ له به طَرِيقًا إلى الجَنَّةِ','صحيح مسلم'],
 ['حديث يبعث على التفاؤل','عَجَبًا لأمْرِ المُؤْمِنِ، إنَّ أمْرَه كُلَّهُ خَيْرٌ','صحيح مسلم'],
 ['حديث في فضل الذكر','مَن قالَ: سُبْحانَ اللَّهِ وبِحَمْدِهِ، في يَومٍ مِئَةَ مَرَّةٍ، حُطَّتْ خَطاياهُ','صحيح البخاري وصحيح مسلم']
];"""
s=s[:start]+block+s[end:]
s=s.replace("giftClicks:0,giftOpened:false,wheelBlessing:null", "giftClicks:0,giftOpened:false,wheelBlessing:null,wheelReady:false")
# Replace the wheel page with a centered animated gift modal after the spin completes.
pat=r"function wheelPage\(\)\{.*?\};\nfunction reelPrompt"
new="""function wheelPage(){const g=S.wheelBlessing||dailyGlad();const modal=S.wheelReady?`<div class=\"wheel-gift-overlay\" role=\"dialog\" aria-label=\"${g[0]}\"><div class=\"wheel-gift-modal\"><button class=\"wheel-gift-close\" id=\"closeWheelGift\" aria-label=\"إغلاق\">×</button>${S.giftOpened?`<div class=\"wheel-blessing-result\"><div class=\"paper-seal\">✦</div><b>${g[0]}</b><div>${g[1]}</div><small>${g[2]}</small></div>`:`<div class=\"wheel-gift-title\">✦ افتح صندوق البشارة ✦</div><button id=\"giftBox\" class=\"gift-box\" aria-label=\"افتح صندوق البشارة\"><span class=\"gift-paper\">بشارة</span><span class=\"gift-lid\"></span><span class=\"gift-body\"><i></i></span><span class=\"gift-bow\">✦</span></button><div class=\"gift-hint\">اضغط على الصندوق لفتح البشارة</div>`}</div></div>`:'';return `<div class=\"card hd\"><div class=\"row\" style=\"direction:rtl;justify-content:space-between\"><b style=\"font-size:16px\">${U('wheel')}</b><button id=\"bk\" class=\"ib\">${I('back')}</button></div><p class=\"mut\" style=\"text-align:center\">${U('wheelDesc')}</p></div><div class=\"card wheel-wrap\"><div class=\"wheel\" id=\"wheel\"><span>${U('remember')}</span></div><button class=\"btn\" id=\"spinWheel\" ${S.wheelSpinning?'disabled':''}>${S.wheelSpinning?'جاري الدوران…':U('spin')}</button></div>${modal}`};
function reelPrompt"""
s2,n=re.subn(pat,new,s,flags=re.S)
if n!=1: raise SystemExit(f'wheelPage replacement count {n}')
s=s2
# Replace the old 3-click gift handler with one-click opening and overlay close.
old="A('#giftBox',()=>{S.giftClicks=(S.giftClicks||0)+1;const box=$('#giftBox');if(S.giftClicks<3){playEffect('click');box?.classList.remove('bump');void box?.offsetWidth;box?.classList.add('bump');return}S.giftOpened=true;render();requestAnimationFrame(()=>playEffect('giftOpen'))});A('#closeBlessing',()=>{S.giftOpened=false;render(true)});"
newh="A('#giftBox',()=>{S.giftOpened=true;render();requestAnimationFrame(()=>playEffect('giftOpen'))});A('#closeWheelGift',()=>{S.wheelReady=false;S.giftOpened=false;render(true)});"
if old not in s: raise SystemExit('gift handler pattern not found')
s=s.replace(old,newh)
# Make the wheel rotate for exactly three seconds and reveal the modal afterwards.
oldspin="A('#spinWheel',()=>{S.wheelBlessing=GLAD_TIDINGS[Math.floor(Math.random()*GLAD_TIDINGS.length)];S.giftClicks=0;S.giftOpened=false;playEffect('click');render(true);setTimeout(()=>{const w=$('#wheel');if(w){w.style.transition='transform 4.8s cubic-bezier(.12,.78,.18,1)';w.style.transform=`rotate(${1440+Math.random()*1080}deg)`}},30)});"
newspin="A('#spinWheel',()=>{if(S.wheelSpinning)return;S.wheelBlessing=GLAD_TIDINGS[Math.floor(Math.random()*GLAD_TIDINGS.length)];S.giftClicks=0;S.giftOpened=false;S.wheelReady=false;S.wheelSpinning=true;playEffect('click');render(true);setTimeout(()=>{const w=$('#wheel');if(w){w.style.transition='transform 3s cubic-bezier(.12,.78,.18,1)';w.style.transform=`rotate(${1440+Math.random()*1080}deg)`}},30);setTimeout(()=>{S.wheelSpinning=false;S.wheelReady=true;render(true)},3050)});"
if oldspin not in s: raise SystemExit('spin handler pattern not found')
s=s.replace(oldspin,newspin)
# Add overlay animation styles.
css="""
.wheel-gift-overlay{position:fixed;inset:0;z-index:360;display:grid;place-items:center;padding:18px;background:rgba(8,16,24,.42);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);animation:wheelOverlayIn .45s ease-out}.wheel-gift-modal{position:relative;width:min(88vw,390px);min-height:270px;padding:34px 22px 22px;border:1px solid #d6a83b;border-radius:18px;background:linear-gradient(145deg,rgba(255,255,255,.96),rgba(247,223,160,.96));box-shadow:0 22px 60px rgba(0,0,0,.45);display:grid;place-items:center;text-align:center;color:#5f4315;animation:wheelGiftIn .7s cubic-bezier(.18,.9,.22,1)}.wheel-gift-title{font-size:15px;font-weight:700;color:#8b5d16;margin-bottom:4px}.wheel-gift-close{position:absolute;top:9px;right:11px;width:28px;height:28px;border:0;background:transparent;color:#79521c;font-size:22px;cursor:pointer}.wheel-gift-modal .gift-box{margin:2px auto 0;animation:giftFloat 1.8s ease-in-out infinite}.wheel-blessing-result{position:relative;width:100%;padding:30px 8px 4px;animation:wheelResultIn .8s cubic-bezier(.18,.9,.22,1)}.wheel-blessing-result>b{display:block;color:#8b5d16;font-size:17px;margin-bottom:14px}.wheel-blessing-result>div:not(.paper-seal){font-size:19px;line-height:2;font-weight:700}.wheel-blessing-result>small{display:block;margin-top:14px;color:#8d6d37;font-size:11px}.wheel-blessing-result .paper-seal{top:-10px}.wheel-gift-modal .gift-hint{color:#8d6d37}@keyframes wheelOverlayIn{from{opacity:0}to{opacity:1}}@keyframes wheelGiftIn{from{opacity:0;transform:translateY(35px) scale(.82)}to{opacity:1;transform:none}}@keyframes wheelResultIn{from{opacity:0;transform:scale(.75) rotate(-3deg)}60%{transform:scale(1.05) rotate(1deg)}to{opacity:1;transform:none}}@keyframes giftFloat{50%{transform:translateY(-8px) rotate(-2deg)}}
"""
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('wheel blessings and animation fixes applied')
