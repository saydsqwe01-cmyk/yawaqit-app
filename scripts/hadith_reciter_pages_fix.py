from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# The general hadith page should contain only the two canonical Sahih collections.
s=s.replace("const books=['bukhari','muslim','tirmidhi','abudawud'];const packs=await Promise.all(books.map(b=>fetch(`https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-${b}.json`)", "const books=['bukhari','muslim'];const packs=await Promise.all(books.map(b=>fetch(`https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-${b}.json`)",1)
# Add clear source notes so the two pages cannot be confused.
old='<b style="font-size:16px">${SNIP[n][0]}</b><button id="bk" class="ib">${I(\'back\')}</button>'
new='<b style="font-size:16px">${SNIP[n][0]}</b>${n===0?\'<small class="page-note">أحاديث صحيحة من صحيح البخاري وصحيح مسلم</small>\':n===9?\'<small class="page-note">أسماء العشرة المبشرين بالجنة</small>\':\'\'}<button id="bk" class="ib">${I(\'back\')}</button>'
if old not in s: raise SystemExit('detail header not found')
s=s.replace(old,new,1)
# Replace the generic list-sheet renderer with a reciter-aware version. Other sheets stay unchanged.
oldfn="""function listSheet(title,items,fn){
  const draw=q=>items.filter(x=>matchesSearch(x,q)).map((x,i)=>`<button class=\"li\" data-i=\"${items.indexOf(x)}\">${x}</button>`).join('');
  sheet(`<h3>${title}</h3><div style=\"position:relative\"><input class=\"srch\" placeholder=\"${T('search')}\" id=\"q\"></div><div id=\"ls\">${draw('')}</div>`);
  const bind=()=>$('#ls').querySelectorAll('.li').forEach(b=>b.onclick=()=>{fn(+b.dataset.i);closeSheet()});
  bind();$('#q').oninput=e=>{$('#ls').innerHTML=draw(e.target.value);bind()};
}"""
newfn="""function listSheet(title,items,fn){
  const isReciter=/قارئ|شيخ|reciter|reader/i.test(String(title));
  const draw=q=>items.filter(x=>matchesSearch(x,q)).map(x=>{const i=items.indexOf(x),r=isReciter?RECITERS[i]:null,src=r?.image_local||r?.image_url||'/assets/logo.png';return `<button class=\"li ${isReciter?'reciter-option':''}\" data-i=\"${i}\">${isReciter?`<img src=\"${src}\" alt=\"\" onerror=\"this.onerror=null;this.src='/assets/logo.png'\">`:''}<span>${x}</span></button>`}).join('');
  sheet(`<h3>${title}</h3><div style=\"position:relative\"><input class=\"srch\" placeholder=\"${T('search')}\" id=\"q\"></div><div id=\"ls\">${draw('')}</div>`);
  const bind=()=>$('#ls').querySelectorAll('.li').forEach(b=>b.onclick=()=>{fn(+b.dataset.i);closeSheet()});
  bind();$('#q').oninput=e=>{$('#ls').innerHTML=draw(e.target.value);bind()};
}"""
if oldfn not in s: raise SystemExit('listSheet function not found')
s=s.replace(oldfn,newfn,1)
css=""".page-note{display:block;width:100%;margin-top:4px;color:var(--mut);font-size:10px;font-weight:400}.reciter-option{display:flex!important;align-items:center;gap:10px;text-align:start!important;min-height:54px!important}.reciter-option img{width:38px;height:38px;flex:0 0 38px;border-radius:50%;object-fit:cover;background:var(--soft);border:1px solid var(--line)}.reciter-option span{flex:1}"""
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('hadith/ten pages separated and reciter portraits added')
