"""Transfer generated pigment only, retaining the verified ancestor elsewhere."""
import hashlib
import json
from pathlib import Path
from image_bytes import read_png, png, resize, jpeg

base=Path('artifacts/line-2/wall.png')
output=Path('artifacts/line-2/wall-v20.png')
ancestor,draft=base.read_bytes(),output.read_bytes()
assert hashlib.sha256(ancestor).hexdigest()=='a91f846165af91e1fe721eeb7861e790f6440bc3d438c6ffe1c83c3a8180704d'
w,h,old=read_png(ancestor)
dw,dh,generated=read_png(draft)
assert (w,h)==(1254,1254) and (dw,dh)==(1024,1024)
x0,y0,width,height=540,220,110,110
sx0,sy0,sw,sh=170,175,700,680
final=bytearray(old)
changed=0
for y in range(y0,y0+height):
    for x in range(x0,x0+width):
        i=(y*w+x)*3
        rock=old[i:i+3]
        sx=sx0+(x-x0)*sw//width
        sy=sy0+(y-y0)*sh//height
        j=(sy*dw+sx)*3
        r,g,b=generated[j:j+3]
        if max(rock)<55 or (x*19+y*31)%17<3:
            continue
        charcoal=max(r,g,b)<105
        ochre=r>1.6*g and 30<g<140 and b<g*.8 and sy<440
        if charcoal or ochre:
            pigment=(39,28,19) if charcoal else (150,64,29)
            alpha=.58 if charcoal else .52
            for c in range(3):
                final[i+c]=round(rock[c]*(1-alpha)+pigment[c]*alpha)
            changed+=final[i:i+3]!=old[i:i+3]
assert 500<changed<width*height
for y in range(h):
    for x in range(w):
        i=(y*w+x)*3
        if final[i:i+3]!=old[i:i+3]:
            assert x0<=x<x0+width and y0<=y<y0+height
            assert max(old[i:i+3])>=55
encoded=png(w,h,final)
base.write_bytes(encoded)
output.write_bytes(encoded)
preview=jpeg(512,512,resize(w,h,final),52)
assert len(preview)<100000
Path('dist/line-2/40.jpg').write_bytes(preview)
review={'number':40,'ancestor_sha256':hashlib.sha256(ancestor).hexdigest(),
 'sha256':hashlib.sha256(encoded).hexdigest(),
 'wall':{'paths':[str(base),str(output)],'width':w,'height':h,'format':'PNG','mode':'RGB','bytes':len(encoded)},
 'preview':{'path':'dist/line-2/40.jpg','width':512,'height':512,'format':'JPEG','bytes':len(preview)},
 'addition_region':{'x':x0,'y':y0,'width':width,'height':height},
 'changed_pixels':changed,'unchanged_pixels':w*h-changed,
 'outside_region_pixel_identical':True,'dark_cracks_preserved':True,
 'generation_tool':'mcp__image__generate_image','draft_sha256':hashlib.sha256(draft).hexdigest(),
 'generated_dimensions':[dw,dh],'draft_retained':False,
 'generation_prompt':'An isolated small prehistoric cave pigment motif, centered on plain warm light tan stone: a charcoal bowl with two inward sloping sides that meet at the bottom, and a single red ochre pebble held above the narrow opening. Primitive flat burnt-stick lines, uneven worn hand-daubed earth pigments, Lascaux cave art. This symbolizes discovering a container cannot admit its promised stone. Only the bowl and pebble, simple distinct strokes occupying central half. No frogs or people or hands. No writing, letters, numbers, mathematical symbols, watermarks, logos, border or frame. No photographic objects or 3D shading.',
 'compositing':'Transferred only generated charcoal and ochre pigment to unused upper-center stone. Generated rock discarded.',
 'visual_review':'pending final inspection',
 'unmet_visual_requirements':['Inherited hands are too indistinct to certify five digits; no hands or handprints added. Inherited photographic rock retained to preserve the ancestor.']}
Path('line-2/wall-review-40.json').write_text(json.dumps(review,indent=2)+'\n')
record={'name':'Room for the Stone','image':'https://api.imd.fun/artifacts/'+review['sha256'],
 'attributes':[{'trait_type':k,'value':v} for k,v in [
 ('Cave','Water'),('Wall','Line 2'),('Number',40),
 ('Left behind','Offline JSON contract feasibility preflight'),
 ('Meaning','Pepe checks whether the promised stone has any place in its bowl.'),
 ('One thing','offline JSON structural contract checking')]]}
Path('dist/line-2/40.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(review,indent=2))
