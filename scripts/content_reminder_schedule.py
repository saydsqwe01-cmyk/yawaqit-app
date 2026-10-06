from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
s=s.replace("monthlyNotifyLast:'',quizLevel", "monthlyNotifyLast:'',contentNotifyLast:'',quizLevel", 1)
s=s.replace("monthlyLast:S.monthlyNotifyLast}))", "monthlyLast:S.monthlyNotifyLast,contentLast:S.contentNotifyLast}))", 1)
s=s.replace("if(x.monthlyLast)S.monthlyNotifyLast=x.monthlyLast}catch(_){} }", "if(x.monthlyLast)S.monthlyNotifyLast=x.monthlyLast;if(x.contentLast)S.contentNotifyLast=x.contentLast}catch(_){} }", 1)
needle="function startDailyReminderLoop(){if(dailyNotifyTimer)clearInterval(dailyNotifyTimer);dailyNotifyTimer=null;if(S.dailyNotifyEnabled)dailyNotifyTimer=setInterval(()=>{checkDailyReminders();checkMonthlyReminders()},30000);if(S.dailyNotifyEnabled){checkDailyReminders();checkMonthlyReminders()}}"
replacement="""function speakArabicText(text){try{if(!('speechSynthesis' in window))return;const u=new SpeechSynthesisUtterance(String(text||''));u.lang='ar-SA';u.rate=.82;u.pitch=1;window.speechSynthesis.cancel();window.speechSynthesis.speak(u)}catch(e){}}
function checkContentReminders(){if(!S.dailyNotifyEnabled)return;const d=new Date(),hour=d.getHours(),minute=d.getMinutes(),date=d.toISOString().slice(0,10);if(minute>1)return;const plans={8:['ذكر الصباح','ابدأ يومك بذكر الله والصلاة على النبي ﷺ','salawat'],14:['ورد القرآن','حان وقت وردك من القرآن الكريم','quran'],20:['حديث اليوم','تذكير بحديث نبوي صحيح','hadith']};const plan=plans[hour];if(!plan)return;const key=`${date}-${hour}`;if(S.contentNotifyLast===key)return;S.contentNotifyLast=key;saveNotifyPrefs();let body=plan[1],text='صَلِّ على النبي';if(plan[2]==='hadith'){const h=(DET[0]||[])[dayIndex()%(DET[0]||[]).length];if(h){body=h[0];text='قال رسول الله صلى الله عليه وسلم: '+h[0]}}showAppNotification(plan[0],body,'content-'+key);playNotificationSequence(()=>plan[2]==='quran'?playRecitation(S.ap==null?0:S.ap):speakArabicText(text))}
function startDailyReminderLoop(){if(dailyNotifyTimer)clearInterval(dailyNotifyTimer);dailyNotifyTimer=null;if(S.dailyNotifyEnabled)dailyNotifyTimer=setInterval(()=>{checkDailyReminders();checkMonthlyReminders();checkContentReminders()},30000);if(S.dailyNotifyEnabled){checkDailyReminders();checkMonthlyReminders();checkContentReminders()}}"""
if needle not in s: raise SystemExit('daily loop not found')
s=s.replace(needle,replacement,1)
p.write_text(s)
print('content reminder schedule added')
