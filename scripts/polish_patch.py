from pathlib import Path

p=Path('/home/ubuntu/yawaqit/index.html')
s=p.read_text(encoding='utf-8')

# 1) Full-size embedded Arabic video card, no tiny preview box.
s=s.replace('.player{height:187px;position:relative;padding:0}', '.player{position:relative;padding:0;height:auto;overflow:hidden}', 1)
s=s.replace('.pv{width:208px;height:117px;margin:16px auto 0;', '.pv{width:calc(100% - 28px);height:200px;margin:14px auto 12px;', 1)

# 2) Native-style scroll: hidden white bar, manual drag only.
s=s.replace('#gb{position:absolute;bottom:4px;left:50%;width:110px;height:4px;margin-left:-55px;background:#5a5a5a;border-radius:4px;z-index:4}', '#gb{display:none}#scr{scrollbar-gutter:stable;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;touch-action:pan-y}', 1)
s=s.replace('#scr{flex:1;overflow-y:auto;padding:13px 13px 96px;scrollbar-width:none}', '#scr{flex:1;overflow-y:auto;padding:13px 13px 96px;scrollbar-width:none;-ms-overflow-style:none}#scr::-webkit-scrollbar{display:none}', 1)

# 3) Neutral language button matching the app card style, not the blue pill.
s=s.replace('langBtn" class="btn" style="margin:0;padding:7px 12px;font-size:10px"', 'langBtn" style="margin:0;padding:9px 14px;border-radius:12px;background:#101010;color:#fff;font-size:11px;border:1px solid #262626"', 1)

# 4) Remove golden background glow on the sunset/dawn pages.
s=s.replace('body.sunset #app:before,body.dawn #app:before{content:"";position:absolute;inset:72px 0 66px;pointer-events:none;opacity:.22;transition:opacity 2.5s;background:radial-gradient(circle at 50% 15%,#f6b93b 0,transparent 38%)}', 'body.sunset #app:before,body.dawn #app:before{content:none}', 1)

# 5) Richer tap sounds: two layers, different tone per interaction type.
start=s.find('function soundTap(){'); end=s.find('\nfunction updateTimeTheme',start); assert start>=0 and end>start
new_sound=r'''function playTap(freq,dur,vol){try{soundContext=soundContext||new (window.AudioContext||window.webkitAudioContext)();const o=soundContext.createOscillator(),g=soundContext.createGain();o.type='triangle';o.frequency.value=freq;g.gain.setValueAtTime(vol,soundContext.currentTime);g.gain.exponentialRampToValueAtTime(.0008,soundContext.currentTime+dur);o.connect(g).connect(soundContext.destination);o.start();o.stop(soundContext.currentTime+dur)}catch(e){}}
function soundTap(kind){if(kind==='nav'){playTap(320,.09,.05);setTimeout(()=>playTap(480,.07,.035),40)}else if(kind==='sheet'){playTap(430,.07,.04)}else if(kind==='audio'){playTap(560,.05,.045)}else{playTap(420,.055,.04)}}
function classifyTap(target){if(target.closest('#nav'))return 'nav';if(target.closest('#ov,#sh'))return 'sheet';if(target.closest('[data-a],[data-p],#pa,.pb'))return 'audio';return 'tile'}'''
s=s[:start]+new_sound+s[end:]

# 6) History encyclopedia from an API: al-Mawsoa records are generated from quran.com ayah metadata.
anchor="let LANGS=["
history=r'''
let HISTORY_API_READY=false;
async function loadHistoryApi(){if(HISTORY_API_READY)return;HISTORY_API_READY=true;try{const d=await fetch('https://api.quran.com/api/v4/chapters?language=ar').then(x=>x.json());const ch=d.chapters||[];DET[2]=ch.slice(0,20).map(c=>[`${c.name_arabic} · ${c.translated_name.name}`,`${c.revelation_place==='makkah'?'مكية':'مدنية'} · ${c.verses_count} آية · ترتيبها ${c.revelation_order}`])}catch(e){}}
'''
assert anchor in s
s=s.replace(anchor,history+'\n'+anchor,1)
s=s.replace('loadNamesApi();loadLanguageApi();}', 'loadNamesApi();loadLanguageApi();loadHistoryApi();}', 1)

# 7) Translation button per language, rendered inside the Quran header in the existing pill style.
s=s.replace('const langBtnRow', 'const langBtnRow', 1)
s=s.replace('loadCollectedData();\n</script>', 'loadCollectedData();\n</script>', 1)
s=s.replace('S.surah=i;S.vp=-1;S.all=false;render(true);loadTranslationForSurah(i)}));', 'S.surah=i;S.vp=-1;S.all=false;render(true);loadTranslationForSurah(i)}));\n  A("#trBtn",()=>{if(S.lang==="ar"){S.audioMsg="اختر لغة غير العربية من الإعدادات أولًا";render();return}if(S.tr){S.tr=false;render()}else{S.tr=true;loadTranslationForSurah(S.surah)}});', 1)
s=s.replace('<button class="pill" id="pa">', '<button class="pill" id="trBtn">${I(\'book\')}${S.tr?\'الترجمة مفعّلة\':\'إظهار الترجمة\'}</button><button class="pill" id="pa">', 1)

p.write_text(s,encoding='utf-8')
print('UI polish patch applied')
