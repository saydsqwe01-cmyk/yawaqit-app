from pathlib import Path

p=Path('/home/ubuntu/yawaqit/index.html')
s=p.read_text(encoding='utf-8')

# Add a richer set of selectable dhikr phrases and a reusable tap action.
s=s.replace("let tasbeehCount=0;", "let tasbeehCount=0,tasbeehPhraseIndex=0;\nconst TASBEEH_PHRASES=['سُبْحَانَ اللَّهِ وَبِحَمْدِهِ','الْحَمْدُ لِلَّهِ','اللَّهُ أَكْبَرُ','لَا إِلَهَ إِلَّا اللَّهُ','أَسْتَغْفِرُ اللَّهَ','لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ','حَسْبِيَ اللَّهُ وَنِعْمَ الْوَكِيلُ','اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّد'];", 1)
old_sound="function soundTap(kind){if(kind==='nav'){playTap(320,.09,.05);setTimeout(()=>playTap(480,.07,.035),40)}else if(kind==='sheet'){playTap(430,.07,.04)}else if(kind==='audio'){playTap(560,.05,.045)}else if(kind==='wrong'){playTap(180,.12,.06);setTimeout(()=>playTap(120,.14,.04),55)}else if(kind==='correct'){playTap(620,.08,.05);setTimeout(()=>playTap(820,.12,.04),55)}else{playTap(420,.055,.04)}}"
assert old_sound in s
new_sound=old_sound+"\nfunction tapTasbeeh(){tasbeehCount++;try{soundTap('audio')}catch(_){};const c=document.querySelector('#tasbeehCount');if(c)c.textContent=ar(tasbeehCount);const orb=document.querySelector('.tasbeeh-orb');orb?.classList.add('tap');setTimeout(()=>orb?.classList.remove('tap'),220)}"
s=s.replace(old_sound,new_sound,1)

# Replace the circular control and select with the supplied image as the control and a draggable range.
old_tas="<div class=\"tasbeeh-orb\"><img class=\"tasbeeh-device\" src=\"/assets/tasbeeh-device.png\" alt=\"سبحة إلكترونية\"><div class=\"tasbeeh-count\" id=\"tasbeehCount\">${ar(tasbeehCount)}</div><div class=\"tasbeeh-label\">تسبيحة</div></div><select id=\"tasbeehPhrase\" class=\"srch\"><option value=\"سُبْحَانَ اللَّهِ وَبِحَمْدِهِ\">سُبْحَانَ اللَّهِ وَبِحَمْدِهِ</option><option value=\"الْحَمْدُ لِلَّهِ\">الْحَمْدُ لِلَّهِ</option><option value=\"اللَّهُ أَكْبَرُ\">اللَّهُ أَكْبَرُ</option><option value=\"لَا إِلَهَ إِلَّا اللَّهُ\">لَا إِلَهَ إِلَّا اللَّهُ</option><option value=\"أَسْتَغْفِرُ اللَّهَ\">أَسْتَغْفِرُ اللَّهَ</option></select><div class=\"tasbeeh-actions\"><button id=\"tasbeehTap\" class=\"tasbeeh-tap\">${I('star')}<span>اضغط للتسبيح</span></button><button id=\"tasbeehReset\" class=\"pill\">تصفير العداد</button></div><div class=\"tasbeeh-phrase\" id=\"tasbeehPhraseText\">سُبْحَانَ اللَّهِ وَبِحَمْدِهِ</div>"
new_tas="<div class=\"tasbeeh-orb\"><img class=\"tasbeeh-device\" id=\"tasbeehDevice\" src=\"/assets/tasbeeh-device.png\" alt=\"اضغط على السبحة الإلكترونية للتسبيح\" role=\"button\" tabindex=\"0\"><div class=\"tasbeeh-count\" id=\"tasbeehCount\">${ar(tasbeehCount)}</div><div class=\"tasbeeh-label\">اضغط على الصورة للتسبيح</div></div><div class=\"tasbeeh-range-wrap\"><label for=\"tasbeehPhraseRange\">اسحب الشريط لاختيار الذكر</label><input id=\"tasbeehPhraseRange\" class=\"tasbeeh-range\" type=\"range\" min=\"0\" max=\"${TASBEEH_PHRASES.length-1}\" value=\"${tasbeehPhraseIndex}\" step=\"1\"><div class=\"tasbeeh-range-value\" id=\"tasbeehPhraseText\">${TASBEEH_PHRASES[tasbeehPhraseIndex]}</div></div><div class=\"tasbeeh-actions\"><button id=\"tasbeehReset\" class=\"pill\">تصفير العداد</button></div>"
assert old_tas in s
s=s.replace(old_tas,new_tas,1)

# Add the missing Quran list renderer before the Quran reading renderer.
needle="quran(){if(S.quranList)return scr.quranList();const s=SUR[S.surah];"
assert needle in s
quran_list="""quranList(){const q=normalizeSearch(S.quranQ||'');const rows=SUR.map((s,i)=>[s,i]).filter(([s])=>!q||matchesSearch(`${s.n} ${s.e||''}`,q));return `<div class=\"card hd\"><div class=\"ttl\"><span>المصحف الشريف</span><span class=\"quran-index\">${ar(SUR.length)} سورة</span></div><input id=\"quranSearch\" class=\"srch\" placeholder=\"ابحث باسم السورة\" value=\"${String(S.quranQ||'').replace(/\"/g,'&quot;')}\"><div class=\"surah-list\">${rows.map(([s,i])=>`<button class=\"surah-choice\" data-surah=\"${i}\"><span class=\"surah-num\">${ar(i+1)}</span><span class=\"surah-name\"><b>${s.n}</b><small>${s.e||''} · ${s.t||''} · ${ar(s.v?.length||0)} آية</small></span><span class=\"surah-open\">${I('exp')}</span></button>`).join('')}</div></div>`},
 """
s=s.replace(needle,quran_list+needle,1)

# Replace old select/button bindings with image tap and slider bindings.
old_bind="A('#tasbeehPhrase',e=>{const t=document.querySelector('#tasbeehPhraseText');if(t)t.textContent=e.target.value});A('#tasbeehTap',()=>{tasbeehCount++;try{soundTap()}catch(_){};const c=document.querySelector('#tasbeehCount');if(c)c.textContent=ar(tasbeehCount);document.querySelector('.tasbeeh-orb')?.classList.add('tap');setTimeout(()=>document.querySelector('.tasbeeh-orb')?.classList.remove('tap'),220)});A('#tasbeehReset',()=>{tasbeehCount=0;render()});"
new_bind="A('#tasbeehDevice',()=>tapTasbeeh());document.querySelector('#tasbeehDevice')?.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();tapTasbeeh()}});const phraseRange=document.querySelector('#tasbeehPhraseRange');if(phraseRange)phraseRange.oninput=e=>{tasbeehPhraseIndex=+e.target.value;const t=document.querySelector('#tasbeehPhraseText');if(t)t.textContent=TASBEEH_PHRASES[tasbeehPhraseIndex]||TASBEEH_PHRASES[0]};A('#tasbeehReset',()=>{tasbeehCount=0;render()});"
assert old_bind in s
s=s.replace(old_bind,new_bind,1)

# Keep Quran search state while typing.
needle2="const qsearch=$('#quranSearch');if(qsearch)qsearch.oninput=e=>{S.quranQ=e.target.value;render()};"
assert needle2 in s

# Override old circle styling: the image is the only visual control.
css=""".tasbeeh-orb{width:auto;height:auto;margin:18px auto 10px;border:0;border-radius:0;background:none;box-shadow:none;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:transform .2s}.tasbeeh-orb.tap .tasbeeh-device{transform:scale(.93) rotate(-8deg)}.tasbeeh-device{position:relative;right:auto;bottom:auto;width:min(68vw,210px);height:auto;aspect-ratio:627/680;object-fit:contain;transform:rotate(-8deg);cursor:pointer;filter:drop-shadow(0 10px 14px rgba(0,0,0,.7));outline:none}.tasbeeh-device:focus-visible{filter:drop-shadow(0 10px 14px rgba(79,179,236,.75))}.tasbeeh-range-wrap{margin:12px auto 8px;max-width:340px}.tasbeeh-range-wrap label{display:block;color:#aaa;font-size:10px;margin-bottom:7px}.tasbeeh-range{width:100%;accent-color:#4fb3ec;direction:rtl}.tasbeeh-range-value{min-height:28px;margin-top:7px;color:#eee;font-family:Amiri,serif;font-size:17px}.tasbeeh-actions{margin-top:8px}.tasbeeh-tap{display:none!important}
"""
s=s.replace('</style>',css+'</style>',1)

p.write_text(s,encoding='utf-8')
print('tasbeeh_quran_fixed')
