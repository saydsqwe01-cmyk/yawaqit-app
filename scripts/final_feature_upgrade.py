from pathlib import Path
import re

p=Path('/home/ubuntu/yawaqit/index.html')
s=p.read_text(encoding='utf-8')

# Full-height phone on a real phone; desktop keeps the centered phone frame.
s=s.replace('#app{width:100%;max-width:420px;height:100%;max-height:820px;', '#app{width:100%;max-width:420px;height:100dvh;min-height:100dvh;max-height:none;', 1)
s=s.replace('@media(min-width:500px){#app{border-radius:30px;box-shadow:0 0 0 1px #333,0 30px 80px rgba(0,0,0,.6);height:96%;margin-top:2vh}}', '@media(min-width:500px){#app{border-radius:30px;box-shadow:0 0 0 1px #333,0 30px 80px rgba(0,0,0,.6);height:96%;max-height:820px;min-height:0;margin-top:2vh}}', 1)

# Celestial indicator stays inside the prayer card, never as a page background.
s=s.replace('</style>', '''
.celestial{height:54px;margin:8px 0 2px;border-radius:14px;background:#080808;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center}
.celestial-label{position:absolute;right:12px;top:7px;color:#9b9b9b;font-size:9px;z-index:2}.orbit{width:180px;height:42px;border-bottom:1px solid #333;border-radius:50%;position:relative}.sun{position:absolute;width:27px;height:27px;border-radius:50%;background:#f6b93b;box-shadow:0 0 18px #f6b93b;left:30px;top:6px;transition:all 2s}.earth{position:absolute;width:13px;height:13px;border-radius:50%;background:#2d9bd0;right:34px;bottom:4px;box-shadow:0 0 8px #2d9bd0;transition:all 2s}body.sunset .sun{background:#e57345;box-shadow:0 0 22px #e57345;left:80px;top:15px}body.night .sun{background:#d5d9e8;box-shadow:0 0 10px #d5d9e8;left:115px;top:8px}.ytframe{width:100%;height:100%;border:0;border-radius:10px;display:block}
'''+ '</style>', 1)

s=s.replace("qz:null,detQ:'',geoReady:false,audioMsg:''", "qz:null,detQ:'',geoReady:false,audioMsg:'',lang:'ar',langName:'العربية',langDir:'rtl',transId:null", 1)

# Replace next-prayer helper with previous-prayer context and an Arabic elapsed-time label.
start=s.find('function prayers(){'); end=s.find('\nfunction dates()',start)
assert start>=0 and end>start
pr=r'''function agoText(sec){sec=Math.max(0,Math.floor(sec));if(sec<60)return 'منذ أقل من دقيقة';const m=Math.floor(sec/60);return m<60?`منذ ${ar(m)} دقيقة`:`منذ ${ar(Math.floor(m/60))} ساعة`}
function prayers(){const d=new Date(),now=d.getHours()*3600+d.getMinutes()*60+d.getSeconds(),times=PR.map(p=>p[1]*3600+p[2]*60);let i=times.findIndex(x=>x>now),add=0;if(i<0){i=0;add=86400}const prevIndex=(i+PR.length-1)%PR.length;let prevSec=now-times[prevIndex];if(prevSec<0)prevSec+=86400;const df=times[i]+add-now;return{i,n:PR[i][0],cd:p2(Math.floor(df/3600))+':'+p2(Math.floor(df%3600/60))+':'+p2(df%60),prev:{n:PR[prevIndex][0],ago:prevSec}}}'''
s=s[:start]+pr+s[end:]

# Language state and Quran translation API.
anchor="const p2=n=>String(n).padStart(2,'0');"
lang_code=r'''
let LANGS=[{iso_code:'ar',name:'Arabic',native_name:'العربية',direction:'rtl'},{iso_code:'en',name:'English',native_name:'English',direction:'ltr'},{iso_code:'ur',name:'Urdu',native_name:'اردو',direction:'rtl'},{iso_code:'fr',name:'French',native_name:'Français',direction:'ltr'},{iso_code:'tr',name:'Turkish',native_name:'Türkçe',direction:'ltr'},{iso_code:'id',name:'Indonesian',native_name:'Bahasa Indonesia',direction:'ltr'},{iso_code:'es',name:'Spanish',native_name:'Español',direction:'ltr'}];
let TRANSLATIONS=[];
async function loadLanguageApi(){try{const [ls,ts]=await Promise.all([fetch('https://api.quran.com/api/v4/resources/languages').then(x=>x.json()),fetch('https://api.quran.com/api/v4/resources/translations').then(x=>x.json())]);if(ls.languages&&ls.languages.length)LANGS=[{iso_code:'ar',name:'Arabic',native_name:'العربية',direction:'rtl'},...ls.languages.filter(x=>x.iso_code!=='ar')];TRANSLATIONS=ts.translations||[]}catch(e){}}
async function loadTranslationForSurah(si){if(S.lang==='ar'||!S.transId){S.tr=false;render();return}try{const chapter=si+1;const d=await fetch(`https://api.quran.com/api/v4/verses/by_chapter/${chapter}?translations=${S.transId}&fields=text_uthmani&per_page=300`).then(x=>x.json());const vs=d.verses||[];vs.forEach((v,i)=>{if(SUR[si]&&SUR[si].v[i])SUR[si].v[i][1]=v.translations&&v.translations[0]?v.translations[0].text:''});S.tr=true;render()}catch(e){S.audioMsg='تعذر تحميل ترجمة هذه السورة';render()}}
'''
assert anchor in s
s=s.replace(anchor,lang_code+'\n'+anchor,1)

# Make the player open an embedded YouTube video instead of only showing a thumbnail.
start=s.find('vid(){'); end=s.find('quran(){',start); assert start>=0 and end>start
video=r'''vid(){const v=VID[S.vid]||['فيديو إسلامي','من قناة موثوقة',0,'',''];const id=v[3]||'';return `<div class="card player"><div class="thumb pv" id="pp">${id?`<iframe class="ytframe" src="https://www.youtube.com/embed/${id}?rel=0&modestbranding=1" title="${String(v[0]).replace(/"/g,'')}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`:I(S.playing?'pause':'play')}</div><div class="ctl"><span>${fmt(S.t)}</span><input type="range" id="sk" min="0" max="1" value="0"><span>يوتيوب</span><button id="sp" style="display:flex;align-items:center;gap:2px">${I('spd','width:20px;height:20px')}<small>${SPD[S.spd]}x</small></button></div></div><div class="card"><div style="font-size:13px;margin-bottom:6px">${v[0]}</div><div class="mut" style="font-size:10px">${v[1]} · ${v[4]||'قناة إسلامية'}</div></div><div class="sec">٣٠ فيديو وخطبة ورسالة يومية</div>${VID.map((x,i)=>`<button class="vi ${i===S.vid?'sel':''}" data-v="${i}"><div class="thumb th" style="background-image:url('https://i.ytimg.com/vi/${x[3]}/mqdefault.jpg');background-size:cover"></div><div class="tx"><b>${x[0]}</b><small>${x[1]}</small></div>${i===S.vid?`<div class="ck">${I('check')}</div>`:'<div class="ph"></div>'}</button>`).join('')}`},
'''
s=s[:start]+video+s[end:]

# Put sun/earth and previous prayer text inside the existing home prayer card.
s=s.replace('<div class="pt">', '<div class="celestial"><span class="celestial-label">حسب الوقت الحالي</span><div class="orbit"><i class="sun"></i><i class="earth"></i></div></div><div style="font-size:9px;color:#9b9b9b;text-align:center;margin:4px 0">الصلاة السابقة: <b style="color:#fff">${pr.prev.n}</b> · ${agoText(pr.prev.ago)}</div><div class="pt">', 1)

# Add language row to the original settings sheet.
s=s.replace("sheet(`<h3>الإعدادات</h3>${row('tr','إظهار الترجمة')}${row('tf','إظهار التفسير')}<div class=\"tg\"><span>حجم خط المصحف</span>", "sheet(`<h3>الإعدادات</h3><div class=\"tg\"><span>لغة القرآن والواجهة</span><button id=\"langBtn\" class=\"btn\" style=\"margin:0;padding:7px 12px;font-size:10px\">${S.langName}</button></div>${row('tr','إظهار الترجمة')}${row('tf','إظهار التفسير')}<div class=\"tg\"><span>حجم خط المصحف</span>", 1)
s=s.replace("$('#sh').querySelectorAll('.sw').forEach(s=>s.onclick=()=>{S[s.dataset.k]=!S[s.dataset.k];s.classList.toggle('on');render()});", "$('#sh').querySelectorAll('.sw').forEach(s=>s.onclick=()=>{S[s.dataset.k]=!S[s.dataset.k];s.classList.toggle('on');render()});$('#langBtn').onclick=()=>listSheet('اختر اللغة',LANGS.map(x=>x.native_name||x.name),i=>{const l=LANGS[i]||LANGS[0];S.lang=l.iso_code;S.langName=l.native_name||l.name;S.langDir=l.direction||'ltr';S.transId=(TRANSLATIONS.find(x=>String(x.language_name||'').toLowerCase().startsWith(String(l.name||'').toLowerCase().slice(0,4)))||{}).id||null;document.documentElement.lang=S.lang;document.documentElement.dir=S.langDir;loadTranslationForSurah(S.surah)});", 1)

# Load language metadata with the existing data loader.
s=s.replace('loadNamesApi();}', 'loadNamesApi();loadLanguageApi();}', 1)
# Make selecting a surah refresh its translation if a language is active.
s=s.replace("A('#pk',()=>listSheet('اختر السورة',SUR.map(s=>s.n),i=>{S.surah=i;S.vp=-1;S.all=false;render(true)}));", "A('#pk',()=>listSheet('اختر السورة',SUR.map(s=>s.n),i=>{S.surah=i;S.vp=-1;S.all=false;render(true);loadTranslationForSurah(i)}));", 1)

p.write_text(s,encoding='utf-8')
print('final feature patch applied')
''