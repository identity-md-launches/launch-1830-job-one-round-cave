"""Local delivery checks, stdlib only. No external paths or network."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
from image_bytes import read_png

root=Path('.')
wall=Path('artifacts/line-2/wall-v20.png').read_bytes()
assert wall==Path('artifacts/line-2/wall.png').read_bytes()
w,h,pixels=read_png(wall)
assert (w,h)==(1254,1254)
record=json.loads(Path('dist/line-2/40.json').read_text())
assert set(record)=={'name','image','attributes'}
assert record['image']=='https://api.imd.fun/artifacts/'+hashlib.sha256(wall).hexdigest()
attrs=record['attributes']
assert all(set(a)=={'trait_type','value'} for a in attrs)
assert [a['trait_type'] for a in attrs]==['Cave','Wall','Number','Left behind','Meaning','One thing']
a={x['trait_type']:x['value'] for x in attrs}
assert a['Cave']=='Water' and a['Wall']=='Line 2' and type(a['Number']) is int and a['Number']==40
assert len(list(Path('dist/line-2').glob('*.json')))==40
preview=Path('dist/line-2/40.jpg').read_bytes()
assert preview[:2]==b'\xff\xd8' and preview[-2:]==b'\xff\xd9'
offset=2
jpeg_size=None
while offset<len(preview):
 assert preview[offset]==255
 marker=preview[offset+1]
 length=int.from_bytes(preview[offset+2:offset+4],'big')
 if marker==192:
  bits,jh,jw,channels=struct.unpack('>BHHB',preview[offset+4:offset+10])
  jpeg_size=(jw,jh)
  assert bits==8 and channels==3
  break
 offset+=2+length
assert jpeg_size==(512,512) and len(preview)<=100000
for directory in ('line-2','dist/line-2'):
 for f in Path(directory).rglob('*'):
  if f.is_file():
   # Existing files are not rewritten or evaluated against new-file size limits.
   if f.name in {'40.json','40.jpg','WALL-40.md','wall-review-40.json','check_delivery_40.py','finish_wall_40.py'} or 'contract-feasibility' in f.parts:
    assert f.stat().st_size<=100000, str(f)
goal=Path('line-2/GOAL.md').read_bytes()
p=subprocess.run(['git','show','HEAD:line-2/GOAL.md'],capture_output=True,check=True)
assert goal==p.stdout
p=subprocess.run(['git','diff','--name-only'],capture_output=True,text=True,check=True)
assert p.stdout.splitlines()==['line-2/USED.md'],p.stdout
p=subprocess.run(['git','ls-files','--others','--exclude-standard'],capture_output=True,text=True,check=True)
assert all(f.startswith(('line-2/','dist/line-2/','artifacts/line-2/')) for f in p.stdout.splitlines())
p=subprocess.run(['git','diff','--check'],capture_output=True,text=True)
assert p.returncode==0,p.stdout
review=json.loads(Path('line-2/wall-review-40.json').read_text())
assert review['sha256']==hashlib.sha256(wall).hexdigest()
assert review['outside_region_pixel_identical']
assert review['changed_pixels']+review['unchanged_pixels']==w*h
result={'passed':True,'wall':{'dimensions':[w,h],'format':'PNG','mode':'RGB','sha256':hashlib.sha256(wall).hexdigest()},'preview':{'dimensions':list(jpeg_size),'format':'JPEG','bytes':len(preview)},'record':40,'goal_unchanged':True,'older_tracked_files_unchanged_except_used_log':True,'scope_checked':True,'unmet_visual_requirements':review['unmet_visual_requirements'],'visual_review':'Human-directed model inspection recorded in wall-review-40.json; structural checks do not certify visual quality.'}
Path('line-2/check-results-40.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
