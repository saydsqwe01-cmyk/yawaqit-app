from pathlib import Path
import re

p = Path('/home/ubuntu/yawaqit/index.html')
s = p.read_text(encoding='utf-8')

# Remove duplicate language keys left by earlier additive patches.
s = s.replace(",lang:'ar',langName:'العربية',langDir:'rtl',transId:null};", "};", 1)

# Keep the original URL from the external video feed for a reliable fallback link.
s = s.replace("VID=VIDEO_DATA.map(x=>[x.title,x.description,0,x.id,x.channel]);", "VID=VIDEO_DATA.map(x=>[x.title,x.description,0,x.id,x.channel,x.url]);", 1)

# Add a complete, localized list of notable women.
anchor = "DET[18]=[['الصدق أمانة','من محاسن الأخلاق'],['الرحمة بالخلق','خلق يحبه الله']];"
assert anchor in s
women = r'''const WOMEN_STORIES={
ar:[['مريم بنت عمران','سيدة نساء العالمين، العابدة الصديقة'],['آسية بنت مزاحم','امرأة فرعون المؤمنة ومثال الثبات'],['خديجة بنت خويلد','أم المؤمنين وأول من آمن بالنبي ﷺ'],['عائشة بنت أبي بكر','أم المؤمنين وعالمة الأمة'],['فاطمة الزهراء','ابنة النبي ﷺ وسيدة نساء أهل الجنة'],['حفصة بنت عمر','أم المؤمنين وحافظة المصحف'],['أم سلمة','أم المؤمنين صاحبة الرأي والحكمة'],['صفية بنت حيي','أم المؤمنين الكريمة الصابرة'],['زينب بنت جحش','أم المؤمنين وكثيرة الصدقة'],['سمية بنت خياط','أول شهيدة في الإسلام'],['هاجر أم إسماعيل','رمز التوكل والصبر والسعي'],['سارة زوج إبراهيم','الزوجة الصالحة وأم الأنبياء'],['أسماء بنت أبي بكر','ذات النطاقين وصاحبة الهجرة'],['نسيبة بنت كعب','أم عمارة ونموذج الشجاعة'],['خولة بنت ثعلبة','صاحبة قصة الظهار التي نزل فيها القرآن'],['رفيدة الأسلمية','من رائدات رعاية الجرحى في الإسلام'],['جويرية بنت الحارث','أم المؤمنين كثيرة البركة'],['ميمونة بنت الحارث','أم المؤمنين العابدة'],['رقية بنت محمد','ابنة النبي ﷺ الصابرة'],['أم كلثوم بنت محمد','ابنة النبي ﷺ المهاجرة الصابرة']],
en:[['Maryam bint Imran','The devoted and truthful mother of Isa'],['Asiya bint Muzahim','The believing wife of Pharaoh and a model of steadfastness'],['Khadijah bint Khuwaylid','The first believer and Mother of the Believers'],['Aisha bint Abu Bakr','Mother of the Believers and scholar of the Ummah'],['Fatimah az-Zahra','Daughter of the Prophet and leader of the women of Paradise'],['Hafsa bint Umar','Mother of the Believers and guardian of the Mushaf'],['Umm Salamah','Wise Mother of the Believers'],['Safiyyah bint Huyayy','Noble and patient Mother of the Believers'],['Zaynab bint Jahsh','Charitable Mother of the Believers'],['Sumayyah bint Khayyat','The first martyr in Islam'],['Hajar','A symbol of trust, patience and striving'],['Sarah','Righteous wife of Ibrahim and mother of prophets'],['Asma bint Abi Bakr','The woman of the two belts and companion of the Hijrah'],['Nusaybah bint Kab','Umm Umara and a model of courage'],['Khawlah bint Thalabah','The woman whose case was heard by Allah'],['Rufaidah al-Aslamiyyah','An early Muslim caregiver of the wounded'],['Juwayriyyah bint al-Harith','A blessed Mother of the Believers'],['Maymunah bint al-Harith','A devout Mother of the Believers'],['Ruqayyah bint Muhammad','Patient daughter of the Prophet'],['Umm Kulthum bint Muhammad','Patient emigrant daughter of the Prophet']],
fr:[['Maryam bint Imran','La dévouée et véridique mère de Issa'],['Asiya bint Muzahim','L’épouse croyante de Pharaon, modèle de constance'],['Khadija bint Khuwaylid','La première croyante et Mère des croyants'],['Aisha bint Abu Bakr','Mère des croyants et savante de la communauté'],['Fatima az-Zahra','Fille du Prophète et dame du Paradis'],['Hafsa bint Umar','Mère des croyants et gardienne du Mushaf'],['Umm Salama','Mère des croyants, sage et perspicace'],['Safiyya bint Huyayy','Mère des croyants, noble et patiente'],['Zaynab bint Jahsh','Mère des croyants, généreuse'],['Sumayya bint Khayyat','Première martyre de l’islam'],['Hajar','Symbole de confiance et de patience'],['Sarah','Épouse vertueuse d’Ibrahim'],['Asma bint Abi Bakr','La femme aux deux ceintures'],['Nusaybah bint Kab','Umm Umara, modèle de courage'],['Khawlah bint Thalabah','La femme dont la plainte fut entendue'],['Rufaidah al-Aslamiyyah','Une des premières soignantes musulmanes'],['Juwayriyyah bint al-Harith','Mère des croyants bénie'],['Maymunah bint al-Harith','Mère des croyants dévote'],['Ruqayyah bint Muhammad','Fille patiente du Prophète'],['Umm Kulthum bint Muhammad','Fille patiente et émigrée du Prophète']],
ur:[['مریم بنت عمران','عبادت گزار اور سچی ماں'],['آسیہ بنت مزاحم','فرعون کی مؤمن بیوی اور ثابت قدمی کی مثال'],['خدیجہ بنت خویلد','پہلی مؤمنہ اور ام المؤمنین'],['عائشہ بنت ابی بکر','ام المؤمنین اور امت کی عالمہ'],['فاطمہ الزہراء','نبی ﷺ کی بیٹی اور جنت کی خواتین کی سردار'],['حفصہ بنت عمر','ام المؤمنین اور مصحف کی محافظ'],['ام سلمہ','دانش مند ام المؤمنین'],['صفیہ بنت حیی','شریف اور صابر ام المؤمنین'],['زینب بنت جحش','سخی ام المؤمنین'],['سمیہ بنت خیاط','اسلام کی پہلی شہیدہ'],['ہاجرہ','توکل اور صبر کی مثال'],['سارہ','ابراہیم کی نیک زوجہ'],['اسماء بنت ابی بکر','ذات النطاقین اور ہجرت کی ساتھی'],['نسیبہ بنت کعب','شجاعت کی مثال'],['خولہ بنت ثعلبہ','وہ خاتون جن کی فریاد سنی گئی'],['رفیدہ اسلمیہ','زخمیوں کی ابتدائی مسلم نگہداشت کرنے والی'],['جویریہ بنت حارث','بابرکت ام المؤمنین'],['میمونہ بنت حارث','عبادت گزار ام المؤمنین'],['رقیہ بنت محمد','نبی ﷺ کی صابر بیٹی'],['ام کلثوم بنت محمد','نبی ﷺ کی صابر مہاجر بیٹی']]
};
function updateWomenStories(){DET[8]=(WOMEN_STORIES[S.lang]||WOMEN_STORIES.ar).map(x=>[x[0],x[1]])}
'''
s = s.replace(anchor, anchor + "\n" + women, 1)

# Use the localized women list after the fetched data layer finishes.
s = s.replace("DET[8]=[['خديجة رضي الله عنها','أم المؤمنين وأول من آمن بالنبي ﷺ'],['مريم عليها السلام','سيدة نساء العالمين']];", "updateWomenStories();", 1)
# Refresh story language immediately when the language setting changes.
s = s.replace("document.documentElement.dir=S.langDir;", "document.documentElement.dir=S.langDir;updateWomenStories();", 1)

# Re-fetch prophet stories when the selected language changes instead of using an old-language cache.
s = s.replace("let PROPHET_API_READY=false,PROPHET_API_LOADING=false;", "let PROPHET_API_READY=false,PROPHET_API_LANG='',PROPHET_API_LOADING=false;", 1)
s = s.replace("if(PROPHET_API_READY||PROPHET_API_LOADING)return;", "if((PROPHET_API_READY&&PROPHET_API_LANG===S.lang)||PROPHET_API_LOADING)return;", 1)
s = s.replace("DET[17]=rows;PROPHET_API_READY=true;", "DET[17]=rows;PROPHET_API_LANG=S.lang;PROPHET_API_READY=true;", 1)

# Put all supplied non-sheikh visuals into the prophets stories view, preserving full images.
story_marker = "const list=shown.map(x=>`<div class=\"card det-item\"><div class=\"verse\">${x[0]}</div><div class=\"ref\">${x[1]}</div></div>`).join('');return `<div class=\"card hd\">"
assert story_marker in s
story_art = r'''const list=shown.map(x=>`<div class="card det-item"><div class="verse">${x[0]}</div><div class="ref">${x[1]}</div></div>`).join('');const storyArt=n===17?`<div class="story-art-grid" aria-label="صور قصص الأنبياء">${[['/assets/prayer-frame.png','إطار مواقيت الصلاة'],['/assets/tasbeeh-device.png','السبحة الإلكترونية'],['/assets/salawat.png','الصلاة على النبي ﷺ'],['/assets/remember-warning.png','لا تنس ذكر الله'],['/assets/adhkar-footer.png','الأذكار']].map(([src,alt])=>`<figure><img src="${src}" alt="${alt}"><figcaption>${alt}</figcaption></figure>`).join('')}</div>`:'';return `<div class="card hd">'''
s = s.replace(story_marker, story_art, 1)
# Render the story visuals after the section heading and before entries.
needle = "</div>${HADITH_API_LOADING&&n===0?"
assert needle in s
s = s.replace(needle, "</div>${storyArt}${HADITH_API_LOADING&&n===0?", 1)

# Make the video iframe robust and add a direct YouTube fallback link.
s = s.replace('id="pp">${id?`<iframe class="ytframe" src="https://www.youtube.com/embed/${id}?rel=0&modestbranding=1" title="${String(v[0]).replace(/"/g,\'\')}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`:I(S.playing?\'pause\':\'play\')}</div>', 'id="video-frame-wrap">${id?`<iframe class="ytframe" src="https://www.youtube-nocookie.com/embed/${id}?rel=0&modestbranding=1&playsinline=1&enablejsapi=1" title="${String(v[0]).replace(/"/g,\'\')}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" loading="lazy" allowfullscreen></iframe>`:I(S.playing?\'pause\':\'play\')}</div>', 1)
# The exact HTML expression can vary after prior patches; apply a simpler guaranteed replacement if needed.
s = s.replace('const v=VID[S.vid]||[\'فيديو إسلامي\',\'من قناة موثوقة\',0,\'\',\'\'];const id=v[3]||\'\';', "const v=VID[S.vid]||['فيديو إسلامي','من قناة موثوقة',0,'','',''];const id=v[3]||'';const videoUrl=v[5]||`https://www.youtube.com/watch?v=${id}`;", 1)
s = s.replace('</div></div><div class="card"><div style="font-size:13px;margin-bottom:6px">${v[0]}</div><div class="mut" style="font-size:10px">${v[1]} · ${v[4]||\'قناة إسلامية\'}</div></div>', '</div></div><div class="card"><div style="font-size:13px;margin-bottom:6px">${v[0]}</div><div class="mut" style="font-size:10px">${v[1]} · ${v[4]||\'قناة إسلامية\'}</div><a class="video-open-link" href="${videoUrl}" target="_blank" rel="noopener noreferrer">فتح الفيديو في YouTube إذا لم يعمل التشغيل داخل الصفحة ↗</a></div>', 1)
# Remove the old parent click binding that could interfere with the embedded iframe.
s = s.replace("  A('#pp',()=>{const v=VID[S.vid];if(v&&v[3])window.open('https://www.youtube.com/watch?v='+v[3],'_blank','noopener');else{S.playing=!S.playing;render()}});\n", "", 1)

# Add non-cropping story art and fallback-link styles before the first style close.
css = r'''
.story-art-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:8px 0 12px}.story-art-grid figure{margin:0;min-height:116px;padding:7px;border:1px solid #282828;border-radius:15px;background:#070707;text-align:center}.story-art-grid img{width:100%;height:86px;object-fit:contain;object-position:center;border-radius:10px;display:block}.story-art-grid figcaption{font-size:8px;color:#aaa;margin-top:5px}.video-open-link{display:block;color:#4fb3ec;font-size:9px;text-decoration:none;margin-top:9px}.video-open-link:hover{text-decoration:underline}
'''
s = s.replace('</style>', css + '</style>', 1)

p.write_text(s, encoding='utf-8')
print('actual index finalized')
