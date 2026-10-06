from pathlib import Path
p=Path('/home/ubuntu/work/yawaqit_extract/index.html')
s=p.read_text()
s=s.replace('.home-quick-grid button:last-child{grid-column:1 / -1;justify-self:center;width:calc(50% - 3px)!important}', '.grid.sm .tile:last-child{grid-column:1 / -1;justify-self:center;width:calc(50% - 4px)!important}')
p.write_text(s)
print('actual home audio tile centered')
