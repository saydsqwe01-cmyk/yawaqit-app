from pathlib import Path

project = Path('/home/ubuntu/yawaqit')
source = Path('/home/ubuntu/upload/يَوَاقِيت.html')
html = source.read_text(encoding='utf-8')

# Keep the supplied file's markup and styling. Only make its static collections replaceable.
html = html.replace('const SUR=[', 'let SUR=[', 1)
html = html.replace('const AZK=', 'let AZK=', 1)
html = html.replace('const RC=', 'let RC=', 1)
html = html.replace('const AUD=', 'let AUD=', 1)

integration = r'''
// Connected data layer — the supplied UI remains the source of layout and interactions.
let RECITERS=[];
let HADITH_PREVIEW=[];
let ADHKAR_DOORS=[];
const audioEl=new Audio();
audioEl.preload='metadata';
function selectedReciter(){return RECITERS[S.rc]||RECITERS[0]||null}
function recitationUrl(i){const r=selectedReciter(),m=r&&r.moshaf&&r.moshaf[0];return m?`${m.server}${String(i+1).padStart(3,'0')}.mp3`:''}
function stopAudio(){audioEl.pause();audioEl.currentTime=0;S.ap=null;S.all=false;S.vp=-1}
function playRecitation(i){const url=recitationUrl(i);if(!url)return;if(audioEl.src===url&&!audioEl.paused){audioEl.pause();S.ap=null;S.all=false;S.vp=-1;render();return}audioEl.src=url;audioEl.playbackRate=SPD[S.spd]||1;audioEl.load();S.ap=i;audioEl.play().catch(()=>{});render()}
audioEl.onended=()=>{S.ap=null;S.all=false;S.vp=-1;render()}
async function loadCollectedData(){
  try{
    const [q,r,a,h]=await Promise.all([
      fetch('/data/quran/quran_uthmani_full.json').then(x=>x.json()),
      fetch('/data/reciters/reciters_featured.json').then(x=>x.json()),
      fetch('/data/adhkar/adhkar_full_ar.json').then(x=>x.json()),
      fetch('/data/hadith/featured.json').then(x=>x.json())
    ]);
    SUR=(q.surahs||[]).map(s=>({n:s.name.replace(/^سُورَةُ\s*/,'').trim(),e:s.englishName,t:s.revelationType==='Meccan'?'مكية':'مدنية',v:(s.ayahs||[]).map(v=>[String(v.text||'').replace(/^\uFEFF/,''),'',''])}));
    RECITERS=r.reciters||[];
    RC=RECITERS.map(x=>x.name);
    AUD=SUR.map(x=>x.n);
    ADHKAR_DOORS=a.doors||[];
    AZK=ADHKAR_DOORS.flatMap(d=>d.items||[]).slice(0,4).map(x=>String(x.text||'').replace(/[()]/g,''));
    if(!AZK.length)AZK=['سبحان الله وبحمده','الحمد لله','لا إله إلا الله','الله أكبر'];
    S.az=new Array(AZK.length).fill(0);
    HADITH_PREVIEW=h.hadiths||[];
    DET[0]=HADITH_PREVIEW.slice(0,4).map(x=>[`«${x.text}»`,'صحيح البخاري']);
    DET[1]=ADHKAR_DOORS.slice(0,1).flatMap(d=>(d.items||[]).slice(0,4).map(x=>[x.text,'حصن المسلم']));
    // The original screen has translation/tafsir switches; keep them off until a source is selected.
    S.tr=false;S.tf=false;
    render(true);
  }catch(e){console.warn('Yawaqit data load failed',e)}
}
'''
needle = 'const p2=n=>String(n).padStart(2,\'0\');'
if needle not in html:
    raise SystemExit('Could not find integration anchor')
html = html.replace(needle, integration + '\n' + needle, 1)

html = html.replace("A('[data-a]',e=>{const i=+e.dataset.a;S.ap=S.ap===i?null:i;render()});", "A('[data-a]',e=>{const i=+e.dataset.a;if(S.ap===i){stopAudio();render()}else playRecitation(i)});")
html = html.replace("A('[data-p]',e=>{const i=+e.dataset.p;S.all=false;S.vp=S.vp===i?-1:i;render()});", "A('[data-p]',e=>{const i=+e.dataset.p;S.all=false;S.vp=S.vp===i?-1:i;if(S.vp>=0)playRecitation(S.surah);else stopAudio();render()});")
html = html.replace("A('#pa',()=>{S.all=!S.all;S.vp=S.all?0:-1;render()});", "A('#pa',()=>{S.all=!S.all;S.vp=S.all?0:-1;if(S.all)playRecitation(S.surah);else{stopAudio();render()}});")
html = html.replace('render(true);\n</script>', 'render(true);\nloadCollectedData();\n</script>', 1)

# Original mobile canvas requested by the user; the source already contains this rule.
project.joinpath('index.html').write_text(html, encoding='utf-8')
print('restored supplied UI with connected data layer')
