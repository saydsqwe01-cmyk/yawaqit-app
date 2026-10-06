import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

const root = process.cwd()
const raw = join(root, 'android/app/src/main/res/raw')
mkdirSync(raw, { recursive: true })

const javaDir = join(root, 'android/app/src/main/java/com/yawaqit/app')
mkdirSync(javaDir, { recursive: true })
writeFileSync(join(javaDir, 'MainActivity.java'), `package com.yawaqit.app;
import android.os.Bundle;
import com.getcapacitor.BridgeActivity;
public class MainActivity extends BridgeActivity {
  @Override public void onCreate(Bundle state) { registerPlugin(YawaqitAdhanPlugin.class); super.onCreate(state); }
}
`)
writeFileSync(join(javaDir, 'YawaqitAdhanPlugin.java'), `package com.yawaqit.app;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import java.util.Calendar;
import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "YawaqitAdhan")
public class YawaqitAdhanPlugin extends Plugin {
  @PluginMethod
  public void schedule(PluginCall call) {
    try {
      JSArray prayers = call.getArray("prayers");
      AlarmManager alarm = (AlarmManager) getContext().getSystemService(Context.ALARM_SERVICE);
      for (int i = 0; i < prayers.length(); i++) {
        JSObject prayer = prayers.getJSObject(i);
        int hour = prayer.getInteger("hour", 0);
        int minute = prayer.getInteger("minute", 0);
        String name = prayer.getString("name", "الصلاة");
        Calendar at = Calendar.getInstance();
        at.set(Calendar.HOUR_OF_DAY, hour); at.set(Calendar.MINUTE, minute); at.set(Calendar.SECOND, 0); at.set(Calendar.MILLISECOND, 0);
        if (at.getTimeInMillis() <= System.currentTimeMillis()) at.add(Calendar.DAY_OF_YEAR, 1);
        Intent intent = new Intent(getContext(), AdhanReceiver.class).setAction("com.yawaqit.app.ADHAN");
        intent.putExtra("prayer", name); intent.putExtra("fajr", "الفجر".equals(name));
        PendingIntent pending = PendingIntent.getBroadcast(getContext(), 5100 + i, intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        alarm.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at.getTimeInMillis(), pending);
      }
      JSObject result = new JSObject(); result.put("scheduled", prayers.length()); call.resolve(result);
    } catch (Exception error) { call.reject("تعذر جدولة الأذان", error); }
  }

  @PluginMethod
  public void stop(PluginCall call) { getContext().sendBroadcast(new Intent("com.yawaqit.app.STOP_ADHAN")); call.resolve(); }
}
`)
writeFileSync(join(javaDir, 'AdhanReceiver.java'), `package com.yawaqit.app;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import androidx.core.app.NotificationCompat;

public class AdhanReceiver extends BroadcastReceiver {
  public static final String CHANNEL = "adhan_full_audio";
  @Override public void onReceive(Context context, Intent intent) {
    if ("com.yawaqit.app.STOP_ADHAN".equals(intent.getAction())) return;
    String prayer = intent.getStringExtra("prayer");
    Intent full = new Intent(context, AdhanActivity.class).putExtra("prayer", prayer).putExtra("fajr", intent.getBooleanExtra("fajr", false));
    full.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
    android.app.PendingIntent fullScreen = android.app.PendingIntent.getActivity(context, 6100, full, android.app.PendingIntent.FLAG_UPDATE_CURRENT | android.app.PendingIntent.FLAG_IMMUTABLE);
    NotificationManager manager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
    if (Build.VERSION.SDK_INT >= 26) manager.createNotificationChannel(new NotificationChannel(CHANNEL, "أذان الصلاة", NotificationManager.IMPORTANCE_HIGH));
    NotificationCompat.Builder n = new NotificationCompat.Builder(context, CHANNEL).setSmallIcon(com.yawaqit.app.R.mipmap.ic_launcher).setLargeIcon(android.graphics.BitmapFactory.decodeResource(context.getResources(), com.yawaqit.app.R.mipmap.ic_launcher)).setContentTitle("حان وقت صلاة " + prayer).setContentText("اضغط مرتين لإيقاف الأذان").setPriority(NotificationCompat.PRIORITY_MAX).setCategory(NotificationCompat.CATEGORY_ALARM).setOngoing(true).setAutoCancel(false).setFullScreenIntent(fullScreen, true);
    manager.notify(6100, n.build());
    try { context.startActivity(full); } catch (Exception ignored) {}
  }
}
`)
writeFileSync(join(javaDir, 'AdhanActivity.java'), `package com.yawaqit.app;

import android.app.Activity;
import android.os.Bundle;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.Window;
import android.view.WindowManager;
import android.widget.TextView;
import android.graphics.Color;
import android.media.MediaPlayer;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;

public class AdhanActivity extends Activity {
  private MediaPlayer player; private GestureDetector gesture; private BroadcastReceiver screenOff;
  @Override public void onCreate(Bundle state) { super.onCreate(state); getWindow().addFlags(WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED | WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON | WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON); if (android.os.Build.VERSION.SDK_INT >= 27) { getWindow().getDecorView().setSystemUiVisibility(0); setShowWhenLocked(true); setTurnScreenOn(true); }
    TextView view = new TextView(this); view.setText("يواقيت المسلم\\n\\nحان وقت صلاة " + getIntent().getStringExtra("prayer") + "\\n\\nاضغط مرتين لإيقاف الأذان"); view.setTextColor(Color.WHITE); view.setTextSize(22); view.setGravity(17); view.setBackgroundColor(Color.rgb(12, 30, 31)); setContentView(view);
    player = MediaPlayer.create(this, getIntent().getBooleanExtra("fajr", false) ? R.raw.adhan_fajr : R.raw.adhan_madina); if (player != null) { player.setLooping(true); player.start(); }
    gesture = new GestureDetector(this, new GestureDetector.SimpleOnGestureListener(){ @Override public boolean onDoubleTap(MotionEvent e){ stopAdhan(); return true; } }); view.setOnTouchListener((v,e)->gesture.onTouchEvent(e));
    screenOff = new BroadcastReceiver(){ @Override public void onReceive(Context c, Intent i){ stopAdhan(); } }; registerReceiver(screenOff, new IntentFilter(Intent.ACTION_SCREEN_OFF));
  }
  private void stopAdhan(){ if (player != null) { player.stop(); player.release(); player=null; } ((android.app.NotificationManager)getSystemService(NOTIFICATION_SERVICE)).cancel(6100); finish(); }
  @Override protected void onDestroy(){ if(screenOff!=null) try{unregisterReceiver(screenOff);}catch(Exception ignored){} if(player!=null){player.stop();player.release();player=null;} super.onDestroy(); }
}
`)

// Use the original Yawaqit logo for every launcher density generated in CI.
const logo = join(root, 'public/assets/logo.png')
for (const density of ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']) {
  const mipmap = join(root, `android/app/src/main/res/mipmap-${density}`)
  mkdirSync(mipmap, { recursive: true })
  for (const icon of ['ic_launcher.png', 'ic_launcher_round.png', 'ic_launcher_foreground.png']) {
    copyFileSync(logo, join(mipmap, icon))
  }
}

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
  'android.permission.USE_FULL_SCREEN_INTENT',
]
const marker = '    <uses-permission android:name="android.permission.INTERNET" />'
const additions = permissions
  .filter(permission => !manifest.includes(permission))
  .map(permission => `    <uses-permission android:name="${permission}" />`)
  .join('\n')
if (additions) manifest = manifest.replace(marker, `${marker}\n${additions}`)
const componentMarker = '    </application>'
const components = `    <receiver android:name=".AdhanReceiver" android:exported="false"><intent-filter><action android:name="com.yawaqit.app.ADHAN" /></intent-filter></receiver>\n    <activity android:name=".AdhanActivity" android:exported="false" android:showWhenLocked="true" android:turnScreenOn="true" android:excludeFromRecents="true" />\n`
if (!manifest.includes('.AdhanReceiver')) manifest = manifest.replace(componentMarker, `${components}${componentMarker}`)
writeFileSync(manifestPath, manifest)
const stringsPath = join(root, 'android/app/src/main/res/values/strings.xml')
let strings = readFileSync(stringsPath, 'utf8')
strings = strings.replace(/(<string name="app_name">)[^<]*/, '$1يواقيت المسلم')
strings = strings.replace(/(<string name="title_activity_main">)[^<]*/, '$1يواقيت المسلم')
writeFileSync(stringsPath, strings)
console.log(`[android] copied original logo, ${sounds.length} notification sounds, and set app name to يواقيت المسلم`)
