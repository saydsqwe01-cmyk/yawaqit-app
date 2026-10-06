from pathlib import Path
import re
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Replace the broad hadith search with a structured signs catalogue: topic + classification + source, not raw unrelated narrations.
old_start='async function loadSignsApi()'
start=s.find(old_start)
end=s.find('\nasync function loadProphetStoriesApi()',start)
if start<0 or end<0: raise SystemExit('signs function not found')
signs="""function loadSignsApi(){if(SIGNS_API_READY)return;SIGNS_API_READY=true;DET[3]=[['ظهور الفتن وكثرة الاضطراب','علامات صغرى · أحاديث صحيحة'],['قبض العلم وظهور الجهل','علامات صغرى · انتشار الجهل وذهاب العلماء'],['كثرة الزلازل','علامات صغرى · تذكير بالرجوع إلى الله'],['تقارب الزمان','علامات صغرى · تغير الإحساس بالوقت'],['كثرة القتل','علامات صغرى · التحذير من الفتن وسفك الدماء'],['التطاول في البنيان','علامات صغرى · ورد في حديث جبريل'],['كثرة المال وظهور الغنى','علامات صغرى · من أشراط الساعة'],['ضياع الأمانة وإسناد الأمر إلى غير أهله','علامات صغرى · من أشراط الساعة'],['خروج المهدي','علامات كبرى · في آخر الزمان'],['خروج الدجال','علامة كبرى · أعظم فتنة منذ خلق آدم'],['نزول عيسى ابن مريم عليه السلام','علامة كبرى · يكسر الصليب ويقتل الخنزير'],['خروج يأجوج ومأجوج','علامة كبرى · بعد نزول عيسى عليه السلام'],['الدخان','علامة كبرى · مذكور في سورة الدخان'],['الدابة','علامة كبرى · خروج دابة تكلم الناس'],['طلوع الشمس من مغربها','علامة كبرى · عندها يغلق باب التوبة'],['ثلاثة خسوف','علامة كبرى · خسف بالمشرق وخسف بالمغرب وخسف بجزيرة العرب'],['النار التي تحشر الناس','علامة كبرى · آخر العلامات العظام'],['النفخ في الصور','أحداث القيامة · البعث والحساب'],['البعث والنشور','أحداث القيامة · ﴿ثُمَّ إِنَّكُم بَعْدَ ذَٰلِكَ لَمَيِّتُونَ﴾'],['الحساب والجزاء','أحداث القيامة · العدل الإلهي الكامل']];render()}"""
s=s[:start]+signs+s[end:]
# Prevent the dhikr page from being replaced with a generic Hadith keyword dump.
s=s.replace("async function loadSectionApi(n){if(n===2)loadHistoryApi();else if(n===3)loadSignsApi();else if(n===4)loadRuqyahApi();else if(n===7)loadQuranDuasApi();else if(n===12)loadQuizApi();else if(n===17)loadProphetStoriesApi();else if(n===22)loadDhikrBenefitsApi();else if(n===23)loadFaithPauseApi()}", "async function loadSectionApi(n){if(n===2)loadHistoryApi();else if(n===4)loadRuqyahApi();else if(n===7)loadQuranDuasApi();else if(n===12)loadQuizApi();else if(n===17)loadProphetStoriesApi();else if(n===23)loadFaithPauseApi()}",1)
# Add missing Quran virtues and a static signs fallback to the curated section set.
needle="DET[22]=[['طمأنينة القلب'"
insert="DET[13]=[['فضل تلاوة القرآن','﴿إِنَّ الَّذِينَ يَتْلُونَ كِتَابَ اللَّهِ وَأَقَامُوا الصَّلَاةَ﴾ · فاطر 29'],['القرآن شفاء ورحمة','﴿وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ﴾ · الإسراء 82'],['تدبر القرآن والعمل به','﴿كِتَابٌ أَنزَلْنَاهُ إِلَيْكَ مُبَارَكٌ لِّيَدَّبَّرُوا آيَاتِهِ﴾ · ص 29']];\n  DET[3]=[['علامات الساعة الصغرى','أبواب وعناوين موثقة من السنة · اختر الموضوع للتفصيل'],['علامات الساعة الكبرى','الدجال ونزول عيسى ويأجوج ومأجوج وطلوع الشمس'],['أحداث القيامة','النفخ والبعث والحساب والجزاء']];\n  "
if needle not in s: raise SystemExit('dhikr insertion point not found')
s=s.replace(needle,insert+needle,1)
p.write_text(s)
print('section content guard applied')
