from pathlib import Path
import re

p = Path('/home/ubuntu/yawaqit/index.html')
s = p.read_text(encoding='utf-8')

# Reduce visual gaps while keeping the supplied card language and dimensions.
s = s.replace('margin-bottom:12px}', 'margin-bottom:6px}', 1)
s = s.replace('.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}', '.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}', 1)
s = s.replace('margin-bottom:9px;border:1.5px', 'margin-bottom:5px;border:1.5px', 1)
s = s.replace('margin-bottom:10px;font-size:12px', 'margin-bottom:4px;font-size:12px', 1)
s = s.replace('</style>', '''
/* time-of-day atmosphere: the original phone canvas remains unchanged */
body{transition:background 2.5s ease;color:#fff}
body.sunset{background:linear-gradient(180deg,#643527,#232323)}
body.dawn{background:linear-gradient(180deg,#31465b,#232323)}
body.night{background:linear-gradient(180deg,#101823,#232323)}
body.sunset #app:before,body.dawn #app:before{content:"";position:absolute;inset:72px 0 66px;pointer-events:none;opacity:.22;transition:opacity 2.5s;background:radial-gradient(circle at 50% 15%,#f6b93b 0,transparent 38%)}
body.night #app:before{content:"";position:absolute;inset:72px 0 66px;pointer-events:none;opacity:.16;background:radial-gradient(circle at 72% 12%,#4fb3ec 0,transparent 28%)}
#app>*{position:relative;z-index:1}
#loc{display:block;margin:6px auto 0;color:#4fb3ec;font-size:9px}
#detSearch{margin-top:8px}
.ytimg{width:100%;height:100%;object-fit:cover;border-radius:10px}
.audio-error{color:#e74c3c;font-size:9px;text-align:center;margin-top:7px}
'''+ '</style>', 1)

s = s.replace('const S={fs:17,rc:0,tab:\'home\',sub:null,vid:1,playing:true,t:5,spd:0,tr:true,tf:true,surah:0,star:{},mark:{},vp:-1,all:false,trOpen:true,tfx:{},az:[0,0,0,0],qz:null};', "const S={fs:17,rc:0,tab:'home',sub:null,vid:0,playing:true,t:5,spd:0,tr:true,tf:true,surah:0,star:{},mark:{},vp:-1,all:false,trOpen:true,tfx:{},az:[0,0,0,0],qz:null,detQ:'',geoReady:false,audioMsg:''};")
s = s.replace('const VID=', 'let VID=', 1)
s = s.replace('const PR=', 'let PR=', 1)

# Add connected behavior immediately before the existing prayers helper.
anchor = "const p2=n=>String(n).padStart(2,'0');"
integration = r'''
let VIDEO_DATA=[];
let HADITH_API_READY=false;
let HADITH_API_LOADING=false;
let NAMES_API_READY=false;
let soundContext=null;
function soundTap(){try{soundContext=soundContext||new (window.AudioContext||window.webkitAudioContext)();const o=soundContext.createOscillator(),g=soundContext.createGain();o.frequency.value=520;g.gain.setValueAtTime(.035,soundContext.currentTime);g.gain.exponentialRampToValueAtTime(.001,soundContext.currentTime+.06);o.connect(g).connect(soundContext.destination);o.start();o.stop(soundContext.currentTime+.06)}catch(e){}}
function updateTimeTheme(){const h=new Date().getHours()+new Date().getMinutes()/60;document.body.classList.remove('sunset','dawn','night');if(h>=16&&h<19)document.body.classList.add('sunset');else if(h>=5&&h<7)document.body.classList.add('dawn');else if(h>=19||h<5)document.body.classList.add('night')}
function loadLocationPrayer(){if(!navigator.geolocation)return;navigator.geolocation.getCurrentPosition(async pos=>{try{const {latitude,longitude}=pos.coords;const d=await fetch(`https://api.aladhan.com/v1/timings?latitude=${latitude}&longitude=${longitude}&method=4`).then(x=>x.json());const t=d.data&&d.data.timings;const clean=x=>String(x||'').split(' ')[0].split(':').map(Number);if(t){PR=[['الفجر',...clean(t.Fajr)],['الظهر',...clean(t.Dhuhr)],['العصر',...clean(t.Asr)],['المغرب',...clean(t.Maghrib)],['العشاء',...clean(t.Isha)]];S.geoReady=true;render()}}catch(e){}},()=>{}, {enableHighAccuracy:true,timeout:12000,maximumAge:600000})}
async function loadNamesApi(){if(NAMES_API_READY)return;try{let d=await fetch('https://api.aladhan.com/v1/asmaAlHusna').then(x=>x.json());let rows=d.data||[];if(!rows.length)throw Error('empty');DET[5]=rows.map(x=>[x.name,`${x.transliteration||''}${x.en&&x.en.meaning?' · '+x.en.meaning:''}`]);NAMES_API_READY=true;render()}catch(e){try{const d=await fetch('/data/asma_fallback.json').then(x=>x.json());DET[5]=(d.data||[]).map(x=>[x.name,`${x.transliteration||''}${x.en&&x.en.meaning?' · '+x.en.meaning:''}`]);NAMES_API_READY=true;render()}catch(_){}}}
async function ensureHadithApi(){if(HADITH_API_READY||HADITH_API_LOADING)return;HADITH_API_LOADING=true;render();try{const d=await fetch('https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-bukhari.json').then(x=>x.json());const rows=d.hadiths||[];if(rows.length)DET[0]=rows.map(x=>[x.text||x.hadithArabic||x.hadith||'', 'صحيح البخاري']);HADITH_API_READY=true}catch(e){}HADITH_API_LOADING=false;render()}
function swipeTabs(){let x=0;const el=$('#scr');el.addEventListener('touchstart',e=>{x=e.changedTouches[0].clientX},{passive:true});el.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-x;if(Math.abs(dx)<70)return;const i=tabs.findIndex(t=>t[0]===S.tab);const ni=Math.max(0,Math.min(tabs.length-1,i+(dx<0?1:-1)));if(ni!==i)go(tabs[ni][0])},{passive:true})}
'''
if anchor not in s:
    raise SystemExit('missing integration anchor')
s = s.replace(anchor, integration+'\n'+anchor, 1)

# Make data loading include the local video snapshot and populate every snippet category.
s = s.replace("const [q,r,a,h]=await Promise.all([", "const [q,r,a,h,videos]=await Promise.all([", 1)
s = s.replace("fetch('/data/hadith/featured.json').then(x=>x.json())\n    ]);", "fetch('/data/hadith/featured.json').then(x=>x.json()),\n      fetch('/data/videos.json').then(x=>x.json())\n    ]);", 1)
s = s.replace("HADITH_PREVIEW=h.hadiths||[];", "HADITH_PREVIEW=h.hadiths||[];VIDEO_DATA=videos.items||[];VID=VIDEO_DATA.map(x=>[x.title,x.description,0,x.id,x.channel]);", 1)
s = s.replace("DET[1]=ADHKAR_DOORS.slice(0,1).flatMap(d=>(d.items||[]).slice(0,4).map(x=>[x.text,'حصن المسلم']));", "DET[1]=ADHKAR_DOORS.slice(0,1).flatMap(d=>(d.items||[]).slice(0,4).map(x=>[x.text,'حصن المسلم']));\n    DET[2]=[['طلب العلم فريضة','الموسوعة التاريخية'],['الهجرة النبوية','محطات من السيرة'],['فتح مكة','من التاريخ الإسلامي']];\n    DET[3]=[['علامات الساعة الصغرى','التذكير بالآخرة والعمل الصالح'],['التوبة باب مفتوح','لا يقنط المؤمن من رحمة الله']];\n    DET[4]=[['الفاتحة والمعوذات','رقية شرعية ثابتة من القرآن'],['أعوذ بكلمات الله التامات','من أذكار الرقية']];\n    DET[6]=[['فضل الصلاة على وقتها','أحب الأعمال إلى الله الصلاة على وقتها'],['فضل الصدقة','الصدقة برهان']];\n    DET[8]=[['خديجة رضي الله عنها','أم المؤمنين وأول من آمن بالنبي ﷺ'],['مريم عليها السلام','سيدة نساء العالمين']];\n    DET[10]=[['أفلا يتدبرون القرآن','القرآن كتاب هداية وتدبر'],['وفي أنفسكم أفلا تبصرون','آيات الله في خلقه']];", 1)
s = s.replace("S.tr=false;S.tf=false;", "S.tr=false;S.tf=false;updateTimeTheme();loadLocationPrayer();loadNamesApi();", 1)

# The home card keeps the original position but now requests precise location explicitly.
s = s.replace('المواقيت تقريبية</small></div>', "${S.geoReady?'مواقيت دقيقة بحسب موقعك':'المواقيت تقريبية'}<button id=\"loc\">تحديد موقعي بدقة</button></small></div>", 1)

# Replace the original video screen with the same layout fed by real YouTube records.
new_vid = r'''vid(){const v=VID[S.vid]||['فيديو إسلامي','من قناة موثوقة',0,'',''];const id=v[3]||'';return `<div class="card player"><div class="thumb pv" id="pp">${id?`<img class="ytimg" src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="${v[0].replace(/"/g,'')}"/>`:I(S.playing?'pause':'play')}</div><div class="ctl"><span>${fmt(S.t)}</span><input type="range" id="sk" min="0" max="1" value="0"><span>يوتيوب</span><button id="sp" style="display:flex;align-items:center;gap:2px">${I('spd','width:20px;height:20px')}<small>${SPD[S.spd]}x</small></button></div></div><div class="card"><div style="font-size:13px;margin-bottom:6px">${v[0]}</div><div class="mut" style="font-size:10px">${v[1]} · ${v[4]||'قناة إسلامية'}</div></div><div class="sec">فيديوهات وخطب ورسائل يومية</div>${VID.map((x,i)=>`<button class="vi ${i===S.vid?'sel':''}" data-v="${i}"><div class="thumb th" style="background-image:url('https://i.ytimg.com/vi/${x[3]}/mqdefault.jpg');background-size:cover"></div><div class="tx"><b>${x[0]}</b><small>${x[1]}</small></div>${i===S.vid?`<div class="ck">${I('check')}</div>`:'<div class="ph"></div>'}</button>`).join('')}`},
 quran()'''
s = re.sub(r"vid\(\)\{.*?\},\n quran\(\)", new_vid, s, count=1, flags=re.S)

# Replace the detail screen with searchable populated content.
new_det = r'''det(){const n=S.sub,d=DET[n]||[],q=S.detQ||'';const rows=d.filter(x=>String(x[0]).includes(q)||String(x[1]).includes(q));const shown=n===0&&!q?rows.slice(0,40):rows.slice(0,100);const search=(n===0||n===5)?`<input id="detSearch" class="srch" placeholder="ابحث داخل المحتوى" value="${q.replace(/"/g,'&quot;')}">`:'';const list=n===1?AZK.map((a,i)=>`<button class="cn" data-z="${i}"><span>${ar(S.az[i]||0)}</span><div style="flex:1">${a}</div></button>`).join(''):shown.map(x=>`<div class="card" style="text-align:center;border-radius:20px"><div class="verse">${x[0]}</div><div class="ref">${x[1]}</div></div>`).join('');return `<div class="card hd"><div class="row" style="direction:rtl;justify-content:space-between"><b style="font-size:16px">${SNIP[n][0]}</b><button id="bk" class="ib">${I('back')}</button></div>${search}</div>${HADITH_API_LOADING&&n===0?`<div class="card mut" style="text-align:center;padding:20px">جارٍ تحميل الأحاديث عبر API...</div>`:''}${list||`<div class="card mut" style="text-align:center;font-size:12px;padding:30px">المحتوى قيد الإعداد</div>`}`},
 aud()'''
s = re.sub(r"det\(\)\{.*?\},\n aud\(\)", new_det, s, count=1, flags=re.S)

# Wire search, location, API-backed categories, real YouTube opening, and robust audio state.
s = s.replace("A('[data-n]',e=>{const n=+e.dataset.n;if(n===12)S.qz={i:0,ans:0,ok:0,pick:null};else S.sub=n;render(true)});", "A('[data-n]',e=>{const n=+e.dataset.n;if(n===12)S.qz={i:0,ans:0,ok:0,pick:null};else{S.detQ='';S.sub=n;if(n===0)ensureHadithApi();if(n===5)loadNamesApi();}render(true)});")
s = s.replace("A('[data-v]',e=>{S.vid=+e.dataset.v;S.t=0;S.playing=true;render()});", "A('[data-v]',e=>{S.vid=+e.dataset.v;S.t=0;S.playing=true;render()});")
s = s.replace("A('#pp',()=>{S.playing=!S.playing;render()});", "A('#pp',()=>{const v=VID[S.vid];if(v&&v[3])window.open('https://www.youtube.com/watch?v='+v[3],'_blank','noopener');else{S.playing=!S.playing;render()}});")
s = s.replace("A('#sp',()=>{S.spd=(S.spd+1)%4;render()});", "A('#sp',()=>{S.spd=(S.spd+1)%4;if(audioEl)audioEl.playbackRate=SPD[S.spd];render()});")
s = s.replace("A('[data-x]',e=>{S.tfx[e.dataset.x]=!S.tfx[e.dataset.x];render()});", "A('[data-x]',e=>{S.tfx[e.dataset.x]=!S.tfx[e.dataset.x];render()});\n  A('#detSearch',e=>{e.oninput=ev=>{S.detQ=ev.target.value;render()}});\n  A('#loc',()=>loadLocationPrayer());")
s = s.replace("A('[data-a]',e=>{const i=+e.dataset.a;if(S.ap===i){stopAudio();render()}else playRecitation(i)});", "A('[data-a]',e=>{const i=+e.dataset.a;if(S.ap===i){stopAudio();render()}else playRecitation(i)});")
s = s.replace("function stopAudio(){audioEl.pause();audioEl.currentTime=0;S.ap=null;S.all=false;S.vp=-1}", "function stopAudio(){audioEl.pause();audioEl.currentTime=0;audioEl.removeAttribute('src');audioEl.load();S.ap=null;S.all=false;S.vp=-1;S.audioMsg=''}")
s = s.replace("audioEl.onended=()=>{S.ap=null;S.all=false;S.vp=-1;render()}", "audioEl.onended=()=>{S.ap=null;S.all=false;S.vp=-1;S.audioMsg='';render()};audioEl.onerror=()=>{S.audioMsg='تعذر تحميل هذا الصوت؛ اختر قارئًا أو سورة أخرى';render()};audioEl.onplaying=()=>{S.audioMsg=''}")
s = s.replace("function playRecitation(i){const url=recitationUrl(i);if(!url)return;if(audioEl.src===url&&!audioEl.paused)", "function playRecitation(i){const url=recitationUrl(i);if(!url){S.audioMsg='لا يوجد تسجيل متاح لهذا القارئ';render();return}if(audioEl.src!==url){audioEl.pause();audioEl.currentTime=0}if(audioEl.src===url&&!audioEl.paused)")

# Add gesture and press feedback once after the original first render.
s = s.replace('render(true);\nloadCollectedData();', "render(true);\nswipeTabs();document.addEventListener('pointerdown',e=>{if(e.target.closest('button'))soundTap()},{passive:true});updateTimeTheme();loadCollectedData();")
s = s.replace("setInterval(()=>{\n  if(S.tab", "setInterval(()=>{\n  updateTimeTheme();\n  if(S.tab", 1)

p.write_text(s, encoding='utf-8')
print('upgraded original UI integration')
''