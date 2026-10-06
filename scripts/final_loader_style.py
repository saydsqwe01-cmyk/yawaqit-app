from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
css='''.loading-brand-logo{filter:grayscale(1) brightness(0)!important}.loading-brand-name{font-family:'Amiri','Times New Roman',serif!important;font-size:22px!important;font-weight:700!important;letter-spacing:0!important;color:#000!important}.loading-orbit{width:68px!important;height:68px!important}.loading-orbit i{width:5px!important;height:5px!important;left:calc(50% - 2.5px)!important;top:-3px!important;transform-origin:2.5px 37px!important}.loading-orbit i:nth-child(n){background:#000!important;box-shadow:none!important}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('final loader style applied')
