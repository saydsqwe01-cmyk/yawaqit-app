from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
repls={
'loadSignsApi':r'''async function loadSignsApi(){if(SIGNS_API_READY)return;SIGNS_API_READY=true;try{const books=['bukhari','muslim','tirmidhi'];const packs=await Promise.all(books.map(b=>fetch(`https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-${b}.json`).then(x=>x.json()).catch(()=>({hadiths:[]}))));const rows=packs.flatMap(d=>d.hadiths||[]).map(x=>({x,t:normalizeSearch(x.text||x.hadithArabic||'')})).filter(o=>/دجال|ساعه|فتن|مهدي|دخان|دابه|طلوع الشمس|خسف|ياجوج|ماجوج/.test(o.t)).map(o=>[o.x.text||o.x.hadithArabic||'','حديث عن علامات الساعة · '+(o.x.reference||'مصدر الحديث')]);if(rows.length)DET[3]=rows.slice(0,300);render()}catch(e){}}''',
'loadQuranDuasApi':r'''async function loadQuranDuasApi(){if(DUAS_API_READY)return;DUAS_API_READY=true;try{const ids=[2,3,5,7,14,20,21,23,25,28,40,59,66,71,113,114];const packs=await Promise.all(ids.map(n=>fetch(`https://api.alquran.cloud/v1/surah/${n}/quran-uthmani`).then(x=>x.json()).catch(()=>null)));const rows=packs.flatMap(d=>(d?.data?.ayahs||[]).filter(a=>{const t=normalizeSearch(a.text||'');return /ربنا|ربي|رب|اللهم|اغفر|اهدنا|ارحم|توفنا|اجعلنا|اتنا|اصلح/.test(t)}).map(a=>[a.text,`دعاء قرآني · ${d.data.name} · الآية ${a.numberInSurah}`]));if(rows.length)DET[7]=rows.slice(0,300);render()}catch(e){}}''',
'loadDhikrBenefitsApi':r'''async function loadDhikrBenefitsApi(){if(DHIKR_API_READY)return;DHIKR_API_READY=true;try{const books=['bukhari','muslim','abudawud','tirmidhi'];const packs=await Promise.all(books.map(b=>fetch(`https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-${b}.json`).then(x=>x.json()).catch(()=>({hadiths:[]}))));const rows=packs.flatMap(d=>d.hadiths||[]).map(x=>({x,t:normalizeSearch(x.text||x.hadithArabic||'')})).filter(o=>/ذكر|اذكر|يسبح|سبح|حمد|استغفر|تهليل|تسبيح|صلاه على النبي/.test(o.t)).map(o=>[o.x.text||o.x.hadithArabic||'',`فوائد الذكر · ${o.x.reference||'مصدر الحديث'}`]);if(rows.length)DET[22]=rows.slice(0,180);render()}catch(e){}}'''
}
for name,new in repls.items():
    pat=rf'async function {name}\(\)\{{[^\n]*'
    s,n=re.subn(pat,new,s)
    print(name,n)
p.write_text(s)
