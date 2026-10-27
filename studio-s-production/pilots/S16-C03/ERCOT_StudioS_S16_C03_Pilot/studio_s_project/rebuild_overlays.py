#!/usr/bin/env python3
"""Rebuild the two transparent highlight overlays from this pilot's D05.png.

Source chart must match cue_geometry.json SHA256; output coordinates are in
source pixels. Font rendering may differ by OS; use the included PNGs as the
version-locked authoritative approved assets.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent

def font(size,bold=False,custom=None):
    if custom:return ImageFont.truetype(custom,size)
    names=('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
           '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf')
    for name in names:
        if Path(name).is_file():return ImageFont.truetype(name,size)
    return ImageFont.load_default()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--font',help='Optional TTF font for matching typography');args=ap.parse_args()
    cue=json.loads((ROOT.parent/'cue_geometry.json').read_text())
    original=ROOT/'assets/D05.png'
    if hashlib.sha256(original.read_bytes()).hexdigest()!=cue['source_sha256']:
        raise SystemExit('Source chart SHA256 mismatch; review data and remeasure before export')
    im=Image.open(original)
    obs=cue['targets'][0]['source_xy_px'];hyb=cue['targets'][1]['source_xy_px']
    marks=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(marks)
    for cx,cy in [obs,hyb]:
        d.ellipse((cx-7,cy-7,cx+7,cy+7),fill=(255,255,255,246),outline=(34,91,141,245),width=4)
    marks.save(ROOT/'assets/S16_C03_markers.png')
    bracket=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(bracket)
    red=(201,65,43,255); x=cue['targets'][2]['source_x_px']; top=obs[1];bottom=hyb[1]
    d.line((x,top,x,bottom),fill=red,width=4)
    d.line((x-12,top,x+12,top),fill=red,width=4)
    d.line((x-12,bottom,x+12,bottom),fill=red,width=4)
    label='6,504 MWh underforecast'; f=font(19,True,args.font)
    pos=(1000,81); bb=d.textbbox(pos,label,font=f,stroke_width=0)
    d.rounded_rectangle((bb[0]-11,bb[1]-7,bb[2]+11,bb[3]+7),radius=7,
                        fill=(255,255,255,240),outline=red,width=2)
    d.text(pos,label,font=f,fill=red)
    bracket.save(ROOT/'assets/S16_C03_bracket.png')
    for entry in cue['media']:
        fp=ROOT/'assets'/entry['file']
        digest=hashlib.sha256(fp.read_bytes()).hexdigest()
        print(entry['file'], 'SAME' if digest==entry['sha256'] else 'CHANGED (review required)')

if __name__=='__main__':main()
