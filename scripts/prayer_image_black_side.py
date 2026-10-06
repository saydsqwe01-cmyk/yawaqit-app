from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
css='''.prayer-mosque-art{left:auto!important;right:10px!important;bottom:2px!important;width:158px!important;height:146px!important;transform:none!important;opacity:1!important;filter:grayscale(1) brightness(0)!important;z-index:1!important}.prayer-banner .pb-count,.prayer-banner .pb-loc,.prayer-banner .pb-badge{z-index:2!important}@media(max-width:480px){.prayer-mosque-art{right:5px!important;width:142px!important;height:132px!important}}'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
print('prayer mosque image moved right, enlarged, and blackened')
