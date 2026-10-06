import { useEffect, useMemo, useRef, useState } from 'react'
import './styles.css'
import { quranDuas } from './quran-duas'

type Tab = 'home' | 'quran' | 'quran-duas' | 'tasbeeh' | 'reciters' | 'hadith' | 'adhkar' | 'stories' | 'videos' | 'tafsir' | 'prayer' | 'settings'
type AnyObj = Record<string, any>

const tabs: { id: Tab; label: string; icon: string }[] = [
  { id: 'home', label: 'الرئيسية', icon: '⌂' },
  { id: 'quran', label: 'المصحف', icon: '▤' },
  { id: 'tasbeeh', label: 'السبحة', icon: '◌' },
  { id: 'reciters', label: 'القراء', icon: '◉' },
  { id: 'hadith', label: 'الأحاديث', icon: '✦' },
  { id: 'adhkar', label: 'الأذكار', icon: '☾' },
]

const moreTabs: { id: Tab; label: string; icon: string }[] = [
  { id: 'stories', label: 'قصص الأنبياء', icon: '✧' },
  { id: 'videos', label: 'الخطب', icon: '▶' },
  { id: 'tafsir', label: 'التفاسير', icon: '⌘' },
  { id: 'prayer', label: 'المواقيت', icon: '◷' },
  { id: 'quran-duas', label: 'أدعية قرآنية', icon: '♡' },
  { id: 'settings', label: 'الإعدادات', icon: '⚙' },
]

const fallbackPrayer = [
  ['الفجر', '04:57'], ['الظهر', '12:03'], ['العصر', '15:27'], ['المغرب', '18:01'], ['العشاء', '19:31'],
]

const pathToTab = (): Tab => {
  const path = window.location.pathname.replace(/\/$/, '')
  const match = [...tabs, ...moreTabs].find(item => item.id !== 'home' && `/${item.id === 'prayer' ? 'prayer-times' : item.id}` === path)
  return match?.id || 'home'
}

const tabToPath = (next: Tab) => next === 'home' ? '/' : `/${next === 'prayer' ? 'prayer-times' : next}`

const arabicNumber = (value: number | string) => String(value).replace(/\d/g, d => '٠١٢٣٤٥٦٧٨٩'[Number(d)])
const fmtTime = (seconds: number) => {
  if (!Number.isFinite(seconds)) return '00:00'
  const s = Math.max(0, Math.floor(seconds))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  return `${h ? `${String(h).padStart(2, '0')}:` : ''}${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}
const stripHtml = (value: string) => value.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
const store = (key: string, value: unknown) => localStorage.setItem(`yawaqit:${key}`, JSON.stringify(value))
const readStore = <T,>(key: string, fallback: T): T => {
  try { return JSON.parse(localStorage.getItem(`yawaqit:${key}`) || '') as T } catch { return fallback }
}

function Icon({ children }: { children: string }) {
  return <span className="ui-icon" aria-hidden="true">{children}</span>
}

function SectionTitle({ children, action }: { children: string; action?: string }) {
  return <div className="section-title"><h2>{children}</h2>{action && <span className="section-action">{action}</span>}</div>
}


const prophetStories: AnyObj[] = [
  ['آدم','إدريس','نوح','هود','صالح','إبراهيم','لوط','إسماعيل','إسحاق','يعقوب','يوسف','أيوب','شعيب','موسى','هارون','ذو الكفل','داود','سليمان','إلياس','اليسع','يونس','زكريا','يحيى','عيسى','محمد'].map((name, i) => ({ id: ['adam','idris','nuh','hud','salih','ibrahim','lut','ismael','ishaq','yaqub','yusuf','ayyub','shuayb','musa','harun','dhul-kifl','dawud','sulaiman','ilyas','alyasa','yunus','zakariya','yahya','isa','muhammad'][i], kind: 'prophet', name: { ar: `${name} عليه السلام`, en: ['Adam','Idris','Nuh','Hud','Salih','Ibrahim','Lut','Ismael','Ishaq','Yaqub','Yusuf','Ayyub','Shuayb','Musa','Harun','Dhul-Kifl','Dawud','Sulaiman','Ilyas','Al-Yasa','Yunus','Zakariya','Yahya','Isa','Muhammad'][i] }, summary: { ar: `قصة ${name} عليه السلام: دروس في الإيمان والصبر والثبات على الحق.`, en: `The story of ${['Adam','Idris','Nuh','Hud','Salih','Ibrahim','Lut','Ismael','Ishaq','Yaqub','Yusuf','Ayyub','Shuayb','Musa','Harun','Dhul-Kifl','Dawud','Sulaiman','Ilyas','Al-Yasa','Yunus','Zakariya','Yahya','Isa','Muhammad'][i]} and lessons of faith, patience and guidance.` } })),
]
const womenStories: AnyObj[] = [
  ['مريم بنت عمران','آسية بنت مزاحم','خديجة بنت خويلد','عائشة بنت أبي بكر','فاطمة الزهراء','حفصة بنت عمر','أم سلمة','صفية بنت حيي','زينب بنت جحش','سمية بنت خياط','هاجر أم إسماعيل','سارة زوج إبراهيم','أسماء بنت أبي بكر','نسيبة بنت كعب','خولة بنت ثعلبة','رفيدة الأسلمية','أم عمارة','جويرية بنت الحارث','ميمونة بنت الحارث','رقية بنت محمد','زينب بنت محمد','أم كلثوم بنت محمد'].map((name, i) => ({ id: `woman-${i}`, kind: 'woman', name: { ar: name, en: ['Maryam bint Imran','Asiya bint Muzahim','Khadijah bint Khuwaylid','Aisha bint Abu Bakr','Fatimah az-Zahra','Hafsa bint Umar','Umm Salamah','Safiyyah bint Huyayy','Zaynab bint Jahsh','Sumayyah bint Khayyat','Hajar','Sarah','Asma bint Abi Bakr','Nusaybah bint Kab','Khawlah bint Thalabah','Rufaidah al-Aslamiyyah','Umm Umara','Juwayriyyah bint al-Harith','Maymunah bint al-Harith','Ruqayyah bint Muhammad','Zaynab bint Muhammad','Umm Kulthum bint Muhammad'][i] }, summary: { ar: `سيرة ${name} ومواقفها العظيمة في الإيمان والصبر ونصرة الحق.`, en: `The inspiring life of ${['Maryam bint Imran','Asiya bint Muzahim','Khadijah bint Khuwaylid','Aisha bint Abu Bakr','Fatimah az-Zahra','Hafsa bint Umar','Umm Salamah','Safiyyah bint Huyayy','Zaynab bint Jahsh','Sumayyah bint Khayyat','Hajar','Sarah','Asma bint Abi Bakr','Nusaybah bint Kab','Khawlah bint Thalabah','Rufaidah al-Aslamiyyah','Umm Umara','Juwayriyyah bint al-Harith','Maymunah bint al-Harith','Ruqayyah bint Muhammad','Zaynab bint Muhammad','Umm Kulthum bint Muhammad'][i]}.` } })),
]
const dhikrOptions = ['سُبْحَانَ الله','الْحَمْدُ لِلَّهِ','اللهُ أَكْبَرُ','لَا إِلَهَ إِلَّا اللهُ','أَسْتَغْفِرُ اللهَ','اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّد']
function App() {
  const [tab, setTab] = useState<Tab>(pathToTab)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [quran, setQuran] = useState<AnyObj[]>([])
  const [reciters, setReciters] = useState<AnyObj[]>([])
  const [adhkarDoors, setAdhkarDoors] = useState<AnyObj[]>([])
  const [hadithManifest, setHadithManifest] = useState<AnyObj>({ books: [], total_hadiths: 0 })
  const [tafsirResources, setTafsirResources] = useState<AnyObj[]>([])
  const [selectedSurah, setSelectedSurah] = useState<number | null>(null)
  const [selectedReciter, setSelectedReciter] = useState(0)
  const [surahQuery, setSurahQuery] = useState('')
  const [reciterQuery, setReciterQuery] = useState('')
  const [hadithQuery, setHadithQuery] = useState('')
  const [adhkarQuery, setAdhkarQuery] = useState('')
  const [selectedBook, setSelectedBook] = useState<AnyObj | null>(null)
  const [hadithRows, setHadithRows] = useState<AnyObj[]>([])
  const [hadithLoading, setHadithLoading] = useState(false)
  const [selectedDoor, setSelectedDoor] = useState(0)
  const [completedAdhkar, setCompletedAdhkar] = useState<Record<string, number>>(() => readStore('adhkar-progress', {}))
  const [fontSize, setFontSize] = useState(() => readStore('font-size', 25))
  const [showPlayer, setShowPlayer] = useState(true)
  const [favorites, setFavorites] = useState<string[]>(() => readStore('favorites', []))
  const [bookmarks, setBookmarks] = useState<string[]>(() => readStore('bookmarks', []))
  const [activeTitle, setActiveTitle] = useState('')
  const [activeReciterId, setActiveReciterId] = useState<number | null>(null)
  const [audioSrc, setAudioSrc] = useState('')
  const [playing, setPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [speed, setSpeed] = useState(1)
  const [tafsirSurah, setTafsirSurah] = useState(1)
  const [tafsirAyah, setTafsirAyah] = useState(1)
  const [tafsirResource, setTafsirResource] = useState(16)
  const [tafsirText, setTafsirText] = useState('')
  const [language, setLanguage] = useState(() => readStore('language', 'ar'))
  const [stories, setStories] = useState<AnyObj[]>([])
  const [storyFilter, setStoryFilter] = useState<'prophets' | 'women'>('prophets')
  const [selectedStory, setSelectedStory] = useState<AnyObj | null>(null)
  const [videos, setVideos] = useState<AnyObj[]>([])
  const [selectedVideo, setSelectedVideo] = useState<AnyObj | null>(null)
  const [dhikrChoice, setDhikrChoice] = useState(() => readStore('tasbeeh-dhikr', 'سُبْحَانَ الله'))
  const [tasbeehCount, setTasbeehCount] = useState(() => readStore('tasbeeh-count', 0))
  const [tasbeehTarget, setTasbeehTarget] = useState(() => readStore('tasbeeh-target', 33))
  const [tasbeehPulse, setTasbeehPulse] = useState(false)
  const [soundEnabled, setSoundEnabled] = useState(() => readStore('tasbeeh-sound', true))
  const [soundStyle, setSoundStyle] = useState(() => readStore('tasbeeh-sound-style', 'soft'))
  const [tafsirLoading, setTafsirLoading] = useState(false)
  const [city, setCity] = useState(() => readStore('city', 'مكة المكرمة'))
  const [prayerTimes, setPrayerTimes] = useState(fallbackPrayer)
  const [prayerLoading, setPrayerLoading] = useState(false)
  const audio = useRef<HTMLAudioElement | null>(null)
  const tasbeehAudio = useRef<AudioContext | null>(null)

  useEffect(() => {
    const player = new Audio()
    player.preload = 'metadata'
    audio.current = player
    const onTime = () => setCurrentTime(player.currentTime)
    const onMeta = () => setDuration(Number.isFinite(player.duration) ? player.duration : 0)
    const onPlay = () => setPlaying(true)
    const onPause = () => setPlaying(false)
    const onEnd = () => setPlaying(false)
    player.addEventListener('timeupdate', onTime)
    player.addEventListener('loadedmetadata', onMeta)
    player.addEventListener('play', onPlay)
    player.addEventListener('pause', onPause)
    player.addEventListener('ended', onEnd)
    return () => {
      player.pause()
      player.removeEventListener('timeupdate', onTime)
      player.removeEventListener('loadedmetadata', onMeta)
      player.removeEventListener('play', onPlay)
      player.removeEventListener('pause', onPause)
      player.removeEventListener('ended', onEnd)
    }
  }, [])

  useEffect(() => {
    const onPopState = () => setTab(pathToTab())
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  }, [])

  useEffect(() => {
    Promise.all([
      fetch('/data/quran/quran_uthmani_full.json').then(r => r.json()),
      fetch('/data/reciters/reciters_featured.json').then(r => r.json()),
      fetch('/data/adhkar/adhkar_full_ar.json').then(r => r.json()),
      fetch('/data/tafsir/resources.json').then(r => r.json()),
      fetch('/data/videos.json').then(r => r.json()),
      fetch('https://people.api.islamic.network/v1/people?kind=prophet&limit=50').then(r => r.json()).catch(() => ({ data: [] })),
     ]).then(([q, r, a, t, v, people]) => {
      setQuran(q.surahs || [])
      setReciters(r.reciters || [])
      setAdhkarDoors(a.doors || [])
      setTafsirResources(t.resources || [])
      setVideos((v.items || []).slice(0, 30))
      const apiPeople = (people.data || []).map((x: AnyObj) => ({ id: x.slug, kind: 'prophet', name: x.name || {}, honorific: x.honorific || {}, summary: x.description || {} }))
      setStories([...prophetStories, ...apiPeople.filter((x: AnyObj) => !prophetStories.some(y => y.id === x.id))])
      if (t.resources?.length) setTafsirResource(t.resources[0].id)
      setLoading(false)
    }).catch(() => {
      setError('تعذر تحميل البيانات المحلية. تحقق من تشغيل الخادم ثم أعد المحاولة.')
      setLoading(false)
    })
  }, [])

  // لا نحمّل فهرس وكتب الأحاديث إلا داخل صفحة الأحاديث حتى لا تتسرب بياناتها لبقية الصفحات.
  useEffect(() => {
    if (tab !== 'hadith' || hadithManifest.books?.length) return
    fetch('/data/hadith/manifest.json').then(r => r.json()).then(setHadithManifest).catch(() => setHadithManifest({ books: [], total_hadiths: 0 }))
  }, [tab, hadithManifest.books?.length])

  useEffect(() => {
    if (selectedSurah && quran.length) setTafsirSurah(selectedSurah)
  }, [selectedSurah, quran.length])

  const currentReciter = reciters.find(r => r.id === activeReciterId) || reciters[selectedReciter]
  const currentSurah = quran.find(s => s.number === selectedSurah)
  const currentDoor = adhkarDoors[selectedDoor]
  const activeHadith = selectedBook ? hadithRows.filter(h => !hadithQuery || String(h.text || '').includes(hadithQuery)).slice(0, 40) : []
  const visibleReciters = useMemo(() => reciters.filter(r => !reciterQuery || r.name.includes(reciterQuery)), [reciters, reciterQuery])
  const visibleSurahs = useMemo(() => quran.filter(s => !surahQuery || s.name.includes(surahQuery) || s.englishName?.toLowerCase().includes(surahQuery.toLowerCase())), [quran, surahQuery])
  const visibleDoors = useMemo(() => adhkarDoors.filter(d => !adhkarQuery || d.title.includes(adhkarQuery)), [adhkarDoors, adhkarQuery])

  function navigate(next: Tab) {
    setTab(next)
    window.history.pushState({}, '', tabToPath(next))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function toggleCollection(kind: 'favorites' | 'bookmarks', key: string) {
    const setter = kind === 'favorites' ? setFavorites : setBookmarks
    const current = kind === 'favorites' ? favorites : bookmarks
    const next = current.includes(key) ? current.filter(x => x !== key) : [...current, key]
    setter(next)
    store(kind, next)
  }

  function playUrl(url: string, title: string, reciterId: number | null = null) {
    if (!audio.current) return
    audio.current.src = url
    audio.current.playbackRate = speed
    audio.current.load()
    setAudioSrc(url)
    setActiveTitle(title)
    setActiveReciterId(reciterId)
    setCurrentTime(0)
    setDuration(0)
    setShowPlayer(true)
    audio.current.play().catch(() => setPlaying(false))
  }

  function playSurah(surah: AnyObj, reciter = currentReciter) {
    if (!reciter?.moshaf?.length) return
    const moshaf = reciter.moshaf[0]
    const url = `${moshaf.server}${String(surah.number).padStart(3, '0')}.mp3`
    setSelectedSurah(surah.number)
    setActiveReciterId(reciter.id)
    setTab('quran')
    playUrl(url, `${surah.name} · ${reciter.name}`, reciter.id)
  }

  function toggleAudio() {
    if (!audio.current || !audioSrc) return
    if (audio.current.paused) audio.current.play().catch(() => undefined)
    else audio.current.pause()
  }

  function seek(value: number) {
    if (!audio.current) return
    audio.current.currentTime = value
    setCurrentTime(value)
  }

  function cycleSpeed() {
    const next = speed === 1 ? 1.25 : speed === 1.25 ? 1.5 : speed === 1.5 ? 2 : 1
    setSpeed(next)
    if (audio.current) audio.current.playbackRate = next
  }

  async function loadHadith(book: AnyObj) {
    setSelectedBook(book)
    setHadithLoading(true)
    setHadithRows([])
    try {
      const data = await fetch(book.file).then(r => r.json())
      setHadithRows(data.hadiths || data.collections || [])
    } finally {
      setHadithLoading(false)
    }
  }

  async function loadTafsir() {
    setTafsirLoading(true)
    setTafsirText('')
    try {
      const url = `https://api.quran.com/api/v4/tafsirs/${tafsirResource}/by_ayah/${tafsirSurah}:${tafsirAyah}`
      const data = await fetch(url).then(r => r.json())
      setTafsirText(stripHtml(data.tafsir?.text || data.text || 'لم يتوفر نص التفسير لهذا الموضع.'))
    } catch {
      setTafsirText('تعذر جلب التفسير الآن. يمكنك قراءة الآية من المصحف والمحاولة مرة أخرى عند توفر الاتصال.')
    } finally {
      setTafsirLoading(false)
    }
  }

  async function loadPrayer() {
    setPrayerLoading(true)
    try {
      const data = await fetch(`https://api.aladhan.com/v1/timingsByCity?city=${encodeURIComponent(city)}&country=Saudi%20Arabia&method=4`).then(r => r.json())
      const t = data.data?.timings
      if (t) {
        setPrayerTimes([['الفجر', t.Fajr], ['الظهر', t.Dhuhr], ['العصر', t.Asr], ['المغرب', t.Maghrib], ['العشاء', t.Isha]])
        store('city', city)
      }
    } catch {
      setPrayerTimes(fallbackPrayer)
    } finally { setPrayerLoading(false) }
  }

  function completeDhikr(id: string, repeat: number) {
    const current = completedAdhkar[id] || 0
    const next = current >= repeat ? 0 : current + 1
    const all = { ...completedAdhkar, [id]: next }
    setCompletedAdhkar(all)
    store('adhkar-progress', all)
  }

  function Header() {
    const current = [...tabs, ...moreTabs].find(x => x.id === tab)
    return <header className="topbar">
      <button className="icon-button" onClick={() => navigate('settings')} aria-label="الإعدادات"><Icon>⚙</Icon></button>
      <div className="brand"><img src="/assets/logo.png" alt="شعار يواقيت" /><div><strong>يَوَاقِيت</strong><small>{current?.label || 'رفيقك في التلاوة والذكر'}</small></div></div>
      <button className="icon-button" onClick={() => navigate('home')} aria-label="الرئيسية"><Icon>⌂</Icon></button>
    </header>
  }

  function PlayerCard() {
    if (!audioSrc || !showPlayer) return null
    return <section className="player-card">
      <div className="player-main">
        <img className="player-avatar" src={currentReciter?.image_local || '/assets/logo.png'} alt={currentReciter?.name || 'القارئ'} />
        <div className="player-copy"><span>تشغيل التلاوة</span><strong>{activeTitle || 'تلاوة قرآنية'}</strong><small>{currentReciter?.name || 'اختر قارئًا'}</small></div>
        <button className="round-play" onClick={toggleAudio}>{playing ? 'Ⅱ' : '▶'}</button>
      </div>
      <div className="player-controls"><span>{fmtTime(currentTime)}</span><input aria-label="تقدم الصوت" type="range" min="0" max={duration || 1} value={Math.min(currentTime, duration || 1)} onChange={e => seek(Number(e.target.value))} /><span>{fmtTime(duration)}</span></div>
      <div className="player-actions"><button onClick={() => seek(Math.max(0, currentTime - 10))}>−١٠</button><button onClick={() => seek(Math.min(duration || currentTime + 10, currentTime + 10))}>+١٠</button><button onClick={cycleSpeed}>{speed}x</button><button onClick={() => { audio.current?.pause(); setShowPlayer(false) }}>إخفاء</button></div>
    </section>
  }

  function tickTasbeeh() {
    const next = tasbeehCount >= tasbeehTarget ? 1 : tasbeehCount + 1
    setTasbeehCount(next); store('tasbeeh-count', next); setTasbeehPulse(true); window.setTimeout(() => setTasbeehPulse(false), 260)
    if (navigator.vibrate) navigator.vibrate(18)
    if (soundEnabled) { try { const ctx = tasbeehAudio.current || new AudioContext(); tasbeehAudio.current = ctx; const osc = ctx.createOscillator(); const gain = ctx.createGain(); const tones: Record<string, number> = { soft: 520, click: 760, bell: 980, tap: 340 }; osc.frequency.value = tones[soundStyle] || 520; gain.gain.setValueAtTime(soundStyle === 'bell' ? .07 : .055, ctx.currentTime); gain.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + (soundStyle === 'bell' ? .2 : .12)); osc.connect(gain); gain.connect(ctx.destination); osc.start(); osc.stop(ctx.currentTime + .12) } catch {} }
  }

  function TasbeehView() {
    return <><div className="page-heading"><div><span className="eyebrow">ذكرٌ وطمأنينة</span><h1>السبحة الإلكترونية</h1><p>اختر الذكر واضغط على السبحة للعدّ مع صوت ولمسة خفيفة</p></div><span className="heading-symbol">◌</span></div><section className="tasbeeh-card"><label className="tasbeeh-select">الذكر<select value={dhikrChoice} onChange={e => { setDhikrChoice(e.target.value); store('tasbeeh-dhikr', e.target.value); setTasbeehCount(0); store('tasbeeh-count', 0) }}>{dhikrOptions.map(x => <option key={x}>{x}</option>)}</select></label><div className="tasbeeh-stage"><button className={`tasbeeh-device ${tasbeehPulse ? 'pulse' : ''}`} onClick={tickTasbeeh} aria-label="اضغط للذكر"><img src="/assets/tasbeeh-device.png" alt="سبحة إلكترونية" /><span>{arabicNumber(tasbeehCount)}</span></button></div><div className="tasbeeh-stats"><span>الهدف <b>{arabicNumber(tasbeehTarget)}</b></span><span>المتبقي <b>{arabicNumber(Math.max(0, tasbeehTarget - tasbeehCount))}</b></span><button onClick={() => { setTasbeehCount(0); store('tasbeeh-count', 0) }}>تصفير</button></div><div className="tasbeeh-tools"><label>الهدف<select value={tasbeehTarget} onChange={e => { const n=Number(e.target.value); setTasbeehTarget(n); store('tasbeeh-target', n) }}><option value={33}>٣٣</option><option value={99}>٩٩</option><option value={100}>١٠٠</option><option value={1000}>١٠٠٠</option></select></label><button className={`switch ${soundEnabled ? 'on' : ''}`} onClick={() => { setSoundEnabled(x => { store('tasbeeh-sound', !x); return !x }); }}><i /></button><span>صوت الضغط</span><select className="sound-style" value={soundStyle} onChange={e => { setSoundStyle(e.target.value); store('tasbeeh-sound-style', e.target.value) }}><option value="soft">هادئ</option><option value="click">نقرة</option><option value="bell">جرس</option><option value="tap">لمسة</option></select></div></section></>
  }

  function StoriesView() {
    const list = storyFilter === 'prophets' ? stories : womenStories
    if (selectedStory) { const name = selectedStory.name?.[language] || selectedStory.name?.ar; const summary = selectedStory.summary?.[language] || selectedStory.summary?.ar; return <><div className="page-heading"><button className="back-button" onClick={() => setSelectedStory(null)}>→</button><div><span className="eyebrow">قصص موثوقة</span><h1>{name}</h1><p>{storyFilter === 'prophets' ? 'من قصص الأنبياء' : 'من النساء العظيمات'}</p></div><span className="heading-symbol">✧</span></div><article className="story-detail"><img src="/assets/quran-primary.png" alt="" /><p>{summary}</p><p>{language === 'ar' ? 'تُجلب بيانات السجل من Islamic Network API، وتُعرض بالعربية أو الإنجليزية حسب اللغة المختارة.' : 'The registry is loaded from the Islamic Network API and shown in the selected language.'}</p></article></> }
    return <><div className="page-heading"><div><span className="eyebrow">سير وعبر</span><h1>قصص الأنبياء</h1><p>كل الأنبياء المذكورين في القرآن والنساء العظيمات</p></div><span className="heading-symbol">✧</span></div><div className="story-visuals"><img src="/assets/prayer-frame.jpg" alt="إطار روحاني" /><img src="/assets/tasbeeh-device.png" alt="سبحة إلكترونية" /><img src="/assets/salawat.png" alt="الصلاة على النبي" /><img src="/assets/remember-warning.png" alt="ذكر الله" /><img src="/assets/adhkar-footer.png" alt="الأذكار" /></div><div className="story-tabs"><button className={storyFilter === 'prophets' ? 'selected' : ''} onClick={() => setStoryFilter('prophets')}>الأنبياء ({arabicNumber(stories.length || 25)})</button><button className={storyFilter === 'women' ? 'selected' : ''} onClick={() => setStoryFilter('women')}>النساء العظيمات ({arabicNumber(womenStories.length)})</button><button onClick={() => { const next = language === 'ar' ? 'en' : 'ar'; setLanguage(next); store('language', next) }}>العربية / English</button></div><div className="story-grid">{list.map(item => <button className="story-card" key={item.id} onClick={() => setSelectedStory(item)}><span className="story-icon">✧</span><strong>{item.name?.[language] || item.name?.ar}</strong><small>{item.summary?.[language] || item.summary?.ar}</small><span className="story-arrow">←</span></button>)}</div></>
  }

  function VideosView() { return <><div className="page-heading"><div><span className="eyebrow">دروس وخطب</span><h1>الفيديوهات</h1><p>اختر أي خطبة لتشغيلها داخل الصفحة، أو افتحها مباشرة إذا منع المتصفح التضمين</p></div><span className="heading-symbol">▶</span></div>{selectedVideo && <section className="video-player"><iframe key={selectedVideo.id} src={`https://www.youtube-nocookie.com/embed/${selectedVideo.id}?rel=0&modestbranding=1&playsinline=1`} title={selectedVideo.title} allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen /><div className="video-meta"><img src={`https://i.ytimg.com/vi/${selectedVideo.id}/mqdefault.jpg`} alt="صورة الفيديو" /><div><strong>{selectedVideo.title}</strong><small>{selectedVideo.channel}</small><a href={selectedVideo.url || `https://www.youtube.com/watch?v=${selectedVideo.id}`} target="_blank" rel="noreferrer">فتح الفيديو في YouTube ↗</a></div></div></section>}<div className="video-grid">{videos.map(v => <button className="video-card" key={v.id} onClick={() => setSelectedVideo(v)}><img src={`https://i.ytimg.com/vi/${v.id}/mqdefault.jpg`} alt="" /><span>▶</span><strong>{v.title}</strong><small>{v.channel}</small></button>)}</div></> }

  function Home() {
    return <>
      <section className="hero-card">
        <div className="hero-copy"><span className="eyebrow">رفيقك في كل وقت</span><h1>تدبّر، استمع، واذكر الله</h1><p>المصحف والتلاوات والأحاديث والأذكار في تجربة واحدة هادئة.</p><button className="primary-button" onClick={() => navigate('quran')}>ابدأ التلاوة <span>←</span></button></div>
        <div className="hero-mark"><img src="/assets/logo.png" alt="" /></div>
      </section>
      <section className="prayer-card prayer-framed"><img src="/assets/prayer-frame.jpg" alt="" /><div><span className="eyebrow">مواقيت اليوم · {city}</span><h2>الصلاة القادمة</h2><strong>{prayerTimes[0][0]}</strong></div><div className="next-time">{prayerTimes[0][1]}<small>عرض المواقيت كاملة</small></div></section>
      <SectionTitle action="عرض الكل">الوصول السريع</SectionTitle>
      <div className="quick-grid">
        {[['قصص الأنبياء','سير وعبر','✧','stories'],['السبحة','ذكر قابل للتغيير','◌','tasbeeh'],['الفيديوهات','خطب ودروس','▶','videos'],['المصحف','قراءة وتلاوة','▤','quran'],['القراء','أصوات مختارة','◉','reciters'],['الأحاديث','كتب صحيحة','✦','hadith'],['الأذكار','وردك اليومي','☾','adhkar'],['التفاسير','فهم الآيات','⌘','tafsir'],['المواقيت','صلاتك أولًا','◷','prayer']].map(([title, sub, ico, destination]) => <button key={destination} className="quick-card" onClick={() => navigate(destination as Tab)}><span className="quick-icon">{ico}</span><strong>{title}</strong><small>{sub}</small></button>)}
      </div>
      <div className="home-promos"><img src="/assets/salawat.png" alt="صل على النبي" /><img src="/assets/remember-warning.png" alt="لا تنس ذكر الله" /></div><SectionTitle>ورد اليوم</SectionTitle>
      <article className="quote-card"><span className="quote-mark">“</span><p>وَرَتِّلِ الْقُرْآنَ تَرْتِيلًا</p><small>سورة المزمل · ٤</small><button onClick={() => navigate('quran')}>افتح المصحف <span>←</span></button></article>
      <SectionTitle>ملخص الحزمة</SectionTitle>
      <div className="stats-row"><div><b>١١٤</b><span>سورة</span></div><div><b>٣٦٬٥١٢</b><span>حديثًا</span></div><div><b>٢٦٧</b><span>ذكرًا</span></div></div>
    </>
  }

  function QuranView() {
    if (currentSurah) {
      const rc = currentReciter || reciters[0]
      return <>
        <div className="page-heading"><button className="back-button" onClick={() => setSelectedSurah(null)}>→</button><div><span className="eyebrow">المصحف الشريف</span><h1>{currentSurah.name}</h1></div><span className="surah-number">{arabicNumber(currentSurah.number)}</span></div>
        <section className="surah-meta"><div><span>نوع السورة</span><strong>{currentSurah.revelationType === 'Meccan' ? 'مكية' : 'مدنية'}</strong></div><div><span>عدد الآيات</span><strong>{arabicNumber(currentSurah.numberOfAyahs)}</strong></div><div><span>الجزء الأول</span><strong>{arabicNumber(currentSurah.ayahs?.[0]?.juz || 1)}</strong></div></section>
        <section className="reciter-picker"><img src={rc?.image_local || '/assets/logo.png'} alt="" /><div><span>القارئ</span><strong>{rc?.name || 'اختر قارئًا'}</strong></div><select value={selectedReciter} onChange={e => { setSelectedReciter(Number(e.target.value)); setActiveReciterId(reciters[Number(e.target.value)]?.id || null) }}>{reciters.map((r, i) => <option key={r.id} value={i}>{r.name}</option>)}</select></section>
        <section className="surah-player"><div className="audio-title"><span>تلاوة السورة كاملة</span><strong>{rc?.name}</strong></div><button className="large-play" onClick={() => playSurah(currentSurah, rc)}>{playing && activeTitle.includes(currentSurah.name) ? 'Ⅱ' : '▶'}</button><div className="player-controls"><span>{fmtTime(currentTime)}</span><input type="range" min="0" max={duration || 1} value={Math.min(currentTime, duration || 1)} onChange={e => seek(Number(e.target.value))} /><span>{fmtTime(duration)}</span></div></section>
        <SectionTitle action="تحديد موضع">آيات السورة</SectionTitle>
        <div className="ayah-list">{currentSurah.ayahs.map((ayah: AnyObj) => { const key = `${currentSurah.number}:${ayah.number}`; const fav = favorites.includes(key); const mark = bookmarks.includes(key); return <article className={`ayah-card ${activeTitle.includes(currentSurah.name) && currentTime > 0 && ayah.number === 1 ? 'active-ayah' : ''}`} key={ayah.global || ayah.number}><div className="ayah-top"><span className="ayah-badge">{arabicNumber(ayah.number)}</span><div className="ayah-actions"><button onClick={() => toggleCollection('bookmarks', key)} className={mark ? 'active-gold' : ''}>⌑</button><button onClick={() => toggleCollection('favorites', key)} className={fav ? 'active-gold' : ''}>★</button><button onClick={() => playSurah(currentSurah, rc)}>▶</button></div></div><p className="quran-text" style={{ fontSize }}>{ayah.text.replace(/^﻿/, '')}</p><small>الجزء {arabicNumber(ayah.juz)} · الصفحة {arabicNumber(ayah.page)}</small></article> })}</div>
      </>
    }
    return <>
      <div className="page-heading"><div><span className="eyebrow">القرآن الكريم</span><h1>المصحف الشريف</h1><p>١١٤ سورة · ٦٢٣٦ آية بالرسم العثماني</p></div><img className="heading-logo" src="/assets/logo.png" alt="" /></div>
      <div className="search-box"><Icon>⌕</Icon><input value={surahQuery} onChange={e => setSurahQuery(e.target.value)} placeholder="ابحث باسم السورة" /></div>
      <div className="juz-strip"><span>الأجزاء</span><strong>٣٠ جزءًا</strong><button onClick={() => setSurahQuery('')}>الكل</button></div>
      <div className="surah-list">{visibleSurahs.map(s => <button className="surah-row" key={s.number} onClick={() => setSelectedSurah(s.number)}><span className="surah-badge">{arabicNumber(s.number)}</span><span className="surah-name"><strong>{s.name}</strong><small>{s.englishName} · {s.revelationType === 'Meccan' ? 'مكية' : 'مدنية'}</small></span><span className="surah-count">{arabicNumber(s.numberOfAyahs)} آية</span><span className="row-arrow">←</span></button>)}</div>
    </>
  }

  function RecitersView() {
    return <><div className="page-heading"><div><span className="eyebrow">أصوات مختارة</span><h1>القراء</h1><p>{arabicNumber(reciters.length)} قارئًا لهم صور متوفرة</p></div><span className="heading-symbol">◉</span></div><div className="search-box"><Icon>⌕</Icon><input value={reciterQuery} onChange={e => setReciterQuery(e.target.value)} placeholder="ابحث عن قارئ" /></div><div className="reciter-grid">{visibleReciters.map((r, i) => <button className="reciter-card" key={r.id} onClick={() => { setSelectedReciter(reciters.findIndex(x => x.id === r.id)); setActiveReciterId(r.id); navigate('quran') }}><img src={r.image_local} alt={r.name} /><div><strong>{r.name}</strong><small>{arabicNumber(r.moshaf?.length || 0)} مصحف متوفر</small></div><span>←</span></button>)}</div></>
  }

  function HadithView() {
    if (selectedBook) return <><div className="page-heading"><button className="back-button" onClick={() => { setSelectedBook(null); setHadithRows([]) }}>→</button><div><span className="eyebrow">كتب الحديث</span><h1>{selectedBook.name}</h1><p>{arabicNumber(selectedBook.count)} حديثًا</p></div></div><div className="search-box"><Icon>⌕</Icon><input value={hadithQuery} onChange={e => setHadithQuery(e.target.value)} placeholder="ابحث داخل الكتاب" /></div>{hadithLoading ? <div className="loading-card">جارٍ تحميل الكتاب...</div> : <div className="hadith-list">{activeHadith.map((h, i) => <article className="hadith-card" key={h.number || i}><div className="hadith-head"><span>حديث {arabicNumber(h.number || i + 1)}</span><button onClick={() => toggleCollection('favorites', `hadith:${selectedBook.slug}:${h.number || i}`)} className={favorites.includes(`hadith:${selectedBook.slug}:${h.number || i}`) ? 'active-gold' : ''}>★</button></div><p>{h.text}</p><small>{selectedBook.name} · المصدر المحلي</small></article>)}</div>}</>
    return <><div className="page-heading"><div><span className="eyebrow">من كتب السنة</span><h1>الأحاديث النبوية</h1><p>{arabicNumber(hadithManifest.total_hadiths || 36512)} حديثًا في {arabicNumber(hadithManifest.books?.length || 10)} كتب</p></div><span className="heading-symbol">✦</span></div><div className="hadith-feature"><span>«إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى»</span><small>متفق عليه · من صحيح البخاري</small></div><SectionTitle>اختر كتابًا</SectionTitle><div className="book-grid">{(hadithManifest.books || []).map((b: AnyObj) => <button className="book-card" key={b.slug} onClick={() => loadHadith(b)}><span className="book-icon">▤</span><strong>{b.name}</strong><small>{arabicNumber(b.count)} حديث</small></button>)}</div></>
  }

  function AdhkarView() {
    const filtered = visibleDoors.length ? visibleDoors : adhkarDoors
    const activeIndex = filtered.findIndex(d => d.id === currentDoor?.id)
    const door = activeIndex >= 0 ? filtered[activeIndex] : filtered[0]
    return <><div className="page-heading"><div><span className="eyebrow">حصن المسلم</span><h1>الأذكار</h1><p>{arabicNumber(adhkarDoors.length)} بابًا · {arabicNumber(adhkarDoors.reduce((n, d) => n + (d.count || d.items?.length || 0), 0))} ذكرًا</p></div><span className="heading-symbol">☾</span></div><div className="search-box"><Icon>⌕</Icon><input value={adhkarQuery} onChange={e => setAdhkarQuery(e.target.value)} placeholder="ابحث في أبواب الأذكار" /></div><div className="door-chips">{filtered.slice(0, 14).map((d, i) => <button className={(door?.id === d.id ? 'selected' : '')} key={d.id} onClick={() => setSelectedDoor(adhkarDoors.findIndex(x => x.id === d.id))}>{d.title}</button>)}</div>{door && <section className="door-card"><div className="door-heading"><span className="door-number">{arabicNumber(door.id)}</span><div><span className="eyebrow">الباب المختار</span><h2>{door.title}</h2></div><button onClick={() => door.audio_url && playUrl(door.audio_url, door.title)}>▶</button></div><div className="dhikr-list">{door.items?.map((item: AnyObj, index: number) => { const id = `${door.id}:${item.id || index}`; const done = completedAdhkar[id] || 0; const repeat = item.repeat || 1; return <article className={`dhikr-card ${done >= repeat ? 'done' : ''}`} key={id}><div className="dhikr-head"><span>{arabicNumber(index + 1)}</span><small>التكرار: {arabicNumber(repeat)}</small></div><p>{item.text}</p>{item.reference && <small className="reference">{item.reference}</small>}<div className="dhikr-actions"><button onClick={() => completeDhikr(id, repeat)}>{done >= repeat ? 'تم الذكر ✓' : `ذكرته ${arabicNumber(done)} / ${arabicNumber(repeat)}`}</button>{item.audio && <button className="secondary-button" onClick={() => playUrl(item.audio, door.title)}>استماع ▶</button>}</div></article> })}</div></section>}<img className="adhkar-footer" src="/assets/adhkar-footer.png" alt="أذكار ودعاء" /></>
  }

  function QuranDuasView() {
    return <><div className="page-heading"><div><span className="eyebrow">من أدعية القرآن</span><h1>أدعية قرآنية</h1><p>آيات جامعة للدعاء، مكتوبة داخل التطبيق ومتاحة دون اتصال</p></div><span className="heading-symbol">♡</span></div><section className="dua-intro"><img src="/assets/dua-person.png" alt="دعاء" /><div><strong>اجعل الدعاء رفيقك</strong><p>اختر دعاءً وتأمل معناه، واحفظه في مفضلتك للرجوع إليه.</p></div></section><div className="quran-dua-list">{quranDuas.map((dua, index) => <article className="quran-dua-card" key={dua.id}><div className="dua-card-head"><span>{arabicNumber(index + 1)}</span><button onClick={() => toggleCollection('favorites', `quran-dua:${dua.id}`)} className={favorites.includes(`quran-dua:${dua.id}`) ? 'active-gold' : ''} aria-label="إضافة إلى المفضلة">★</button></div><p>{dua.text}</p><small>{dua.reference}</small></article>)}</div></>
  }

  function TafsirView() {
    const surah = quran.find(s => s.number === tafsirSurah)
    return <><div className="page-heading"><div><span className="eyebrow">فهم كلام الله</span><h1>التفاسير</h1><p>اختر السورة والآية والتفسير</p></div><span className="heading-symbol">⌘</span></div><section className="form-card"><label>التفسير<select value={tafsirResource} onChange={e => setTafsirResource(Number(e.target.value))}>{tafsirResources.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}</select></label><label>السورة<select value={tafsirSurah} onChange={e => { setTafsirSurah(Number(e.target.value)); setTafsirAyah(1) }}>{quran.map(s => <option key={s.number} value={s.number}>{s.name}</option>)}</select></label><label>الآية<select value={tafsirAyah} onChange={e => setTafsirAyah(Number(e.target.value))}>{surah?.ayahs?.map((a: AnyObj) => <option key={a.number} value={a.number}>{arabicNumber(a.number)}</option>)}</select></label><button className="primary-button full" onClick={loadTafsir}>{tafsirLoading ? 'جارٍ التحميل...' : 'عرض التفسير'}</button></section>{surah && <article className="tafsir-ayah"><span>سورة {surah.name} · الآية {arabicNumber(tafsirAyah)}</span><p>{surah.ayahs?.find((a: AnyObj) => a.number === tafsirAyah)?.text}</p></article>}{tafsirText && <article className="tafsir-card"><div className="hadith-head"><span>نص التفسير</span><span className="source-pill">quran.com</span></div><p>{tafsirText}</p></article>}</>
  }

  function PrayerView() {
    return <><div className="page-heading"><div><span className="eyebrow">صلاتك أولًا</span><h1>مواقيت الصلاة</h1><p>احفظ مدينتك واعرض المواقيت بالحساب المناسب</p></div><span className="heading-symbol">◷</span></div><section className="form-card"><label>المدينة<input value={city} onChange={e => setCity(e.target.value)} placeholder="مكة المكرمة" /></label><button className="primary-button full" onClick={loadPrayer}>{prayerLoading ? 'جارٍ التحديث...' : 'تحديث المواقيت'}</button><small className="form-note">المصدر: Aladhan API · آخر تحديث يُحفظ على جهازك</small></section><div className="prayer-list">{prayerTimes.map(([name, time], index) => <div className={`prayer-row ${index === 0 ? 'next' : ''}`} key={name}><span className="prayer-dot">{index === 0 ? '◉' : '○'}</span><strong>{name}</strong><b>{time}</b></div>)}</div></>
  }

  function SettingsView() {
    return <><div className="page-heading"><div><span className="eyebrow">تجربتك</span><h1>الإعدادات</h1><p>خصص القراءة والاستماع كما تحب</p></div><span className="heading-symbol">⚙</span></div><section className="settings-card"><div className="setting-row"><div><strong>حجم خط القرآن</strong><small>اضبط حجم الآيات في شاشة المصحف</small></div><div className="stepper"><button onClick={() => { const n = Math.max(18, fontSize - 2); setFontSize(n); store('font-size', n) }}>−</button><b>{arabicNumber(fontSize)}</b><button onClick={() => { const n = Math.min(36, fontSize + 2); setFontSize(n); store('font-size', n) }}>+</button></div></div><div className="setting-row"><div><strong>المشغل المصغر</strong><small>إظهاره أسفل التطبيق أثناء الاستماع</small></div><button className={`switch ${showPlayer ? 'on' : ''}`} onClick={() => setShowPlayer(x => !x)}><i /></button></div><div className="setting-row"><div><strong>المفضلة والعلامات</strong><small>{arabicNumber(favorites.length)} مفضلة · {arabicNumber(bookmarks.length)} علامة محفوظة</small></div><button className="secondary-button" onClick={() => { setFavorites([]); setBookmarks([]); store('favorites', []); store('bookmarks', []) }}>مسح</button></div></section><section className="about-card"><img src="/assets/logo.png" alt="شعار يواقيت" /><h2>يَوَاقِيت</h2><p>المصحف والتلاوة والذكر في تجربة هادئة.</p><small>البيانات: quran.com · mp3quran · حصن المسلم · كتب الحديث</small></section></>
  }

  function renderContent() {
    if (loading) return <div className="loading-card"><div className="spinner" />جارٍ تجهيز المصحف والبيانات...</div>
    if (error) return <div className="loading-card error-card">{error}</div>
    if (tab === 'quran') return <QuranView />
    if (tab === 'quran-duas') return <QuranDuasView />
    if (tab === 'tasbeeh') return <TasbeehView />
    if (tab === 'reciters') return <RecitersView />
    if (tab === 'hadith') return <HadithView />
    if (tab === 'stories') return <StoriesView />
    if (tab === 'videos') return <VideosView />
    if (tab === 'adhkar') return <AdhkarView />
    if (tab === 'tafsir') return <TafsirView />
    if (tab === 'prayer') return <PrayerView />
    if (tab === 'settings') return <SettingsView />
    return <Home />
  }

  return <div className="app-shell"><Header /><main className="scroll-area">{renderContent()}</main><PlayerCard /><nav className="bottom-nav">{tabs.map(item => <button className={tab === item.id ? 'active' : ''} key={item.id} onClick={() => navigate(item.id)}><Icon>{item.icon}</Icon><span>{item.label}</span></button>)}<button className={moreTabs.some(x => x.id === tab) ? 'active' : ''} onClick={() => navigate(moreTabs.find(x => x.id === tab)?.id || 'settings')}><Icon>⋯</Icon><span>المزيد</span></button></nav></div>
}

export default App
import { createRoot } from 'react-dom/client'

createRoot(document.getElementById('root')!).render(<App />)
