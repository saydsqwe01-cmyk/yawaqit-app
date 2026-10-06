from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Keep shortcut indices aligned with the source array (25 base shortcuts + 3 custom shortcuts).
s=s.replace("SNIP_I18N.ar=Array(25).fill('');SNIP_I18N.ar.push", "SNIP_I18N.ar=Array(25).fill('');SNIP_I18N.en=[...SNIP_I18N.en,...Array(5).fill('')];SNIP_I18N.fr=[...SNIP_I18N.fr,...Array(5).fill('')];SNIP_I18N.ur=[...SNIP_I18N.ur,...Array(5).fill('')];SNIP_I18N.ar.push")
# Translate the most visible home and tasbeeh labels without changing layout.
s=s.replace("[\"السبحة\",\"moon\",\"tasbeeh\"]", "[S.lang==='en'?'Tasbeeh':S.lang==='fr'?'Tasbih':S.lang==='ur'?'تسبیح':'السبحة',\"moon\",\"tasbeeh\"]")
s=s.replace("<button id=\"gladBox\" class=\"glad-box\"><span class=\"glad-icon\">✦</span><span><b>صندوق البشارة</b><small>افتح بشارتك اليوم</small></span>", "<button id=\"gladBox\" class=\"glad-box\"><span class=\"glad-icon\">✦</span><span><b>${S.lang==='en'?'Good news box':S.lang==='fr'?'Boîte de bonnes nouvelles':S.lang==='ur'?'بشارت کا صندوق':'صندوق البشارة'}</b><small>${S.lang==='en'?'Open today’s message':S.lang==='fr'?'Ouvrir le message du jour':S.lang==='ur'?'آج کی بشارت کھولیں':'افتح بشارتك اليوم'}</small></span>")
s=s.replace("<div style=\"font-size:9px;color:#9b9b9b;text-align:center;margin:4px 0\">الصلاة السابقة: <b style=\"color:#fff\">${pr.prev.n}</b> · ${agoText(pr.prev.ago)}</div>", "<div style=\"font-size:9px;color:#9b9b9b;text-align:center;margin:4px 0\">${T('previousPrayer')}: <b style=\"color:#fff\">${PL(pr.prev.n)}</b> · ${agoText(pr.prev.ago)}</div>")
s=s.replace("${pr.n} ${S.lang==='en'?'next':S.lang==='fr'?'prochaine':S.lang==='ur'?'بعد':'بعد'}", "${PL(pr.n)} ${T('nextPrayer')}")
s=s.replace("<div class=\"card hd tasbeeh-page\"><div class=\"row\" style=\"direction:rtl;justify-content:space-between\"><b style=\"font-size:17px\">السبحة الإلكترونية</b>", "<div class=\"card hd tasbeeh-page\"><div class=\"row\" style=\"direction:rtl;justify-content:space-between\"><b style=\"font-size:17px\">${S.lang==='en'?'Electronic Tasbeeh':S.lang==='fr'?'Tasbih électronique':S.lang==='ur'?'الیکٹرانک تسبیح':'السبحة الإلكترونية'}</b>")
s=s.replace("<p class=\"mut\" style=\"text-align:center;margin:8px 0\">اذكر الله واحتسب الأجر</p>", "<p class=\"mut\" style=\"text-align:center;margin:8px 0\">${S.lang==='en'?'Remember Allah and seek reward':S.lang==='fr'?'Évoquez Allah et espérez la récompense':S.lang==='ur'?'اللہ کو یاد کریں اور اجر کی نیت کریں':'اذكر الله واحتسب الأجر'}</p>")
s=s.replace("<div class=\"tasbeeh-label\">اضغط على الصورة للتسبيح</div>", "<div class=\"tasbeeh-label\">${S.lang==='en'?'Tap the image to count':S.lang==='fr'?'Touchez l’image pour compter':S.lang==='ur'?'گنتی کے لیے تصویر دبائیں':'اضغط على الصورة للتسبيح'}</div>")
s=s.replace("<button id=\"tasbeehReset\" class=\"pill\">تصفير العداد</button>", "<button id=\"tasbeehReset\" class=\"pill\">${S.lang==='en'?'Reset counter':S.lang==='fr'?'Réinitialiser':S.lang==='ur'?'کاؤنٹر صفر کریں':'تصفير العداد'}</button>")
p.write_text(s)
print('final localization fixes applied')
