from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
marker='</style>'
css="""
/* Keep the remembrance video notice visible below the header. The header stays clickable. */
.reel-prompt.reel-notice-wrap{z-index:520!important;top:72px!important;inset-inline-end:0!important;inset-inline-start:0!important}
.reel-notice{z-index:521!important;top:8px!important;right:14px!important;max-width:calc(100vw - 28px)!important}
"""
s=s.replace(marker,css+marker,1)
p.write_text(s)
print('video notice visibility fixed')
