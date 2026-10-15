#!/usr/bin/env python3
"""Add a restrained two-seed ochre mark to an RGB/RGBA PNG using only stdlib."""
import struct, sys, zlib

def read_png(path):
    b=open(path,'rb').read(); assert b[:8]==b'\x89PNG\r\n\x1a\n'; p=8; idat=bytearray()
    while p<len(b):
        n=struct.unpack('>I',b[p:p+4])[0]; t=b[p+4:p+8]; d=b[p+8:p+8+n]; p+=n+12
        if t==b'IHDR': w,h,dep,kind,co,fi,inter=struct.unpack('>IIBBBBB',d)
        elif t==b'IDAT': idat.extend(d)
    assert (dep,co,fi,inter)==(8,0,0,0) and kind in (2,6)
    ch=3 if kind==2 else 4; stride=w*ch; raw=zlib.decompress(idat); rows=[]; prev=bytearray(stride); p=0
    for _ in range(h):
        ft=raw[p]; p+=1; cur=bytearray(raw[p:p+stride]); p+=stride
        for i in range(stride):
            a=cur[i-ch] if i>=ch else 0; u=prev[i]
            if ft==1: cur[i]=(cur[i]+a)&255
            elif ft==2: cur[i]=(cur[i]+u)&255
            elif ft==3: cur[i]=(cur[i]+(a+u)//2)&255
        rows.append(cur); prev=cur
    return w,h,ch,rows
def write_png(path,w,h,ch,rows):
    def c(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    raw=b''.join(b'\0'+bytes(r) for r in rows); kind=2 if ch==3 else 6
    out=b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',w,h,8,kind,0,0,0))+c(b'IDAT',zlib.compress(raw,9))+c(b'IEND',b'')
    open(path,'wb').write(out)
def paint(rows,w,h,ch,cx,cy,rx,ry,col,alpha):
    n=0
    for y in range(max(0,cy-ry-3),min(h,cy+ry+4)):
      for x in range(max(0,cx-rx-3),min(w,cx+rx+4)):
        d=((x-cx)/rx)**2+((y-cy)/ry)**2
        if d<=1:
          a=alpha*(1 if d<.72 else (1-d)/.28); i=x*ch; old=tuple(rows[y][i:i+3]); new=tuple(round(old[k]*(1-a)+col[k]*a) for k in range(3))
          if new!=old: rows[y][i:i+3]=bytes(new); n+=1
    return n
def main(src,dst):
    w,h,ch,rows=read_png(src); before=[bytes(r) for r in rows]; cx,cy=int(w*.165),int(h*.715)
    paint(rows,w,h,ch,cx-25,cy,31,24,(164,91,35),.62); paint(rows,w,h,ch,cx+28,cy-3,27,23,(184,104,38),.62)
    for ox,oy,rx,ry in [(-28,35,42,5),(0,43,45,5),(30,34,34,5)]: paint(rows,w,h,ch,cx+ox,cy+oy,rx,ry,(42,31,20),.52)
    write_png(dst,w,h,ch,rows); print(f'{w}x{h} RGB={ch==3} changed_pixels={sum(a!=b for a,b in zip(before,rows))}')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: pair_seeds.py INPUT.png OUTPUT.png')
    main(sys.argv[1],sys.argv[2])
