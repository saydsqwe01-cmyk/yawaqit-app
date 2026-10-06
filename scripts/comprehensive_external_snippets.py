from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Replace the three-dot markup with twenty orbiting dots.
old=re.search(r'<div id="loadingScreen"[^>]*>.*?</div></div></div>',s)
if not old: raise SystemExit('loading markup missing')
dots=''.join(f'<i style="--i:{i}"></i>' for i in range(20))
new=f'<div id="loadingScreen" role="status" aria-live="polite"><div class="loading-inner"><img class="loading-mosque" src="/assets/loading-mosque.png" alt=""><div class="loading-copy">جاري التحميل</div><div class="loading-orbit" aria-hidden="true">{dots}</div></div></div>'
s=s[:old.start()]+new+s[old.end():]
# Slow the orbit and force a uniformly distributed twenty-dot palette/delay.
s=s.replace('animation:loadingOrbit 2.1s linear infinite','animation:loadingOrbit 4.2s linear infinite',1)
s=s.replace('</style>','.loading-orbit i:nth-child(n){animation-delay:calc(var(--i)*-.21s);background:hsl(calc(var(--i)*18deg) 72% 55%)}\n</style>',1)
# Comprehensive corpus loader for all remaining content-heavy snippets.
marker='function swipeTabs()'
block=r'''
let COMPREHENSIVE_SNIPPETS_READY=false,COMPREHENSIVE_SNIPPETS_LOADING=false;
async function loadComprehensiveSnippetApis(){
 if(COMPREHENSIVE_SNIPPETS_READY||COMPREHENSIVE_SNIPPETS_LOADING)return;
 COMPREHENSIVE_SNIPPETS_LOADING=true;render();
 try{
  const books=['bukhari','muslim','abudawud','tirmidhi'];
  const packs=await Promise.all(books.map(b=>fetch(`https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-${b}.json`).then(x=>x.json()).catch(()=>({hadiths:[]}))));
  const hadiths=packs.flatMap(d=>d.hadiths||[]).map(x=>({x,t:normalizeSearch(x.text||x.hadithArabic||'')})).filter(o=>o.t);
  const pick=(rx,limit=180)=>hadiths.filter(o=>rx.test(o.t)).slice(0,limit).map(o=>[o.x.text||o.x.hadithArabic||'',`مصدر خارجي موثوق · ${o.x.reference||'حديث'}`]);
  const put=(n,rows)=>{if(rows.length)DET[n]=rows};
  put(6,pick(/صلاه|صلاه|زكاه|صوم|حج|صدقه|عمل صالح|اجر|عباد/));
  put(8,pick(/نساء|امراه|مريم|عائشه|فاطمه|خديجه|اسيا|زوج/));
  put(9,pick(/ابو بكر|عمر بن|عثمان بن|علي بن|العشره|الجنه/));
  put(14,pick(/نبي|رسول|هجره|غزوه|مكه|مدينه|سيره|بعثه/));
  put(15,pick(/دعاء|اللهم|اعوذ|ربنا|استغفر|مساء|صبح/));
  put(16,pick(/صل على النبي|صلوا علي|يصلي علي|الصلاه على النبي/));
  put(18,pick(/خلق|رحمه|رحم|صدق|غضب|تواضع|رفق|احسان|كذب/));
  put(22,pick(/ذكر|اذكر|يسبح|سبح|حمد|استغفر|تهليل|تسبيح/));
  put(24,pick(/وصي|عليكم|اتقوا|احفظوا|نصيحه/));
  const ids=[2,3,12,13,16,17,18,19,20,21,23,24,25,26,28,31,36,39,41,49,55,56,57,59,61,65,67,75,76,78,79,80,81,82,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114];
  const qpacks=await Promise.all(ids.map(n=>fetch(`https://api.alquran.cloud/v1/surah/${n}/quran-uthmani`).then(x=>x.json()).catch(()=>null)));
  const verses=qpacks.flatMap(d=>(d?.data?.ayahs||[]).map(a=>({a,s:d.data.name})));
  const qpick=(rx,limit=220)=>verses.filter(o=>rx.test(normalizeSearch(o.a.text||''))).slice(0,limit).map(o=>[o.a.text,`القرآن الكريم · ${o.s} · الآية ${o.a.numberInSurah}`]);
  put(7,qpick(/ربنا|ربي|رب|اغفر|اهدنا|ارحم|توفنا|اجعلنا|اتنا|اصلح/));
  put(10,qpick(/خلق|سماء|ارض|بحر|ليل|نهار|انسان|انعام|افاق|انفس/));
  put(11,qpick(/هدى|رحمه|صبر|تقوى|تذكر|يتفكر|يعقل|بشرى|موعظه/));
  put(13,qpick(/قران|كتاب|ايات|يتلو|تدبر|ذكر/));
  put(21,qpick(/يتدبر|تفكر|يتفكر|ذكرى|بصيره|يعقل|اولي الالباب/));
  put(23,qpick(/يسر|رحمه|صبر|توكل|فرج|لا تقنط|مخرج|حسبه/));
  COMPREHENSIVE_SNIPPETS_READY=true;
 }catch(e){}
 COMPREHENSIVE_SNIPPETS_LOADING=false;render();
}
'''
if marker not in s: raise SystemExit('swipe marker missing')
s=s.replace(marker,block+marker,1)
# Ensure each content section triggers the shared external load; existing specialized loaders remain in place.
old='function loadSectionApi(n){if(n===2)loadHistoryApi();else if(n===3)loadSignsApi();else if(n===4)loadRuqyahApi();else if(n===7)loadQuranDuasApi();else if(n===12)loadQuizApi();else if(n===17)loadProphetStoriesApi();else if(n===22)loadDhikrBenefitsApi();else if(n===23)loadFaithPauseApi()}'
new='function loadSectionApi(n){if(n===2)loadHistoryApi();else if(n===3)loadSignsApi();else if(n===4)loadRuqyahApi();else if(n===7)loadQuranDuasApi();else if(n===12)loadQuizApi();else if(n===17)loadProphetStoriesApi();else if(n===22)loadDhikrBenefitsApi();else if(n===23)loadFaithPauseApi();if([6,7,8,9,10,11,13,14,15,16,18,21,22,23,24].includes(n))loadComprehensiveSnippetApis()}'
if old not in s: raise SystemExit('loadSectionApi exact text missing')
s=s.replace(old,new,1)
# Show a section-level loading notice while the shared API corpus is being fetched.
s=s.replace("${(SECTION_API_LOADING||FAITH_PAUSE_API_LOADING)&&[2,3,4,23].includes(n)?", "${(SECTION_API_LOADING||FAITH_PAUSE_API_LOADING||COMPREHENSIVE_SNIPPETS_LOADING)&&[2,3,4,6,7,8,9,10,11,13,14,15,16,18,21,22,23,24].includes(n)?")
p.write_text(s)
print('comprehensive external snippet loader and 20-dot loader applied')
