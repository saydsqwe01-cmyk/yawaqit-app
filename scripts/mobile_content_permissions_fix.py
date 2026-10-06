from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Keep the Hadith API limited to the Hadith page; never use it to overwrite advice pages.
s=s.replace("if(rows.length)DET[0]=rows;HADITH_API_READY=true;DET[24]=rows.filter(x=>/أوص|وصي|وصية|اتقوا|عليكم|احفظوا/.test(x[0])).slice(0,120);if(!DET[24].length)DET[24]=rows.slice(0,80)", "if(rows.length)DET[0]=rows;HADITH_API_READY=true")
s=s.replace("if(n===0||n===24)ensureHadithApi();", "if(n===0)ensureHadithApi();")
s=s.replace("else if(n===22)loadDhikrBenefitsApi();else if(n===23)loadFaithPauseApi();if([6,7,8,9,10,11,13,14,15,16,18,21,22,23,24].includes(n))loadComprehensiveSnippetApis()", "else if(n===22)loadDhikrBenefitsApi();else if(n===23)loadFaithPauseApi()")
# Insert curated, section-specific content. This prevents generic Hadith rows from appearing in unrelated pages.
marker='let VIDEO_DATA=[];'
content=r'''function applyRelevantSectionContent(){
  DET[2]=[['بداية تدوين السيرة النبوية','العهد النبوي · القرآن والسنة'],['الهجرة إلى المدينة','السيرة النبوية · بناء المجتمع المسلم'],['فتح مكة','السنة الثامنة للهجرة · حدث تاريخي'],['حجة الوداع','السنة العاشرة للهجرة · خطبة جامعة']];
  DET[6]=[['إقامة الصلاة','﴿إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَوْقُوتًا﴾ · النساء 103'],['الخشوع في الصلاة','﴿قَدْ أَفْلَحَ الْمُؤْمِنُونَ ۝ الَّذِينَ هُمْ فِي صَلَاتِهِمْ خَاشِعُونَ﴾ · المؤمنون 1-2'],['الصدقة','﴿وَمَا أَنْفَقْتُمْ مِنْ شَيْءٍ فَهُوَ يُخْلِفُهُ﴾ · سبأ 39'],['الصيام','﴿لَعَلَّكُمْ تَتَّقُونَ﴾ · البقرة 183']];
  DET[8]=[['مريم بنت عمران','اصطفاها الله وطهّرها وجعلها آية للمؤمنين'],['آسية امرأة فرعون','نموذج الثبات والإيمان أمام الطغيان'],['خديجة بنت خويلد','أم المؤمنين وأول من آمن بالنبي ﷺ'],['فاطمة الزهراء','ابنة النبي ﷺ ومن أهل بيته']];
  DET[9]=[['أبو بكر الصديق','من العشرة المبشرين بالجنة'],['عمر بن الخطاب','من العشرة المبشرين بالجنة'],['عثمان بن عفان','من العشرة المبشرين بالجنة'],['علي بن أبي طالب','من العشرة المبشرين بالجنة'],['طلحة بن عبيد الله','من العشرة المبشرين بالجنة'],['الزبير بن العوام','من العشرة المبشرين بالجنة'],['عبد الرحمن بن عوف','من العشرة المبشرين بالجنة'],['سعد بن أبي وقاص','من العشرة المبشرين بالجنة'],['سعيد بن زيد','من العشرة المبشرين بالجنة'],['أبو عبيدة عامر بن الجراح','من العشرة المبشرين بالجنة']];
  DET[14]=[['مولد النبي ﷺ','بداية السيرة النبوية'],['نزول الوحي','غار حراء · بداية الرسالة'],['الدعوة في مكة','الصبر والثبات على التوحيد'],['الهجرة إلى المدينة','بناء الدولة والمجتمع المسلم'],['غزوة بدر','السنة الثانية للهجرة'],['فتح مكة','السنة الثامنة للهجرة'],['حجة الوداع','السنة العاشرة للهجرة']];
  const morning=ADHKAR_DOORS.find(d=>/الصباح والمساء/.test(d.title||''));
  if(morning) DET[15]=(morning.items||[]).map(x=>[x.text,`${x.reference||'أذكار الصباح والمساء'} · التكرار ${ar(x.repeat||1)}`]);
  DET[16]=[['الصلاة على النبي ﷺ','﴿إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ﴾ · الأحزاب 56'],['صيغة الصلاة الإبراهيمية','اللهم صل على محمد وعلى آل محمد كما صليت على إبراهيم'],['فضل الذكر والصلاة عليه','ذكرٌ مشروع بنص القرآن والسنة']];
  DET[18]=[['الصدق','﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَكُونُوا مَعَ الصَّادِقِينَ﴾ · التوبة 119'],['بر الوالدين','﴿وَبِالْوَالِدَيْنِ إِحْسَانًا﴾ · الإسراء 23'],['العفو','﴿وَلْيَعْفُوا وَلْيَصْفَحُوا﴾ · النور 22'],['التواضع','﴿وَلَا تَمْشِ فِي الْأَرْضِ مَرَحًا﴾ · الإسراء 37']];
  DET[22]=[['طمأنينة القلب','﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ · الرعد 28'],['مغفرة الذنوب','﴿وَالذَّاكِرِينَ اللَّهَ كَثِيرًا وَالذَّاكِرَاتِ أَعَدَّ اللَّهُ لَهُم مَّغْفِرَةً﴾ · الأحزاب 35'],['أذكار الصباح والمساء','ورد يومي للحفظ والطمأنينة · من حصن المسلم']];
  DET[24]=[['احفظ الله يحفظك','وصية جامعة في مراقبة الله والتوكل عليه'],['اغتنم وقتك','اغتنم صحتك وفراغك قبل الشغل والعجز'],['أحسن إلى الناس','الكلمة الطيبة والرفق من مكارم الأخلاق'],['الزم التقوى','التقوى وصية الأنبياء وطريق النجاة']];
}
function requestStartupPermissions(){
  if('Notification' in window && Notification.permission==='default') setTimeout(()=>Notification.requestPermission().catch(()=>{}),700);
  if(navigator.geolocation) setTimeout(()=>locate(),250);
}
'''
if marker not in s: raise SystemExit('VIDEO marker missing')
s=s.replace(marker,content+marker,1)
# Apply curated content after local data is available; default to the combined morning/evening door.
s=s.replace("S.az=new Array(AZK.length).fill(0);", "S.az=new Array(AZK.length).fill(0);\n    const morningIndex=ADHKAR_DOORS.findIndex(d=>/الصباح والمساء/.test(d.title||''));if(morningIndex>=0)S.adhkarDoor=morningIndex;",1)
s=s.replace("DET[10]=[['أفلا يتدبرون القرآن','القرآن كتاب هداية وتدبر'],['وفي أنفسكم أفلا تبصرون','آيات الله في خلقه']];", "DET[10]=[['أفلا يتدبرون القرآن','القرآن كتاب هداية وتدبر'],['وفي أنفسكم أفلا تبصرون','آيات الله في خلقه']];\n    applyRelevantSectionContent();",1)
# Replace the plain select with the same glass/settings visual language.
pattern=r'<select id="adhkarDoor" class="srch" style="margin-top:10px">.*?</select><div class="adhkar-player"><select id="adhkarVoice">\$\{voiceOptions\}</select>'
replacement='<div class="settings-select-row"><span>اختيار باب الذكر</span><select id="adhkarDoor" class="settings-select">${ADHKAR_DOORS.map((x,i)=>`<option value="${i}" ${i===S.adhkarDoor?\'selected\':\'\'}>${ar(i+1)} — ${x.title} (${ar((x.items||[]).length)})</option>`).join(\'\')}</select></div><div class="adhkar-player"><div class="settings-select-row"><span>صوت القارئ</span><select id="adhkarVoice" class="settings-select">${voiceOptions}</select></div>'
s,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('adhkar select not found')
# Add CSS before the first closing style tag.
css=r'''.settings-select-row{display:flex;align-items:center;gap:10px;justify-content:space-between;margin-top:10px;padding:9px 11px;border:1px solid var(--line);border-radius:14px;background:var(--soft);font-size:11px}.settings-select-row>span{color:var(--mut);white-space:nowrap}.settings-select{min-width:0;flex:1;border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--card);color:var(--text);font:inherit;outline:none}.settings-select:focus{border-color:#888;box-shadow:0 0 0 3px rgba(120,120,120,.12)}.adhkar-player{display:grid!important;gap:9px!important;padding-top:4px}.adhkar-player .pill{width:100%}'''
s=s.replace('</style>',css+'</style>',1)
# Ensure the startup routine requests both permissions rather than only relying on button clicks.
s=s.replace("updateTimeTheme();startDailyReminderLoop();loadCollectedData();", "updateTimeTheme();startDailyReminderLoop();requestStartupPermissions();loadCollectedData();",1)
p.write_text(s)
print('content, permissions, and settings-style selectors added')
