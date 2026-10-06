import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

const root = process.cwd()
const raw = join(root, 'android/app/src/main/res/raw')
mkdirSync(raw, { recursive: true })

const sounds = [
  ['public/assets/audio/adhan-fajr.mp3', 'adhan_fajr.mp3'],
  ['public/assets/audio/adhan-madina.mp3', 'adhan_madina.mp3'],
  ['public/assets/audio/notify.mp3', 'notify.mp3'],
  ['public/assets/audio/click.mp3', 'click.mp3'],
  ['public/assets/audio/correct.mp3', 'correct.mp3'],
  ['public/assets/audio/high-score.mp3', 'high_score.mp3'],
]
for (const [source, target] of sounds) copyFileSync(join(root, source), join(raw, target))

const manifestPath = join(root, 'android/app/src/main/AndroidManifest.xml')
let manifest = readFileSync(manifestPath, 'utf8')
const permissions = [
  'android.permission.POST_NOTIFICATIONS',
  'android.permission.SCHEDULE_EXACT_ALARM',
  'android.permission.WAKE_LOCK',
  'android.permission.RECEIVE_BOOT_COMPLETED',
]
const marker = '    <uses-permission android:name="android.permission.INTERNET" />'
const additions = permissions
  .filter(permission => !manifest.includes(permission))
  .map(permission => `    <uses-permission android:name="${permission}" />`)
  .join('\n')
if (additions) manifest = manifest.replace(marker, `${marker}\n${additions}`)
writeFileSync(manifestPath, manifest)
console.log(`[android] copied ${sounds.length} notification sounds and updated permissions`)
