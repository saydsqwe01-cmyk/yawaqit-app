from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Remove the premature invocation; S is declared later.
s=s.replace("\nsetLanguage({iso_code:S.lang,native_name:S.langName,direction:S.langDir});","")
# Rebuild the beginning of TXT as a valid object (the source is intentionally compact).
start=s.index('const TXT={')
end=s.index(" en:{", start)
ar_old="quranTitle:'المصحف الشريف',surahs:'سورة',searchSurah:'ابحث عن اسم السورة أو رقمها',searchContent:'ابحث داخل المحتوى',translate:'الترجمة',translation:'العربية',noResults:'لا توجد نتائج مطابقة',next:'التالي',result:'النتيجة',quiz:'تحدي الأسئلة',answered:'المجاب',correct:'الصحيح',final:'النتيجة النهائية',retry:'إعادة التحدي',audioDetails:'تفاصيل الصوت',reader:'القارئ',surah:'السورة',ayah:'الآية',playSurah:'تشغيل السورة كاملة',stop:'إيقاف',tafsir:'التفسير الميسر',dailyVerse:'آية وعبرة',about:'بعد كل ضيق فرج قريب',adhkar:'كل الأذكار',search:'ابحث هنا',selectReader:'اختر القارئ',selectSurah:'اختر السورة',listen:'اضغط تشغيل للاستماع',playing:'يتم التشغيل الآن'"
ar_new="settingsTheme:'مظهر التطبيق',language:'لغة القرآن والواجهة',chooseLanguage:'اختر اللغة',morningMode:'وضع صباحي',nightMode:'وضع ليلي',prayerNotifications:'إشعارات الصلاة',enabled:'مفعلة',disabled:'متوقفة',adhanSound:'صوت الأذان',fajrAdhanSound:'صوت أذان الفجر',dailyReminders:'تذكيرات المناسبات',reminderHour:'ساعة التذكير',close:'إغلاق',previousPrayer:'الصلاة السابقة',nextPrayer:'الصلاة القادمة',fullVideo:'فيديو كامل',openYouTube:'فتح الفيديو في YouTube إذا لم يعمل التشغيل داخل الصفحة ↗',videoList:'فيديو وخطبة ورسالة يومية',share:'إعادة نشر',like:'إعجاب',playFromSource:'تشغيل الفيديو'"
new=f"const TXT={{\n ar:{{{ar_new},{ar_old}}},\n"
s=s[:start]+new+s[end:]
# Initialize direction only after S exists.
needle="const SPD=[1,1.25,1.5,2];"
s=s.replace(needle,"setLanguage({iso_code:S.lang,native_name:S.langName,direction:S.langDir});\n"+needle,1)
p.write_text(s)
print('repaired')
