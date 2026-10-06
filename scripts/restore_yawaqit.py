from pathlib import Path
import re
p=Path('/home/ubuntu/work/index.html')
s=p.read_text()
# Restore brand identity.
s=s.replace('<span class="brand-name">موسوعة المسلم</span>','<span class="brand-name">يَوَاقِيت</span>')
s=s.replace('<meta name="apple-mobile-web-app-title" content="موسوعة المسلم">','<meta name="apple-mobile-web-app-title" content="يَوَاقِيت">')
# Restore the first prayer-banner homepage.
old_home=r'''home(){const pr=prayers(),dt=dates();S.np=pr.n;
 return `<div class="card hd prayer-banner"><div class="pb-sky"><span class="pb-grid">${I('cc')}</span><div class="pb-badge">${I('star')}<span>${pr.n} ${S.lang==='en'?'next':S.lang==='fr'?'prochaine':S.lang==='ur'?'بعد':'بعد'}</span></div><div id="cd" class="pb-count">${pr.cd}</div><div class="pb-loc"><span>${S.geoReady?(S.geoName||(S.lang==='en'?'Your location':S.lang==='fr'?'Votre position':S.lang==='ur'?'آپ کا مقام':'موقعك الحالي')):(S.lang==='en'?'Locating...':S.lang==='fr'?'Localisation...':S.lang==='ur'?'مقام تلاش ہو رہا ہے...':'جارٍ تحديد موقعك...')}</span>${I('pin')}</div><div class="pb-orbit"><i class="sun"></i><i class="earth"></i></div><div class="mosque"><svg viewBox="0 0 346 74" preserveAspectRatio="none"><path d="M0 74V52h22V38h6V22l3-4 3 4v16h6v14h26V46c0-11 8-19 19-22V16l-3-3 3-3 3 3-3 3v8c11 3 19 11 19 22v6h30V44h10V28l3-4 3 4v16h10v14h24V42h8V26l3-4 3 4v16h8v16h28V46c0-11 8-19 19-22V16l-3-3 3-3 3 3-3 3v8c11 3 19 11 19 22v6h30V44h10V28l3-4 3 4v16h10v14h20v22z" fill="#050505"/><g fill="#f6b93b" opacity=".55"><rect x="24" y="44" width="4" height="8" rx="2"/><rect x="96" y="58" width="6" height="10" rx="3"/><rect x="104" y="58" width="6" height="10" rx="3"/><rect x="160" y="50" width="4" height="8" rx="2"/><rect x="228" y="58" width="6" height="10" rx="3"/><rect x="236" y="58" width="6" height="10" rx="3"/><rect x="292" y="50" width="4" height="8" rx="2"/></g></svg></div></div>
 <div class="pb-sub">${L('prev')}: <b style="color:#fff">${pr.prev.n}</b> · ${agoText(pr.prev.ago)}</div><div class="pt">${PR.map((p,i)=>`<div class="${i===pr.i?'on':''}"><small>${PL(p[0])}</small><b>${ar(p2(p[1]>12?p[1]-12:p[1]))}:${ar(p2(p[2]))}</b></div>`).join('')}</div><small class="mut" style="font-size:8.5px;display:block;text-align:center;margin-top:8px">${S.geoReady?(S.lang==='en'?'Accurate prayer times':S.lang==='fr'?'Horaires précis':S.lang==='ur'?'درست نماز کے اوقات':'مواقيت دقيقة بحسب موقعك'):(S.lang==='en'?'Approximate times':S.lang==='fr'?'Horaires approximatifs':S.lang==='ur'?'تقریبی اوقات':'المواقيت تقريبية')}<button id="loc">${L('location')}</button></small></div>
 <div class="grid sm">${[[T('quiz'),null,'quiz'],[L('quran'),'book','quran'],[L('vid'),'film','vid'],[L('aud'),'head','aud']].map(([l,ic,t])=>`<button class="tile" data-go="${t}">${ic?I(ic):'<span class="q">؟</span>'}${l}</button>`).join('')}</div>
 <div class="pb-dates">${dt[0]} · ${dt[1]}</div>
 <div class="sec">${L('daily')}</div><div class="card" style="text-align:center"><div class="verse">«${(DAILY_COPY[S.lang]||DAILY_COPY.ar)[0]}»</div><div class="ref">${(DAILY_COPY[S.lang]||DAILY_COPY.ar)[1]}</div></div>
 <div class="sec">${T('dailyVerse')}</div><div class="card" style="text-align:center"><div class="verse">﴿فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًا﴾</div><div class="ref">${T('about')}</div></div>`},
 vid('''
s=re.sub(r"home\(\)\{[\s\S]*?\},\n vid\(",old_home,s,count=1)
# Restore the original wide phone canvas and its original header/nav proportions, while allowing full width on every device.
restore_css='''/* restored original Yawaqit phone canvas */
#app{max-width:none;width:100%;height:100dvh;min-height:100dvh}
.bar{height:72px;font-size:18px}.brand-logo{width:26px;height:26px;margin-left:8px}.brand-name{font-size:18px}.bar button{right:14px}
#scr{padding:13px 13px 96px;background:var(--bg)}#nav{height:66px}#nav .t{padding-bottom:9px;font-size:12px;gap:3px}#nav .t svg{width:22px;height:22px}#bump{top:-22px;width:68px;height:44px}#dot{top:-21px;width:43px;height:43px}#dot svg{width:22px;height:22px}
.home-dashboard{padding:0}.home-heading{display:none}
@media (display-mode:fullscreen),(display-mode:standalone){#app{max-width:none;width:100vw;height:100dvh;min-height:100dvh}.bar{height:calc(72px + env(safe-area-inset-top,0px));padding-top:env(safe-area-inset-top,0px)}#scr{padding-bottom:calc(96px + env(safe-area-inset-bottom,0px))}#nav{height:calc(66px + env(safe-area-inset-bottom,0px));padding-bottom:env(safe-area-inset-bottom,0px)}}
'''
s=s.replace('</style>',restore_css+'</style>',1)
# Change manifest naming by source reference later; keep manifest separate too.
# Robust full-surah fallback on source errors.
old="audioEl.onended=()=>{S.ap=null;S.all=false;S.vp=-1;S.adhkarPlaying=false;S.audioMsg='';render()};audioEl.onerror=()=>{S.audioMsg='تعذر تحميل هذا الصوت؛ اختر قارئًا أو سورة أخرى';render()};audioEl.onplaying=()=>{S.audioMsg=''}"
new="""let audioFallbackTried=false;
audioEl.onended=()=>{audioFallbackTried=false;S.ap=null;S.all=false;S.vp=-1;S.adhkarPlaying=false;S.audioMsg='';render()};
audioEl.onerror=()=>{if(!audioFallbackTried&&S.ap!=null&&!S.vp>=0){audioFallbackTried=true;const fallback=`https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/${S.ap+1}.mp3`;if(audioEl.src!==fallback){audioEl.src=fallback;audioEl.load();audioEl.play().catch(()=>{S.audioMsg='تعذر تشغيل الصوت، حاول مرة أخرى';render()});return}}S.audioMsg=S.lang==='en'?'Audio failed. Try again.':S.lang==='fr'?'Audio indisponible. Réessayez.':'تعذر تشغيل الصوت، حاول مرة أخرى';render()};
audioEl.onplaying=()=>{audioFallbackTried=false;S.audioMsg=''}"""
s=s.replace(old,new)
# Fix a faulty precedence introduced by defensive condition, using an explicit verse guard.
s=s.replace("!S.vp>=0", "S.vp<0")
# Clean audio state before every source change and reset retry state.
s=s.replace("function playRecitation(i,exactAyah=false){const url=exactAyah?ayahUrl(S.surah,i):recitationUrl(i);", "function playRecitation(i,exactAyah=false){audioFallbackTried=false;const url=exactAyah?ayahUrl(S.surah,i):recitationUrl(i);")
s=s.replace("function stopAudio(){audioEl.pause();audioEl.currentTime=0;audioEl.removeAttribute('src');", "function stopAudio(){audioFallbackTried=false;audioEl.pause();audioEl.currentTime=0;audioEl.removeAttribute('src');")
p.write_text(s)
