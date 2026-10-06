from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Add the new shortcut and localized labels.
s=s.replace("['عجلة يواقيت','star']];", "['عجلة يواقيت','star'],['اهتمامات المسلم','book']];", 1)
s=s.replace("SNIP_I18N.ar.push('ريلز المسلم','تعلم يواقيت','عجلة يواقيت');", "SNIP_I18N.ar.push('ريلز المسلم','تعلم يواقيت','عجلة يواقيت','اهتمامات المسلم');", 1)
s=s.replace("SNIP_I18N.en.push('Muslim Reels','Yawaqit Learning','Yawaqit Wheel');", "SNIP_I18N.en.push('Muslim Reels','Yawaqit Learning','Yawaqit Wheel','Muslim interests');", 1)
s=s.replace("SNIP_I18N.fr.push('Reels musulmans','Apprendre Yawaqit','Roue Yawaqit');", "SNIP_I18N.fr.push('Reels musulmans','Apprendre Yawaqit','Roue Yawaqit','Intérêts du musulman');", 1)
s=s.replace("SNIP_I18N.ur.push('مسلم ریلز','یواقیت سیکھیں','یواقیت وہیل');", "SNIP_I18N.ur.push('مسلم ریلز','یواقیت سیکھیں','یواقیت وہیل','مسلمان کی دلچسپیاں');", 1)
# Add local asset list immediately after the snippets.
marker="const DET={0:["
assets="const MUSLIM_INTERESTS=['01','02','03','04','05','06','07','08'].map((x,i)=>({src:`/assets/muslim-interests/${x}.jpg`,n:i+1}));\n"
if marker not in s: raise SystemExit('DET marker not found')
s=s.replace(marker,assets+marker,1)
# Add swipe gallery renderer before the detail renderer.
marker="det(){const n=S.sub;"
gallery="""muslimInterests(){return `<div class=\"card hd muslim-interests-head\"><div class=\"row\" style=\"direction:rtl;justify-content:space-between\"><b style=\"font-size:17px\">${SL(28,'اهتمامات المسلم')}</b><button id=\"bk\" class=\"ib\">${I('back')}</button></div><p class=\"mut\" style=\"text-align:center;margin-top:6px\">اسحب الصورة يمينًا أو يسارًا للتنقل بين الصور</p></div><div class=\"muslim-interest-gallery\" id=\"interestGallery\">${MUSLIM_INTERESTS.map((x,i)=>`<figure class=\"interest-slide\"><img src=\"${x.src}\" alt=\"اهتمامات المسلم ${ar(x.n)}\" loading=\"${i<2?'eager':'lazy'}\" decoding=\"async\"><figcaption>${ar(x.n)} / ${ar(MUSLIM_INTERESTS.length)}</figcaption></figure>`).join('')}</div><div class=\"interest-controls\"><button class=\"ib\" data-interest-prev aria-label=\"الصورة السابقة\">${I('back','transform:scaleX(-1)')}</button><span>اسحب للتنقل</span><button class=\"ib\" data-interest-next aria-label=\"الصورة التالية\">${I('back')}</button></div><div class=\"interest-source\">المصدر: Pinterest · تم حفظ الصور محليًا لتظهر بسرعة</div>`},
 """
if marker not in s: raise SystemExit('det renderer marker not found')
s=s.replace(marker,gallery+marker,1)
# Route item 28 before the normal detail page.
s=s.replace("det(){const n=S.sub;if(n===25)return reelsPage();if(n===26)return learnPage();if(n===27)return wheelPage();", "det(){const n=S.sub;if(n===25)return reelsPage();if(n===26)return learnPage();if(n===27)return wheelPage();if(n===28)return scr.muslimInterests();", 1)
# Bind arrow buttons after detail/search bindings are set up.
needle="A('[data-n]',e=>{const n=+e.dataset.n;"
insert="""const gallery=document.querySelector('#interestGallery');if(gallery){document.querySelector('[data-interest-prev]')?.addEventListener('click',()=>gallery.scrollBy({left:-gallery.clientWidth,behavior:'smooth'}));document.querySelector('[data-interest-next]')?.addEventListener('click',()=>gallery.scrollBy({left:gallery.clientWidth,behavior:'smooth'}))}
  """
if needle not in s: raise SystemExit('bind anchor not found')
s=s.replace(needle,insert+needle,1)
css=""".muslim-interest-gallery{display:flex;gap:12px;width:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;direction:ltr;padding:0 2px 8px}.muslim-interest-gallery::-webkit-scrollbar{display:none}.interest-slide{position:relative;flex:0 0 100%;height:min(68dvh,560px);margin:0;display:flex;align-items:center;justify-content:center;scroll-snap-align:center;overflow:hidden;border-radius:20px;background:var(--card);border:1px solid var(--line);box-shadow:0 10px 26px rgba(0,0,0,.12)}.interest-slide img{display:block;width:100%;height:100%;object-fit:contain;background:var(--card)}.interest-slide figcaption{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);padding:4px 10px;border-radius:999px;background:rgba(0,0,0,.58);color:#fff;font-size:10px;direction:rtl}.interest-controls{display:flex;align-items:center;justify-content:center;gap:16px;margin:8px 0;color:var(--mut);font-size:10px}.interest-controls .ib{width:34px;height:34px;border:1px solid var(--line);border-radius:50%;background:var(--soft)}.interest-source{text-align:center;color:var(--mut);font-size:9px;margin:4px 0 12px}"""
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('muslim interests swipe gallery added')
