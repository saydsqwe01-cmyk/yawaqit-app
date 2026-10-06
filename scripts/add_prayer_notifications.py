from pathlib import Path

p=Path('/home/ubuntu/yawaqit/index.html')
s=p.read_text(encoding='utf-8')

# Replace the mosque image everywhere with the newly supplied decorative frame.
s=s.replace('/assets/prayer-frame.png','/assets/prayer-frame.jpg')
# Keep the new frame visually consistent with the dark site palette.
s=s.replace('object-fit:fill;object-position:center bottom;opacity:.22;pointer-events:none;mix-blend-mode:screen}', 'object-fit:fill;object-position:center bottom;opacity:.20;filter:grayscale(1) brightness(.72) contrast(1.1);pointer-events:none;mix-blend-mode:screen}', 1)

# Persist notification and adhan preferences in the existing state object.
s=s.replace("adhkarVoice:'api'};", "adhkarVoice:'api',notifyEnabled:false,adhanVoice:'makkah',lastPrayerNotification:'',notifyMessage:''};", 1)

# Add notification/audio helpers beside the existing audio element.
needle="const audioEl=new Audio();\naudioEl.preload='metadata';"
assert needle in s
helpers=r'''const audioEl=new Audio();
audioEl.preload='metadata';
const ADHAN_SOUNDS={makkah:{label:'أذان مكة',url:'https://cdn.aladhan.com/audio/adhan/adhan_makkah.mp3'},medina:{label:'أذان المدينة',url:'https://cdn.aladhan.com/audio/adhan/adhan_medina.mp3'},mishary:{label:'أذان مشاري العفاسي',url:'https://cdn.aladhan.com/audio/adhan/adhan_mishary.mp3'}};
let adhanAudio=null,notifyTimer=null;
function saveNotifyPrefs(){try{localStorage.setItem('yawaqit-notify',JSON.stringify({enabled:S.notifyEnabled,voice:S.adhanVoice,last:S.lastPrayerNotification}))}catch(_){} }
function loadNotifyPrefs(){try{const x=JSON.parse(localStorage.getItem('yawaqit-notify')||'{}');if(typeof x.enabled==='boolean')S.notifyEnabled=x.enabled;if(x.voice&&ADHAN_SOUNDS[x.voice])S.adhanVoice=x.voice;if(x.last)S.lastPrayerNotification=x.last}catch(_){} }
function playAdhan(){const sound=ADHAN_SOUNDS[S.adhanVoice]||ADHAN_SOUNDS.makkah;try{if(adhanAudio){adhanAudio.pause();adhanAudio.currentTime=0}adhanAudio=new Audio(sound.url);adhanAudio.preload='auto';adhanAudio.play().catch(()=>{S.audioMsg='اضغط تشغيل للسماح بصوت الأذان';render()})}catch(_){} }
function notifyPrayer(prayer){const now=new Date(),key=`${now.toISOString().slice(0,10)}-${prayer[0]}`;if(S.lastPrayerNotification===key)return;S.lastPrayerNotification=key;saveNotifyPrefs();const title=`حان وقت صلاة ${prayer[0]}`,body='تقبل الله طاعتكم';try{if('serviceWorker' in navigator&&navigator.serviceWorker.ready)navigator.serviceWorker.ready.then(r=>r.showNotification(title,{body,icon:'/assets/logo.png',badge:'/assets/logo.png',tag:key,renotify:true,dir:'rtl'}));else if('Notification' in window&&Notification.permission==='granted')new Notification(title,{body,icon:'/assets/logo.png',tag:key});}catch(_){}playAdhan();}
function checkPrayerNotifications(){if(!S.notifyEnabled)return;const d=new Date(),sec=d.getHours()*3600+d.getMinutes()*60+d.getSeconds();for(const p of PR){const target=p[1]*3600+p[2]*60;if(Math.abs(sec-target)<=35){notifyPrayer(p);break}}}
async function enablePrayerNotifications(){if(!('Notification' in window)){S.notifyMessage='الإشعارات غير مدعومة في هذا المتصفح';render();return}let permission=Notification.permission;if(permission!=='granted')permission=await Notification.requestPermission();if(permission==='granted'){S.notifyEnabled=true;S.notifyMessage='الإشعارات مفعلة';saveNotifyPrefs();startPrayerNotificationLoop();render()}else{S.notifyEnabled=false;S.notifyMessage='اسمح بالإشعارات من إعدادات المتصفح';saveNotifyPrefs();render()}}
function startPrayerNotificationLoop(){if(notifyTimer)clearInterval(notifyTimer);if(S.notifyEnabled)notifyTimer=setInterval(checkPrayerNotifications,30000);checkPrayerNotifications()}
loadNotifyPrefs();
'''
s=s.replace(needle,helpers,1)

# Add settings controls below the font-size control.
old="</div>`);\n  $('#sh').querySelectorAll('[data-fs]')"
new="</div><div class=\"tg\"><span>إشعارات الصلاة</span><button id=\"notifyBtn\" class=\"notify-setting\">${S.notifyEnabled?'مفعلة':'تفعيل'}</button></div><div class=\"tg\"><span>صوت الأذان</span><select id=\"adhanVoice\" class=\"notify-select\">${Object.entries(ADHAN_SOUNDS).map(([k,v])=>`<option value=\"${k}\" ${S.adhanVoice===k?'selected':''}>${v.label}</option>`).join('')}</select></div>${S.notifyMessage?`<div class=\"notify-message\">${S.notifyMessage}</div>`:''}`);\n  $('#sh').querySelectorAll('[data-fs]')"
assert old in s
s=s.replace(old,new,1)

# Bind the new controls at the end of settings().
needle2="if(S.qz)loadQuizApi()});\n}"
assert needle2 in s
replacement="if(S.qz)loadQuizApi()});$('#notifyBtn').onclick=()=>{if(S.notifyEnabled){S.notifyEnabled=false;saveNotifyPrefs();startPrayerNotificationLoop();render()}else enablePrayerNotifications()};$('#adhanVoice').onchange=e=>{S.adhanVoice=e.target.value;saveNotifyPrefs()};\n}"
s=s.replace(needle2,replacement,1)

# Start the in-page scheduler after collected data and location are ready.
s=s.replace("updateTimeTheme();loadLocationPrayer();loadNamesApi();", "updateTimeTheme();loadLocationPrayer();startPrayerNotificationLoop();loadNamesApi();", 1)

# Add compact styles for the settings controls.
css=""".notify-setting,.notify-select{background:#101010;color:#fff;border:1px solid #333;border-radius:10px;padding:7px 10px;font-size:10px}.notify-setting{color:#4fb3ec}.notify-message{color:#aaa;text-align:center;font-size:9px;padding:5px}.prayer-frame-art{filter:grayscale(1) brightness(.72) contrast(1.1)}
"""
s=s.replace('</style>',css+'</style>',1)
p.write_text(s,encoding='utf-8')
print('notifications_added')
