from pathlib import Path
import shutil, json
root=Path('/home/ubuntu/work/yawaqit_extract')
p=root/'index.html'
s=p.read_text()
# Persist one monthly Islamic reminder separately from the daily reminder.
s=s.replace("dailyNotifyEnabled:true,dailyNotifyHour:10,dailyNotifyLast:'',quizLevel", "dailyNotifyEnabled:true,dailyNotifyHour:10,dailyNotifyLast:'',monthlyNotifyLast:'',quizLevel", 1)
s=s.replace("dailyLast:S.dailyNotifyLast}))", "dailyLast:S.dailyNotifyLast,monthlyLast:S.monthlyNotifyLast}))", 1)
s=s.replace("if(x.dailyLast)S.dailyNotifyLast=x.dailyLast}catch(_){} }", "if(x.dailyLast)S.dailyNotifyLast=x.dailyLast;if(x.monthlyLast)S.monthlyNotifyLast=x.monthlyLast}catch(_){} }", 1)
# All app notifications use the existing local notify sound before their content sound.
s=s.replace("function speakReminder(){", "function playNotificationSequence(after){return playEffect('notify',after)}\nfunction speakReminder(){", 1)
s=s.replace("}playAdhan(prayer);}", "}playNotificationSequence(()=>playAdhan(prayer));}", 1)
# Replace the Gregorian-only reminder block with daily + Islamic calendar reminders.
old="""function dailyReminderText(){const d=new Date(),day=d.getDay(),m=d.getMonth();if(day===5)return 'اللهم صل وسلم على نبينا محمد — يوم الجمعة';if(m===8)return 'رمضان شهر القرآن — لا تنس وردك اليومي';if(m===7)return 'شعبان شهر الاستعداد — أكثر من الصلاة على النبي';return 'سبحان الله وبحمده، سبحان الله العظيم'}
function checkDailyReminders(){if(!S.dailyNotifyEnabled)return;const d=new Date(),key=d.toISOString().slice(0,10);if(d.getHours()!==Number(S.dailyNotifyHour)||d.getMinutes()>1||d.getDate()%2===0||S.dailyNotifyLast===key)return;S.dailyNotifyLast=key;saveNotifyPrefs();try{const title='تذكير من يواقيت',body=dailyReminderText();if('serviceWorker' in navigator&&navigator.serviceWorker.ready)navigator.serviceWorker.ready.then(r=>r.showNotification(title,{body,icon:'/assets/logo.png',badge:'/assets/logo.png',tag:'daily-'+key,dir:'rtl'}));}catch(e){}playEffect('notify',speakReminder)}
function startDailyReminderLoop(){if(dailyNotifyTimer)clearInterval(dailyNotifyTimer);dailyNotifyTimer=null;if(S.dailyNotifyEnabled)dailyNotifyTimer=setInterval(checkDailyReminders,30000);if(S.dailyNotifyEnabled)checkDailyReminders()}"""
new="""function dailyReminderText(){const d=new Date(),day=d.getDay();if(day===5)return 'اللهم صل وسلم على نبينا محمد — يوم الجمعة';return 'سبحان الله وبحمده، سبحان الله العظيم'}
function islamicDateParts(){try{const p=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura-nu-latn',{day:'numeric',month:'numeric',year:'numeric'}).formatToParts(new Date());return{day:+p.find(x=>x.type==='day').value,month:+p.find(x=>x.type==='month').value,year:+p.find(x=>x.type==='year').value}}catch(e){return null}}
function monthlyReminder(){const h=islamicDateParts();if(!h)return null;const m=h.month,d=h.day;if(m===9&&d===1)return['رمضان','رمضان شهر القرآن — أكثر من تلاوة القرآن والذكر.','quran'];if(m===9&&d===27)return['ليلة مباركة','اجتهد في الدعاء والقرآن والذكر في الليالي الوترية.','salawat'];if(m===10&&d===1)return['عيد الفطر','تقبل الله منا ومنكم، وأكثروا من التكبير والذكر.','salawat'];if(m===12&&d===1)return['عشر ذي الحجة','بدأت عشر ذي الحجة، فأكثر من التكبير والذكر والعمل الصالح.','salawat'];if(m===12&&d===9)return['يوم عرفة','يوم عرفة، أكثر من الدعاء والذكر والصيام لمن استطاع.','salawat'];if(m===12&&d===10)return['عيد الأضحى','تقبل الله طاعتكم، وأكثروا من التكبير والذكر.','salawat'];if(m===1&&d===10)return['يوم عاشوراء','يوم عاشوراء، تذكير بالصيام والذكر وشكر نعم الله.','salawat'];if(m===8&&d===15)return['ليلة النصف من شعبان','أكثر من الدعاء والذكر وسائر الطاعات.','salawat'];return null}
function showAppNotification(title,body,tag){try{if('serviceWorker' in navigator&&navigator.serviceWorker.ready)navigator.serviceWorker.ready.then(r=>r.showNotification(title,{body,icon:'/assets/logo.png',badge:'/assets/logo.png',tag,renotify:true,dir:'rtl',silent:false}));else if('Notification' in window&&Notification.permission==='granted')new Notification(title,{body,icon:'/assets/logo.png',tag});}catch(_){} }
function checkDailyReminders(){if(!S.dailyNotifyEnabled)return;const d=new Date(),key=d.toISOString().slice(0,10);if(d.getHours()!==Number(S.dailyNotifyHour)||d.getMinutes()>1||S.dailyNotifyLast===key)return;S.dailyNotifyLast=key;saveNotifyPrefs();const body=dailyReminderText();showAppNotification('تذكير من يواقيت',body,'daily-'+key);playNotificationSequence(speakReminder)}
function checkMonthlyReminders(){if(!S.dailyNotifyEnabled)return;const d=new Date(),h=islamicDateParts(),event=monthlyReminder();if(!h||!event||d.getHours()!==Number(S.dailyNotifyHour)||d.getMinutes()>1)return;const key=`${h.year}-${h.month}-${h.day}-${event[0]}`;if(S.monthlyNotifyLast===key)return;S.monthlyNotifyLast=key;saveNotifyPrefs();showAppNotification(event[0],event[1],'islamic-'+key);playNotificationSequence(()=>event[2]==='quran'?playRecitation(S.ap==null?0:S.ap):speakReminder())}
function startDailyReminderLoop(){if(dailyNotifyTimer)clearInterval(dailyNotifyTimer);dailyNotifyTimer=null;if(S.dailyNotifyEnabled)dailyNotifyTimer=setInterval(()=>{checkDailyReminders();checkMonthlyReminders()},30000);if(S.dailyNotifyEnabled){checkDailyReminders();checkMonthlyReminders()}}"""
if old not in s: raise SystemExit('daily reminder block not found')
s=s.replace(old,new,1)
# All prayer notifications should use the same notification sound before adhan.
s=s.replace("}catch(_){}playAdhan(prayer);}", "}catch(_){}playNotificationSequence(()=>playAdhan(prayer));}", 1)
# Make the APK conversion explicit without changing the UI.
s=s.replace('<meta name="theme-color" content="#232323">', '<meta name="theme-color" content="#232323">\n<meta name="application-name" content="يَوَاقِيت">\n<meta name="format-detection" content="telephone=no">', 1)
# Force a new cache after notification assets are added.
(root/'public/sw.js').write_text((root/'public/sw.js').read_text().replace("yawaqit-media-v6","yawaqit-media-v7",1))
p.write_text(s)
# Local notification audio asset for PWA/APK packaging and future Android notification channels.
shutil.copy2(root/'public/assets/audio/notify.mp3', root/'public/assets/notification-sound.mp3')
# Android wrapper configuration; the existing Vite build remains unchanged.
(root/'capacitor.config.json').write_text(json.dumps({"appId":"com.yawaqit.app","appName":"يَوَاقِيت","webDir":"dist","bundledWebRuntime":False,"android":{"allowMixedContent":False}},ensure_ascii=False,indent=2)+'\n')
# Enrich manifest for installability and Android wrapper tooling.
m=json.loads((root/'public/manifest.webmanifest').read_text())
m.update({"id":"/","categories":["lifestyle","education"],"prefer_related_applications":False})
(root/'public/manifest.webmanifest').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('notification sequences, Islamic reminders, and Android readiness added')
