import { Capacitor } from '@capacitor/core'
import { Geolocation } from '@capacitor/geolocation'
import { LocalNotifications } from '@capacitor/local-notifications'

type PrayerInput = { name: string; hour: number; minute: number }
type ScheduleOptions = { dailyHour?: number; dailyEnabled?: boolean }

const CHANNELS = [
  { id: 'prayer_fajr', name: 'أذان الفجر', description: 'إشعار أذان الفجر بصوت مستقل', sound: 'adhan_fajr.mp3' },
  { id: 'prayer_makkah', name: 'أذان الصلوات', description: 'إشعارات الظهر والعصر والمغرب والعشاء', sound: 'adhan_madina.mp3' },
  { id: 'daily_dhikr', name: 'تذكير الذكر', description: 'تذكير يومي بالذكر', sound: 'notify.mp3' },
  { id: 'quran_reading', name: 'ورد القرآن', description: 'تذكير ورد القرآن', sound: 'correct.mp3' },
  { id: 'hadith_reminder', name: 'حديث اليوم', description: 'تذكير بحديث اليوم', sound: 'click.mp3' },
]

const nativeAvailable = () => Capacitor.getPlatform() === 'android' || Capacitor.getPlatform() === 'ios'

async function requestNativePermissions() {
  try {
    const [geo, notifications] = await Promise.allSettled([
      Geolocation.requestPermissions({ permissions: ['location'] }),
      LocalNotifications.requestPermissions(),
    ])
    if (nativeAvailable() && notifications.status === 'fulfilled' && notifications.value.display === 'granted') {
      await Promise.allSettled(CHANNELS.map(channel => LocalNotifications.createChannel({
        ...channel,
        importance: 5,
        visibility: 1,
        vibration: true,
        lights: true,
        lightColor: '#C99B45',
      })))
    }
    console.info('[Yawaqit] native permissions requested', {
      location: geo.status === 'fulfilled' ? geo.value.location : 'unavailable',
      notifications: notifications.status === 'fulfilled' ? notifications.value.display : 'unavailable',
    })
  } catch (error) {
    console.warn('[Yawaqit] native permission request skipped', error)
  }
}

function nextAt(hour: number, minute: number) {
  const at = new Date()
  at.setHours(hour, minute, 0, 0)
  return at
}

async function schedulePrayerNotifications(prayers: PrayerInput[], options: ScheduleOptions = {}) {
  if (!nativeAvailable()) return { scheduled: false, reason: 'web' }
  try {
    const permission = await LocalNotifications.checkPermissions()
    if (permission.display !== 'granted') return { scheduled: false, reason: 'permission' }
    await Promise.allSettled(CHANNELS.map(channel => LocalNotifications.createChannel({
      ...channel, importance: 5, visibility: 1, vibration: true, lights: true, lightColor: '#C99B45',
    })))
    const notifications: any[] = prayers.slice(0, 5).map((prayer, index) => ({
      id: 4100 + index,
      title: `حان الآن وقت صلاة ${prayer.name}`,
      body: prayer.name === 'الفجر' ? 'الصلاة خير من النوم · يواقيت' : 'حي على الصلاة · تقبل الله طاعتكم',
      channelId: prayer.name === 'الفجر' ? 'prayer_fajr' : 'prayer_makkah',
      sound: prayer.name === 'الفجر' ? 'adhan_fajr.mp3' : 'adhan_madina.mp3',
      schedule: { at: nextAt(prayer.hour, prayer.minute), repeats: true, allowWhileIdle: true },
      autoCancel: true,
      extra: { type: 'prayer', prayer: prayer.name },
    }))
    const dailyHour = Math.max(0, Math.min(23, Number(options.dailyHour ?? 10)))
    if (options.dailyEnabled !== false) {
      notifications.push(
        { id: 4201, title: 'تذكير الذكر', body: 'سبحان الله وبحمده، سبحان الله العظيم', channelId: 'daily_dhikr', sound: 'notify.mp3', schedule: { at: nextAt(dailyHour, 0), repeats: true, allowWhileIdle: true }, autoCancel: true, extra: { type: 'dhikr' } },
        { id: 4202, title: 'ورد القرآن', body: 'حان وقت وردك من القرآن الكريم', channelId: 'quran_reading', sound: 'correct.mp3', schedule: { at: nextAt((dailyHour + 4) % 24, 0), repeats: true, allowWhileIdle: true }, autoCancel: true, extra: { type: 'quran' } },
        { id: 4203, title: 'حديث اليوم', body: 'افتح يواقيت لقراءة حديث صحيح', channelId: 'hadith_reminder', sound: 'click.mp3', schedule: { at: nextAt((dailyHour + 10) % 24, 0), repeats: true, allowWhileIdle: true }, autoCancel: true, extra: { type: 'hadith' } },
      )
    }
    await LocalNotifications.cancel({ notifications: notifications.map(notification => ({ id: notification.id })) })
    const result = await LocalNotifications.schedule({ notifications })
    console.info('[Yawaqit] scheduled background prayer notifications', result)
    return { scheduled: true, count: notifications.length }
  } catch (error) {
    console.warn('[Yawaqit] background notification scheduling failed', error)
    return { scheduled: false, reason: 'error' }
  }
}

if (typeof window !== 'undefined') {
  ;(window as any).YawaqitNative = { requestNativePermissions, schedulePrayerNotifications }
  const start = () => { void requestNativePermissions() }
  if (document.readyState === 'loading') window.addEventListener('DOMContentLoaded', start, { once: true })
  else start()
}

export { requestNativePermissions, schedulePrayerNotifications }
