from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Add a real reels screen; the router already points to reelsPage(), but the function was missing.
marker='function transferCard(name,i,compact=false)'
reels=r'''function reelsPage(){return `<div class="card hd"><div class="row" style="direction:rtl;justify-content:space-between"><b style="font-size:16px">${U('reels')}</b><button id="bk" class="ib">${I('back')}</button></div><p class="mut" style="text-align:center">${U('reelsDesc')}</p><a class="transfer-open" style="display:block;text-align:center;margin:8px auto;max-width:220px" href="${TRANSFER_SOURCE}" target="_blank" rel="noopener noreferrer">${U('openTransfer')}</a></div><div class="transfer-list">${TRANSFER_REELS.map((name,i)=>transferCard(name,i)).join('')}</div>`}
'''
if marker not in s: raise SystemExit('transferCard marker missing')
s=s.replace(marker,reels+marker,1)
# Add API loaders for Quran duas and dhikr benefits.
marker2='async function loadSectionApi(n)'
extra=r'''
let DUAS_API_READY=false,DHIKR_API_READY=false;
async function loadQuranDuasApi(){if(DUAS_API_READY)return;DUAS_API_READY=true;try{const ids=[2,3,5,7,14,20,21,23,25,28,40,59,66,71,113,114];const packs=await Promise.all(ids.map(n=>fetch(`https://api.alquran.cloud/v1/surah/${n}/quran-uthmani`).then(x=>x.json()).catch(()=>null)));const rows=packs.flatMap(d=>(d?.data?.ayahs||[]).filter(a=>/رَبَّنَا|رَبِّ|رَبَّ|اللَّهُمَّ|اغْفِرْ|اهْدِنَا|ارْحَمْنَا|تَوَفَّنَا/.test(a.text||'')).map(a=>[a.text,`دعاء قرآني · ${d.data.name} · الآية ${a.numberInSurah}`]));if(rows.length)DET[7]=rows;render()}catch(e){}}
async function loadDhikrBenefitsApi(){if(DHIKR_API_READY)return;DHIKR_API_READY=true;try{const books=['bukhari','muslim','abudawud','tirmidhi'];const packs=await Promise.all(books.map(b=>fetch(`https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-${b}.json`).then(x=>x.json()).catch(()=>({hadiths:[]}))));const rows=packs.flatMap(d=>d.hadiths||[]).filter(x=>/(الذكر|يذكر|اذكر|سبحان|الحمد|استغفر|التسبيح|التهليل|ذكر الله)/.test(x.text||x.hadithArabic||'')).map(x=>[x.text||x.hadithArabic||'',`فوائد الذكر · ${x.reference||'حديث'}`]);if(rows.length)DET[22]=rows.slice(0,180);render()}catch(e){}}
'''
if marker2 not in s: raise SystemExit('loadSectionApi marker missing')
s=s.replace(marker2,extra+marker2,1)
old="async function loadSectionApi(n){if(n===2)loadHistoryApi();else if(n===3)loadSignsApi();else if(n===4)loadRuqyahApi();else if(n===12)loadQuizApi();else if(n===17)loadProphetStoriesApi();else if(n===23)loadFaithPauseApi()}"
new="async function loadSectionApi(n){if(n===2)loadHistoryApi();else if(n===3)loadSignsApi();else if(n===4)loadRuqyahApi();else if(n===7)loadQuranDuasApi();else if(n===12)loadQuizApi();else if(n===17)loadProphetStoriesApi();else if(n===22)loadDhikrBenefitsApi();else if(n===23)loadFaithPauseApi()}"
if old not in s: raise SystemExit('loadSectionApi exact pattern missing')
s=s.replace(old,new,1)
p.write_text(s)
print('external section loaders and reels page applied')
