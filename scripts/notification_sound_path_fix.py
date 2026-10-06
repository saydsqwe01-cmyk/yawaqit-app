from pathlib import Path
import shutil
root=Path('/home/ubuntu/work/yawaqit_extract')
shutil.copy2(root/'public/assets/audio/notify.mp3', root/'public/assets/notification-sound.mp3')
p=root/'index.html'
s=p.read_text().replace("/notification-sound.mp3","/assets/notification-sound.mp3")
p.write_text(s)
print('notification sound asset path fixed')
