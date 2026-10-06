from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
css='''.loading-orbit{width:50px!important;height:50px!important;margin-top:10px!important}.loading-orbit i{width:4px!important;height:4px!important;left:calc(50% - 2px)!important;top:-2px!important;transform-origin:2px 27px!important}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('loader orbit shrunk')
