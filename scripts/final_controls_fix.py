from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Font size must affect Quran/verse text only, not zoom the whole app or screen.
s=s.replace("#app{font-size:var(--fs,17px);zoom:var(--ui-scale,1)}", "#app{font-size:initial}")
s=s.replace("document.documentElement.style.setProperty('--ui-scale',String(S.fs/17));", "")
# Keep the reminder video compact on laptops/large screens while preserving the phone layout.
css="""
@media (min-width:901px){.reel-viewer-card{width:min(42vw,430px)!important}.reel-viewer-card .reel-ad-video{height:min(58vh,420px)!important;max-height:calc(92dvh - 72px)!important}}
@media (min-width:481px) and (max-width:900px){.reel-viewer-card{width:min(72vw,500px)!important}.reel-viewer-card .reel-ad-video{height:min(58vh,380px)!important}}
"""
s=s.replace('</style>',css+'</style>',1)
# Changing the voice immediately updates the active preference and previews the selected file.
s=s.replace("$('#adhanVoice').onchange=e=>{S.adhanVoice=e.target.value;saveNotifyPrefs()};", "$('#adhanVoice').onchange=e=>{S.adhanVoice=e.target.value;saveNotifyPrefs();previewAdhan('normal');settings()};")
s=s.replace("$('#fajrAdhanVoice').onchange=e=>{S.fajrAdhanVoice=e.target.value;saveNotifyPrefs()};", "$('#fajrAdhanVoice').onchange=e=>{S.fajrAdhanVoice=e.target.value;saveNotifyPrefs();previewAdhan('fajr');settings()};")
p.write_text(s)
print('font, reminder sizing, and adhan controls fixed')
