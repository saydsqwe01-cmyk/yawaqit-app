from pathlib import Path
p=Path('/home/ubuntu/work/index.html')
s=p.read_text()

# Add a proper localization layer and normalized search helper.
s=s.replace("function L(k, fallback){const d=UI[S&&S.lang]||UI.ar;return d[k]||fallback||UI.ar[k]||k}", """function L(k, fallback){const d=UI[S&&S.lang]||UI.ar;return d[k]||fallback||UI.ar[k]||k}
const TXT={
 ar:{quranTitle:'المصحف الشريف',surahs:'سورة',searchSurah:'ابحث عن اسم السورة أو رقمها',searchContent:'ابحث داخل المحتوى',translate:'الترجمة',translation:'العربية',noResults:'لا توجد نتائج مطابقة',next:'التالي',result:'النتيجة',quiz:'تحدي الأسئلة',answered:'المجاب',correct:'الصحيح',final:'النتيجة النهائية',retry:'إعادة التحدي',audioDetails:'تفاصيل الصوت',reader:'القارئ',surah:'السورة',ayah:'الآية',playSurah:'تشغيل السورة كاملة',stop:'إيقاف',tafsir:'التفسير الميسر',dailyVerse:'آية وعبرة',about:'بعد كل ضيق فرج قريب',adhkar:'كل الأذكار',search:'ابحث هنا',selectReader:'اختر القارئ',selectSurah:'اختر السورة',listen:'اضغط تشغيل للاستماع',playing:'يتم التشغيل الآن'},
 en:{quranTitle:'The Noble Quran',surahs:'surahs',searchSurah:'Search by surah name or number',searchContent:'Search inside content',translate:'Translation',translation:'English',noResults:'No matching results',next:'Next',result:'Result',quiz:'Quiz challenge',answered:'Answered',correct:'Correct',final:'Final score',retry:'Try again',audioDetails:'Audio details',reader:'Reciter',surah:'Surah',ayah:'Ayah',playSurah:'Play whole surah',stop:'Stop',tafsir:'Tafsir',dailyVerse:'Verse & reflection',about:'After every hardship comes ease',adhkar:'All adhkar',search:'Search here',selectReader:'Choose reciter',selectSurah:'Choose surah',listen:'Press play to listen',playing:'Playing now'},
 fr:{quranTitle:'Le Noble Coran',surahs:'sourates',searchSurah:'Rechercher par nom ou numéro',searchContent:'Rechercher dans le contenu',translate:'Traduction',translation:'Français',noResults:'Aucun résultat',next:'Suivant',result:'Résultat',quiz:'Défi de questions',answered:'Répondues',correct:'Correctes',final:'Résultat final',retry:'Recommencer',audioDetails:'Détails audio',reader:'Récitateur',surah:'Sourate',ayah:'Verset',playSurah:'Lire la sourate entière',stop:'Arrêter',tafsir:'Tafsir',dailyVerse:'Verset et réflexion',about:'Après toute difficulté vient la facilité',adhkar:'Tous les adhkar',search:'Rechercher',selectReader:'Choisir le récitateur',selectSurah:'Choisir la sourate',listen:'Appuyez sur lecture',playing:'Lecture en cours'},
 ur:{quranTitle:'قرآن مجید',surahs:'سورتیں',searchSurah:'سورت کے نام یا نمبر سے تلاش کریں',searchContent:'مواد میں تلاش کریں',translate:'ترجمہ',translation:'اردو',noResults:'کوئی نتیجہ نہیں',next:'اگلا',result:'نتیجہ',quiz:'سوالات کا چیلنج',answered:'جواب دیے',correct:'درست',final:'حتمی نتیجہ',retry:'دوبارہ شروع',audioDetails:'آڈیو کی تفصیل',reader:'قاری',surah:'سورت',ayah:'آیت',playSurah:'مکمل سورت چلائیں',stop:'روکیں',tafsir:'تفسیر',dailyVerse:'آیت اور سبق',about:'ہر مشکل کے بعد آسانی ہے',adhkar:'تمام اذکار',search:'تلاش کریں',selectReader:'قاری منتخب کریں',selectSurah:'سورت منتخب کریں',listen:'سننے کے لیے چلائیں',playing:'اب چل رہا ہے'}
};
function T(k,fallback){return (TXT[S&&S.lang]||TXT.ar)[k]||fallback||TXT.ar[k]||k}
function normalizeSearch(v){return String(v||'').toLocaleLowerCase().normalize('NFKD').replace(/[\\u064B-\\u065F\\u0670\\u0640]/g,'').replace(/[إأآٱ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/ؤ/g,'و').replace(/ئ/g,'ي').trim()}
function matchesSearch(value,query){return !normalizeSearch(query)||normalizeSearch(value).includes(normalizeSearch(query))}""")
# make surah names follow chosen language, using API simple name when available
s=s.replace("function SN(s){return S&&S.lang==='en'?s.e:s.n}", "function SN(s){if(!s)return '';if(S&&S.lang==='ar')return s.n;if(S&&S.lang==='en')return s.e;if(S&&S.lang==='fr')return s.fr||s.e;if(S&&S.lang==='ur')return s.ur||s.e;return s.e}")
# Add localized metadata fields and Arabic translation fallback
s=s.replace("SUR=(q.surahs||[]).map(s=>({n:s.name.replace(/^سُورَةُ\\s*/,'').trim(),e:s.englishName,t:s.revelationType==='Meccan'?'مكية':'مدنية',v:(s.ayahs||[]).map(v=>[String(v.text||'').replace(/^\\uFEFF/,''),'',''])}));", "SUR=(q.surahs||[]).map(s=>({n:s.name.replace(/^سُورَةُ\\s*/,'').trim(),e:s.englishName,fr:s.englishName,ur:s.englishName,t:s.revelationType==='Meccan'?'مكية':'مدنية',v:(s.ayahs||[]).map(v=>[String(v.text||'').replace(/^\\uFEFF/,'') ,String(v.text||'').replace(/^\\uFEFF/,'') ,''])}));")
# Change Arabic translation behavior and include translation immediately for Arabic.
s=s.replace("async function loadTranslationForSurah(si){if(S.lang==='ar'||!S.transId){S.tr=false;render();return}", "async function loadTranslationForSurah(si){if(S.lang==='ar'){if(SUR[si])SUR[si].v.forEach(v=>{v[1]=v[0]});S.tr=true;render();return}if(!S.transId){S.tr=false;render();return}")
# localized search lists
s=s.replace("filter(x=>!q||x.s.n.includes(q)||String(x.i+1).includes(q))", "filter(x=>matchesSearch([x.s.n,x.s.e,x.s.fr,x.s.ur,x.i+1].join(' '),q))")
s=s.replace("placeholder=\"ابحث عن سورة أو رقم\"", "placeholder=\"${T('searchSurah')}\"")
s=s.replace("<b style=\"font-size:18px\">المصحف الشريف</b><span class=\"mut\" style=\"font-size:10px\">${ar(SUR.length)} سورة</span>", "<b style=\"font-size:18px\">${T('quranTitle')}</b><span class=\"mut\" style=\"font-size:10px\">${ar(SUR.length)} ${T('surahs')}</span>")
# Replace Quran translation box and hardcoded headings.
s=s.replace("<span>${TRL[trl]}</span>", "<span>${T('translate')}: ${S.lang==='ar'?T('translation'):(LANGS.find(x=>x.iso_code===S.lang)?.native_name||T('translation'))}</span>")
s=s.replace("${S.tr?`<div class=\"bx\"><div class=\"h\" data-t=\"tr\"><button class=\"ib\" data-tp=\"1\">${I('tri')}</button><span>${T('translate')}: ${S.lang==='ar'?T('translation'):(LANGS.find(x=>x.iso_code===S.lang)?.native_name||T('translation'))}</span></div>${S.trOpen?`<p class=\"en\">${trl?'(الترجمة غير متوفرة في هذه النسخة التجريبية) ':''}${v[1]}</p>`:''}</div>`:''}", "${S.tr?`<div class=\"bx translation-box\"><div class=\"h\" data-t=\"tr\"><button class=\"ib\" data-tp=\"1\">${I('tri')}</button><span>${T('translate')}: ${S.lang==='ar'?T('translation'):(LANGS.find(x=>x.iso_code===S.lang)?.native_name||T('translation'))}</span></div>${S.trOpen?`<p class=\"translation-text\">${v[1]||T('translation')}</p>`:''}</div>`:''}")
s=s.replace("${S.tf?`<div class=\"bx tf ${S.tfx[i]?'x':''}\"><div class=\"h\" style=\"direction:rtl\"><span style=\"display:flex;gap:6px;align-items:center\">${I('book','width:16px;height:16px')}التفسير الميسر</span>", "${S.tf?`<div class=\"bx tf ${S.tfx[i]?'x':''}\"><div class=\"h\" style=\"direction:rtl\"><span style=\"display:flex;gap:6px;align-items:center\">${I('book','width:16px;height:16px')}${T('tafsir')}</span>")
# remove gold crescent icon from prayer banner
s=s.replace('<span class="pb-icon">${I(\'moon\')}</span>','')
# localized home labels and daily cards
s=s.replace("[['تحدي الأسئلة',null,'quiz'],['المصحف','book','quran'],['الفيديوهات','film','vid'],['الصوتيات','head','aud']]", "[[T('quiz'),null,'quiz'],[L('quran'),'book','quran'],[L('vid'),'film','vid'],[L('aud'),'head','aud']]")
s=s.replace('<div class="sec">آية وعبرة</div><div class="card" style="text-align:center"><div class="verse">﴿فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًا﴾</div><div class="ref">بعد كل ضيق فرج قريب</div></div>', '<div class="sec">${T(\'dailyVerse\')}</div><div class="card" style="text-align:center"><div class="verse">﴿فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًا﴾</div><div class="ref">${T(\'about\')}</div></div>')
# localized details/audio/adhkar/search
s=s.replace('placeholder="ابحث داخل المحتوى"', 'placeholder="${T(\'searchContent\')}"')
s=s.replace('placeholder="ابحث هنا"', 'placeholder="${T(\'search\')}"')
s=s.replace('>كل الأذكار</b>', '>${T(\'adhkar\')}</b>')
s=s.replace('<b>تفاصيل الصوت</b>', '<b>${T(\'audioDetails\')}</b>')
s=s.replace('القارئ: ${r.name||\'—\'}', '${T(\'reader\')}: ${r.name||\'—\'}')
s=s.replace('سورة: ${s.n||\'—\'}', '${T(\'surah\')}: ${s.n||\'—\'}')
s=s.replace("'اضغط تشغيل للاستماع'", "T('listen')")
s=s.replace("'يتم التشغيل الآن'", "T('playing')")
# Search filter in details and sheet/list helper
s=s.replace("items.filter(x=>x.includes(q))", "items.filter(x=>matchesSearch(x,q))")
s=s.replace("const rows=d.filter(x=>String(x[0]).includes(q)||String(x[1]).includes(q));", "const rows=d.filter(x=>matchesSearch(String(x[0])+' '+String(x[1]),q));")
# Add localized quiz banks and replace quiz renderer.
needle="const QS=[["
insert="""const QUIZ_BANK={
 ar:[['من هو أول من جمع المصحف الشريف؟',['أبو بكر الصديق رضي الله عنه','عمر بن الخطاب رضي الله عنه','عثمان بن عفان رضي الله عنه','علي بن أبي طالب رضي الله عنه'],0],['كم عدد أركان الإسلام؟',['ثلاثة','أربعة','خمسة','ستة'],2],['كم عدد سور القرآن الكريم؟',['١١٠','١١٤','١٢٠','١٢٤'],1],['ما هي أول سورة نزلت آياتها؟',['العلق','الفاتحة','المدثر','البقرة'],0],['ما هي أطول سورة في القرآن؟',['البقرة','آل عمران','النساء','المائدة'],0]],
 en:[['Who first compiled the Quran?',['Abu Bakr','Umar ibn Al-Khattab','Uthman ibn Affan','Ali ibn Abi Talib'],0],['How many pillars of Islam are there?',['Three','Four','Five','Six'],2],['How many surahs are in the Quran?',['110','114','120','124'],1],['Which was the first surah revealed?',['Al-Alaq','Al-Fatihah','Al-Muddaththir','Al-Baqarah'],0],['Which is the longest surah?',['Al-Baqarah','Aal Imran','An-Nisa','Al-Maidah'],0]],
 fr:[['Qui a compilé le premier le Coran ?',['Abou Bakr','Omar ibn Al-Khattab','Othman ibn Affan','Ali ibn Abi Talib'],0],['Combien y a-t-il de piliers de l’islam ?',['Trois','Quatre','Cinq','Six'],2],['Combien de sourates dans le Coran ?',['110','114','120','124'],1],['Quelle fut la première sourate révélée ?',['Al-Alaq','Al-Fatiha','Al-Muddaththir','Al-Baqara'],0],['Quelle est la plus longue sourate ?',['Al-Baqara','Aal Imran','An-Nisa','Al-Maida'],0]],
 ur:[['قرآن کریم سب سے پہلے کس نے جمع کیا؟',['ابوبکر صدیق','عمر بن خطاب','عثمان بن عفان','علی بن ابی طالب'],0],['اسلام کے کتنے ارکان ہیں؟',['تین','چار','پانچ','چھ'],2],['قرآن میں کتنی سورتیں ہیں؟',['۱۱۰','۱۱۴','۱۲۰','۱۲۴'],1],['سب سے پہلے کون سی سورت نازل ہوئی؟',['العلق','الفاتحہ','المدثر','البقرہ'],0],['سب سے لمبی سورت کون سی ہے؟',['البقرہ','آل عمران','النساء','المائدہ'],0]]};
function quizSet(){return QUIZ_BANK[S.lang]||QUIZ_BANK.en}
"""
s=s.replace(needle,insert+needle)
s=s.replace("const q=S.qz,n=q.i,QSET=Q_API.length?Q_API:QS,tot=QSET.length,pc=q.ans?Math.round(q.ok/q.ans*100):0;", "const q=S.qz,n=q.i,QSET=quizSet(),tot=QSET.length,pc=q.ans?Math.round(q.ok/q.ans*100):0;")
s=s.replace('تحدي الأسئلة</b>', "${T('quiz')}</b>")
s=s.replace('المجاب : ${q.ans}', "${T('answered')}: ${q.ans}")
s=s.replace('الصحيح : ${q.ok}', "${T('correct')}: ${q.ok}")
s=s.replace('النتيجة النهائية', "${T('final')}")
s=s.replace('إعادة التحدي', "${T('retry')}")
s=s.replace("${n===tot-1?'النتيجة':'التالي'}", "${n===tot-1?T('result'):T('next')}")
# Normalize quran/detail search handlers and improve language switch reset/translation.
s=s.replace("S.transId=tc[0]?tc[0].id:null;document.documentElement.lang=S.lang;", "S.transId=tc[0]?tc[0].id:null;Q_API=[];QUIZ_API_READY=false;document.documentElement.lang=S.lang;")
s=s.replace("if(S.lang!=='ar'&&S.transId)loadTranslationForSurah(S.surah);", "loadTranslationForSurah(S.surah);")
s=s.replace("S.quranQ=e.target.value;render()", "S.quranQ=e.target.value;render()")
s=s.replace("S.detQ=ev.target.value;render()", "S.detQ=ev.target.value;render()")
# Use correct answer index from localized bank.
s=s.replace("if(q.pick===QS[q.i][2])q.ok++;render()", "if(q.pick===quizSet()[q.i][2])q.ok++;render()")
# Vary sound effects and use classifier.
s=s.replace("function soundTap(kind){if(kind==='nav'){playTap(320,.09,.05);setTimeout(()=>playTap(480,.07,.035),40)}else if(kind==='sheet'){playTap(430,.07,.04)}else if(kind==='audio'){playTap(560,.05,.045)}else{playTap(420,.055,.04)}}", """function soundTap(kind){if(kind==='nav'){playTap(320,.09,.05);setTimeout(()=>playTap(480,.07,.035),40)}else if(kind==='sheet'){playTap(430,.07,.04)}else if(kind==='audio'){playTap(560,.05,.045)}else if(kind==='wrong'){playTap(180,.12,.06);setTimeout(()=>playTap(120,.14,.04),55)}else if(kind==='correct'){playTap(620,.08,.05);setTimeout(()=>playTap(820,.12,.04),55)}else{playTap(420,.055,.04)}}""")
s=s.replace("A('[data-o]',e=>{const q=S.qz;if(q.pick!=null)return;q.pick=+e.dataset.o;q.ans++;if(q.pick===quizSet()[q.i][2])q.ok++;render()});", "A('[data-o]',e=>{const q=S.qz;if(q.pick!=null)return;q.pick=+e.dataset.o;q.ans++;const good=q.pick===quizSet()[q.i][2];if(good)q.ok++;soundTap(good?'correct':'wrong');render()});")
s=s.replace("document.addEventListener('pointerdown',e=>{if(e.target.closest('button'))soundTap()}", "document.addEventListener('pointerdown',e=>{if(e.target.closest('button'))soundTap(classifyTap(e.target))}")
# Visual polish for translation and answer states.
s=s.replace('</style>', '''.pb-icon{display:none}.translation-box{border-right:3px solid var(--blue);animation:translationIn .45s ease-out}.translation-text{direction:inherit;text-align:start;color:#d7e9f7;font-family:'Noto Kufi Arabic',system-ui,sans-serif;font-size:12px!important;line-height:1.9!important}.op.ok{background:rgba(46,204,113,.13);box-shadow:0 0 0 1px rgba(46,204,113,.25),0 6px 18px rgba(46,204,113,.13)}.op.no{background:rgba(231,76,60,.13);box-shadow:0 0 0 1px rgba(231,76,60,.25),0 6px 18px rgba(231,76,60,.13)}@keyframes translationIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}@keyframes correctPulse{0%{transform:scale(.96)}50%{transform:scale(1.04)}100%{transform:scale(1)}}.op.ok{animation:correctPulse .5s ease-out}.op.no{animation:sh .42s ease-out}.surah-choice,.tile,.btn,.pill,.audio-select,.li{transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s,background .25s}.surah-choice:hover,.tile:hover,.btn:hover,.pill:hover,.audio-select:hover,.li:hover{box-shadow:0 8px 22px rgba(11,134,201,.18);transform:translateY(-2px)}
</style>''',1)
p.write_text(s)
