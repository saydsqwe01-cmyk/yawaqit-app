from pathlib import Path
import json,re
root=Path('/home/ubuntu/work/yawaqit_extract')
p=root/'index.html'; s=p.read_text()
# Keep the localized previous-prayer line only; remove its duplicate shorthand line.
s=s.replace('<div class="pb-sub">${L(\'prev\')}: <b style="color:#fff">${pr.prev.n}</b> · ${agoText(pr.prev.ago)}</div>', '', 1)
# Build a reliable 50-item Quran pool from the local canonical Quran data.
q=json.loads((root/'public/data/quran/quran_uthmani_full.json').read_text())
selected=[(2,153),(2,286),(3,8),(3,139),(3,159),(5,8),(8,46),(9,51),(10,57),(11,6),(12,87),(13,28),(14,7),(16,90),(17,23),(18,10),(20,25),(20,46),(21,87),(23,1),(24,35),(25,63),(26,80),(28,24),(29,69),(30,21),(31,17),(33,70),(39,53),(40,60),(41,34),(42,43),(49,10),(50,16),(51,56),(53,39),(55,13),(57,4),(59,18),(64,16),(65,2),(65,3),(93,3),(93,5),(94,5),(94,6),(103,3),(112,1),(113,1),(114,1)]
reflections=[
'الصبر مع الصلاة يعين القلب على الثبات.', 'رحمة الله أوسع من تقصيرنا، فاسأله العفو دائمًا.', 'ثبّت قلبك على الإيمان ولا تجعل الدعاء آخر خيار.', 'بعد التعب تأتي قوة جديدة لمن أحسن التوكل.', 'الرفق والحكمة يفتحان القلوب قبل الكلمات.', 'العدل مطلوب مع القريب والبعيد وفي كل حال.', 'اجعل ذكرك لله سببًا لاجتماع قلبك وقوتك.', 'اطمئن إلى تقدير الله وخذ بالأسباب.', 'القرآن شفاء للقلوب وتذكير بنعمة الله.', 'رزق الله محفوظ، فاطلبه بالحلال واطمئن.', 'لا تيأس من رحمة الله مهما طال البلاء.', 'بذكر الله تهدأ النفس ويستقر القلب.', 'شكر النعمة يحفظها ويزيدها.', 'الإحسان والعدل أساس صلاح الحياة.', 'بر الوالدين عبادة عظيمة تبدأ بالكلمة الطيبة.', 'الدعاء في الشدة باب أمل لا يغلق.', 'اطلب العلم والعون من الله بقلب صادق.', 'معية الله تمنح المؤمن أمانًا في الطريق.', 'الفرج قريب لمن دعا ربه بصدق.', 'الفلاح يبدأ بإصلاح الصلاة والقلب.', 'نور الله يهدي القلب إذا صدق في طلب الحق.', 'التواضع يزيد الإنسان رفعة ومحبة.', 'العمل الصالح هو الزاد الحقيقي في كل يوم.', 'فضل الله قريب ممن أحسن الظن وسعى.', 'المجاهدة تفتح أبواب الهداية.', 'المودة والرحمة أساس السكينة في البيت.', 'الصلاة والصبر يصنعان شخصية قوية.', 'ليكن كلامك واضحًا طيبًا يرضي الله.', 'لا تقنط من رحمة الله، فباب التوبة مفتوح.', 'الدعاء عبادة ووعد الله بالاستجابة حق.', 'ادفع الإساءة بالإحسان يتبدل الخصام قربًا.', 'العفو مع القدرة من مكارم الأخلاق.', 'أصلح بين الناس تكن سببًا في الخير.', 'الله أقرب إلى عبده ويعلم ما يخفيه صدره.', 'الغاية من الحياة عبادة الله وإعمار الخير.', 'الإنسان ينال ثمرة سعيه، فابدأ بخطوة صالحة.', 'نعم الله لا تُحصى، فاجعل لسانك رطبًا بالحمد.', 'الله مطلع على أعمالنا، فاستحضر مراقبته.', 'حاسب نفسك قبل أن يبدأ يوم جديد.', 'القوة الحقيقية في الطاعة والإنفاق من الخير.', 'التقوى سبب للمخرج والرزق من حيث لا نحتسب.', 'التوكل لا يلغي السعي بل يطهّر القلب من القلق.', 'اليسر قادم، فلا تجعل الحزن يسرق رجاءك.', 'تكرار الفرج في القرآن يعلّمنا حسن الظن بالله.', 'النجاة في الإيمان والعمل الصالح والتواصي بالحق.', 'التواصي بالصبر يحفظ المجتمع من اليأس.', 'الله واحد، فاجعل توحيده أعظم مقصدك.', 'استعذ بالله من الشر واحفظ قلبك بالذكر.', 'استعذ برب الناس من الوساوس والضعف.', 'اجعل الالتجاء إلى الله حصنك من كل وسواس وقلق.'
]
lookup={(x['number'],a['number']):a['text'].replace('\ufeff','') for x in q['surahs'] for a in x['ayahs']}
surah_names={x['number']:x['name'].replace('سُورَةُ ','').strip() for x in q['surahs']}
entries=[]
for (sn,an),ref in zip(selected,reflections):
    verse=lookup[(sn,an)]
    entries.append([verse, f'{surah_names[sn]}: {an} · العبرة: {ref}'])
block='const DAILY_AYAH_POOL='+json.dumps(entries,ensure_ascii=False,separators=(',',':'))+';'
# Insert pool immediately before the existing dailyEntry function.
marker='function dailyEntry(lang){'
if marker not in s: raise SystemExit('dailyEntry marker missing')
if 'const DAILY_AYAH_POOL=' in s:
    s=re.sub(r'const DAILY_AYAH_POOL=.*?;\nfunction dailyAyahIndex',block+"\nfunction dailyAyahIndex",s,count=1,flags=re.S)
else:
    s=s.replace(marker,block+"\nfunction dailyAyahIndex(){const key='yawaqit-daily-ayah-'+new Date().toISOString().slice(0,10);try{const old=localStorage.getItem(key);if(old!=null&&Number.isInteger(+old)&&+old>=0&&+old<DAILY_AYAH_POOL.length)return +old;const i=Math.floor(Math.random()*DAILY_AYAH_POOL.length);localStorage.setItem(key,String(i));return i}catch(_){return Math.floor(Math.random()*DAILY_AYAH_POOL.length)}}\nfunction dailyEntry(lang){",1)
# Arabic gets one deterministic random selection from 50 per device per day; other locales retain their localized copy.
s=s.replace('function dailyEntry(lang){const rows=DAILY_COPY[lang]||DAILY_COPY.ar;return rows[dayIndex()%rows.length]}', "function dailyEntry(lang){if(lang==='ar')return DAILY_AYAH_POOL[dailyAyahIndex()];const rows=DAILY_COPY[lang]||DAILY_COPY.ar;return rows[dayIndex()%rows.length]}",1)
# Replace API-specific loading copy with one concise message plus an animated circle.
old1='<div class="card mut" style="text-align:center;padding:20px">جارٍ تحميل الأحاديث عبر API...</div>'
old2='<div class="card mut" style="text-align:center;padding:20px">جارٍ تحميل المحتوى من API...</div>'
loader='<div class="card mut content-loader"><span class="content-spinner" aria-hidden="true"></span><span>جاري تحميل المحتوى</span></div>'
s=s.replace(old1,loader).replace(old2,loader)
# Hide Quran translation by default while preserving its existing show/hide button.
s=s.replace("trOpen:true", "trOpen:false", 1)
# Remove frames/backgrounds from translation and tafsir blocks; retain only their compact toggles and text.
css='''.translation-box,.tf{background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;padding:4px 0!important;margin-top:6px!important}.translation-box .h,.tf .h{background:transparent!important;border:0!important;padding:2px 0!important}.translation-text,.tf p{padding:0!important;margin:6px 0 0!important;background:transparent!important;border:0!important}.content-loader{display:flex;align-items:center;justify-content:center;gap:9px;min-height:56px!important;background:transparent!important;border:0!important}.content-spinner{display:inline-block;width:16px;height:16px;border:2px solid currentColor;border-top-color:transparent;border-radius:50%;animation:contentSpin .8s linear infinite}@keyframes contentSpin{to{transform:rotate(360deg)}}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('daily 50 pool, duplicate removal, concise loader, and Quran frameless toggles applied')
