from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()

# Keep the existing visual design, but make media framing explicit: full YouTube content on black.
s=s.replace(".ytframe{width:100%;height:100%;border:0;border-radius:10px;display:block}", ".ytframe{width:100%;height:100%;border:0;border-radius:10px;display:block;background:#000}.player .thumb.pv{background:#000!important;overflow:hidden}.player .ytframe{aspect-ratio:16/9;object-fit:contain;background:#000}.learn-video{background:#000!important}.learn-video iframe{display:block;width:100%;background:#000;object-fit:contain}")
s=s.replace(".reels-feed .transfer-video{display:block;width:100%;height:100%!important;min-height:0;object-fit:cover;border-radius:0;background:#000}", ".reels-feed .transfer-video{display:block;width:100%;height:100%!important;min-height:0;object-fit:contain;border-radius:0;background:#000}")

# Better language storage and initial document direction.
s=s.replace("lang:'ar',langName:'العربية',langDir:'rtl'", "lang:localStorage.getItem('yawaqit-lang')||'ar',langName:localStorage.getItem('yawaqit-lang-name')||'العربية',langDir:localStorage.getItem('yawaqit-lang-dir')||'rtl'")

# Add common translated UI labels without touching the established layout.
needle="const TXT={\n ar:{"
insert="""const TXT={
 ar:{settingsTheme:'مظهر التطبيق',language:'لغة القرآن والواجهة',chooseLanguage:'اختر اللغة',morningMode:'وضع صباحي',nightMode:'وضع ليلي',prayerNotifications:'إشعارات الصلاة',enabled:'مفعلة',disabled:'متوقفة',adhanSound:'صوت الأذان',fajrAdhanSound:'صوت أذان الفجر',dailyReminders:'تذكيرات المناسبات',reminderHour:'ساعة التذكير',close:'إغلاق',previousPrayer:'الصلاة السابقة',nextPrayer:'الصلاة القادمة',fullVideo:'فيديو كامل',openYouTube:'فتح الفيديو في YouTube إذا لم يعمل التشغيل داخل الصفحة ↗',videoList:'فيديو وخطبة ورسالة يومية',share:'إعادة نشر',like:'إعجاب',playFromSource:'تشغيل الفيديو'},
 en:{settingsTheme:'App appearance',language:'Quran and interface language',chooseLanguage:'Choose language',morningMode:'Light mode',nightMode:'Dark mode',prayerNotifications:'Prayer notifications',enabled:'Enabled',disabled:'Disabled',adhanSound:'Adhan sound',fajrAdhanSound:'Fajr adhan sound',dailyReminders:'Daily reminders',reminderHour:'Reminder hour',close:'Close',previousPrayer:'Previous prayer',nextPrayer:'Next prayer',fullVideo:'Full video',openYouTube:'Open on YouTube if playback does not work here ↗',videoList:'Videos, sermons and daily messages',share:'Repost',like:'Like',playFromSource:'Play video'},
 fr:{settingsTheme:'Apparence',language:'Langue du Coran et de l’interface',chooseLanguage:'Choisir la langue',morningMode:'Mode clair',nightMode:'Mode sombre',prayerNotifications:'Notifications de prière',enabled:'Activées',disabled:'Désactivées',adhanSound:'Son de l’adhan',fajrAdhanSound:'Son de l’adhan du Fajr',dailyReminders:'Rappels quotidiens',reminderHour:'Heure du rappel',close:'Fermer',previousPrayer:'Prière précédente',nextPrayer:'Prochaine prière',fullVideo:'Vidéo complète',openYouTube:'Ouvrir sur YouTube si la lecture échoue ici ↗',videoList:'Vidéos, sermons et messages quotidiens',share:'Reposter',like:'J’aime',playFromSource:'Lire la vidéo'},
 ur:{settingsTheme:'ایپ کا انداز',language:'قرآن اور انٹرفیس کی زبان',chooseLanguage:'زبان منتخب کریں',morningMode:'دن کا موڈ',nightMode:'رات کا موڈ',prayerNotifications:'نماز کی اطلاعات',enabled:'فعال',disabled:'غیر فعال',adhanSound:'اذان کی آواز',fajrAdhanSound:'فجر کی اذان کی آواز',dailyReminders:'روزانہ یاد دہانیاں',reminderHour:'یاد دہانی کا وقت',close:'بند کریں',previousPrayer:'پچھلی نماز',nextPrayer:'اگلی نماز',fullVideo:'مکمل ویڈیو',openYouTube:'اگر یہاں نہ چلے تو YouTube پر کھولیں ↗',videoList:'ویڈیوز، خطبات اور روزانہ پیغامات',share:'دوبارہ نشر',like:'پسند',playFromSource:'ویڈیو چلائیں'},
"""
if needle in s:
    s=s.replace(needle,insert,1)

# Add a single helper for direction/name application.
needle="function T(k,fallback){return (TXT[S&&S.lang]||TXT.ar)[k]||fallback||TXT.ar[k]||k}"
rep=needle+"\nfunction setLanguage(l){S.lang=l.iso_code||'ar';S.langName=l.native_name||l.name||S.lang;S.langDir=l.direction||'ltr';localStorage.setItem('yawaqit-lang',S.lang);localStorage.setItem('yawaqit-lang-name',S.langName);localStorage.setItem('yawaqit-lang-dir',S.langDir);document.documentElement.lang=S.lang;document.documentElement.dir=S.langDir;document.body.dir=S.langDir;}\nsetLanguage({iso_code:S.lang,native_name:S.langName,direction:S.langDir});"
s=s.replace(needle,rep,1)

# Localize the settings labels that were hardcoded.
s=s.replace("<h3>${L('settings')}</h3><div class=\"tg\"><span>مظهر التطبيق</span><button id=\"themeBtn\" class=\"notify-setting\">${S.theme==='light'?'وضع صباحي':'وضع ليلي'}</button></div><div class=\"tg\"><span>${S.lang==='en'?'Quran and interface language':S.lang==='fr'?'Langue du Coran et de l’interface':'لغة القرآن والواجهة'}</span>", "<h3>${L('settings')}</h3><div class=\"tg\"><span>${T('settingsTheme')}</span><button id=\"themeBtn\" class=\"notify-setting\">${S.theme==='light'?T('morningMode'):T('nightMode')}</button></div><div class=\"tg\"><span>${T('language')}</span>")
s=s.replace("<div class=\"tg\"><span>إشعارات الصلاة</span><button id=\"notifyBtn\" class=\"notify-setting\">${S.notifyEnabled?'مفعلة':'متوقفة'}</button></div><div class=\"tg\"><span>صوت الأذان</span>", "<div class=\"tg\"><span>${T('prayerNotifications')}</span><button id=\"notifyBtn\" class=\"notify-setting\">${S.notifyEnabled?T('enabled'):T('disabled')}</button></div><div class=\"tg\"><span>${T('adhanSound')}</span>")
s=s.replace("<div class=\"tg\"><span>صوت أذان الفجر</span>", "<div class=\"tg\"><span>${T('fajrAdhanSound')}</span>")
s=s.replace("<div class=\"tg\"><span>تذكيرات المناسبات</span>", "<div class=\"tg\"><span>${T('dailyReminders')}</span>")
s=s.replace("<div class=\"tg\"><span>ساعة التذكير</span>", "<div class=\"tg\"><span>${T('reminderHour')}</span>")
s=s.replace("listSheet('اختر اللغة'", "listSheet(T('chooseLanguage')")
# Replace duplicate language handler body assignments with shared helper in both occurrences.
s=s.replace("S.lang=l.iso_code;S.langName=l.native_name||l.name;S.langDir=l.direction||'ltr';document.documentElement.lang=S.lang;document.documentElement.dir=S.langDir;", "setLanguage(l);")
s=s.replace("S.lang=l.iso_code;S.langName=l.native_name||l.name;S.langDir=l.direction||'ltr';", "setLanguage(l);")
# Ensure the actual handler persists language and rerenders immediately (the second handler is the active one).
s=s.replace("document.documentElement.lang=S.lang;document.documentElement.dir=S.langDir;updateWomenStories();render(true);", "setLanguage(l);updateWomenStories();render(true);")

# Localize selected prominent video/reel labels.
s=s.replace("aria-label=\"إعجاب\"", "aria-label=\"${T('like')}\"")
s=s.replace("aria-label=\"إعادة نشر\"", "aria-label=\"${T('share')}\"")
s=s.replace("<a class=\"video-open-link\" href=\"${videoUrl}\" target=\"_blank\" rel=\"noopener noreferrer\">فتح الفيديو في YouTube إذا لم يعمل التشغيل داخل الصفحة ↗</a>", "<a class=\"video-open-link\" href=\"${videoUrl}\" target=\"_blank\" rel=\"noopener noreferrer\">${T('openYouTube')}</a>")
s=s.replace("<div class=\"sec\">٣٠ فيديو وخطبة ورسالة يومية</div>", "<div class=\"sec\">${T('videoList')}</div>")

# Stop like/repost from rerendering the whole feed (which restarted every video).
old="""A('[data-reel-like]',e=>{const i=e.dataset.reelLike;S.reelLikes[i]=!S.reelLikes[i];render()});A('[data-reel-repost]',e=>{const i=e.dataset.reelRepost;S.reelReposts[i]=!S.reelReposts[i];render()});"""
new="""A('[data-reel-like]',e=>{const i=e.dataset.reelLike;S.reelLikes[i]=!S.reelLikes[i];e.classList.toggle('active',!!S.reelLikes[i]);e.setAttribute('aria-pressed',String(!!S.reelLikes[i]));localStorage.setItem('yawaqit-reel-likes',JSON.stringify(S.reelLikes))});A('[data-reel-repost]',e=>{const i=e.dataset.reelRepost;S.reelReposts[i]=!S.reelReposts[i];e.classList.toggle('active',!!S.reelReposts[i]);e.setAttribute('aria-pressed',String(!!S.reelReposts[i]));localStorage.setItem('yawaqit-reel-reposts',JSON.stringify(S.reelReposts))});"""
if old not in s:
    raise SystemExit('reel binding not found')
s=s.replace(old,new,1)
# Load saved reel states and avoid autoplay loops on all videos; IntersectionObserver controls the active reel.
s=s.replace("reelLikes:{},reelReposts:{}", "reelLikes:JSON.parse(localStorage.getItem('yawaqit-reel-likes')||'{}'),reelReposts:JSON.parse(localStorage.getItem('yawaqit-reel-reposts')||'{}')")
s=s.replace("v.volume=1;v.muted=false;});\n  const feed", "v.volume=1;v.muted=false;if(!v.closest('.reels-feed'))v.play().catch(()=>{});});\n  const feed",1)
# Use translated prompt copy.
s=s.replace("<small>اضغط لمشاهدة الفيديو</small>", "<small>${T('playFromSource')}</small>")

p.write_text(s)
print('patched', p)
