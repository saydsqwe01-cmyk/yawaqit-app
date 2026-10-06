from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
# Tafsir is not expanded automatically after API data arrives.
s=s.replace("S.tr=true;S.tf=true;S.reelPrompt=true;", "S.tr=true;S.tf=false;S.reelPrompt=true;")
s=s.replace("S.tf=true;render()}}catch(e){if(SUR[si])", "render()}}catch(e){if(SUR[si])")
old="${S.tf?`<div class=\"bx tf ${S.tfx[i]?'x':''}\"><div class=\"h\" style=\"direction:rtl\"><span style=\"display:flex;gap:6px;align-items:center\">${I('book','width:16px;height:16px')}${T('tafsir')}</span></div><p>الآية ${ar(i+1)}<br>${v[2]}</p><div style=\"text-align:left\"><button class=\"ib\" data-x=\"${i}\">${I('exp')}</button></div></div>`:''}"
new="${S.tfx[i]?`<div class=\"bx tf x\"><div class=\"h\" style=\"direction:rtl\"><span style=\"display:flex;gap:6px;align-items:center\">${I('book','width:16px;height:16px')}${T('tafsir')}</span><button class=\"tafsir-collapse\" data-x=\"${i}\" aria-label=\"${T('close')}\">${I('exp','width:15px;height:15px')}</button></div><p>الآية ${ar(i+1)}<br>${v[2]}</p></div>`:`<button class=\"tafsir-show\" data-x=\"${i}\">${I('book','width:15px;height:15px')}${T('tafsir')}</button>`}"
if old not in s: raise SystemExit('tafsir markup pattern not found')
s=s.replace(old,new)
# Small borderless controls for show/collapse.
s=s.replace('</style>', ".tafsir-show,.tafsir-collapse{border:0!important;background:transparent!important;box-shadow:none!important;color:var(--mut);font-size:10px;padding:3px 0;display:inline-flex;align-items:center;gap:4px;cursor:pointer}.tafsir-show{margin:3px 0}.tafsir-collapse{margin-inline-start:auto;color:var(--mut)}.tf p{max-height:none!important;overflow:visible!important}</style>",1)
p.write_text(s)
print('tafsir collapsed controls applied')
