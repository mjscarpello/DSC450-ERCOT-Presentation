#!/usr/bin/env python3
"""Render Studio S native Canvas frames with a local Chromium browser.

No JS renderer reimplementation: uses the unchanged checkpoint's app/render.html,
core timebase/animation, and src/render/canvas.js. Requires Python Playwright,
Chromium and FFmpeg to produce MP4. Optional --images-only for 3 keyframes.
"""
import argparse,base64,http.server,functools,json,os,pathlib,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parent
NATIVE=pathlib.Path(os.environ.get('STUDIO_S_SOURCE',''))
if not (NATIVE/'app/render.html').exists(): raise SystemExit('Set STUDIO_S_SOURCE to Studio S source checkpoint root')
P=json.loads((ROOT/'pilot.sproj').read_text())
OUT=ROOT.parent/'native_render'
OUT.mkdir(exist_ok=True)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(NATIVE)))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
args=argparse.ArgumentParser();args.add_argument('--images-only',action='store_true');parsed=args.parse_args()
frames=[0,40,100] if parsed.images_only else list(range(150))
video=None
if not parsed.images_only:
    video=subprocess.Popen(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','image2pipe','-framerate','30',
      '-i','pipe:0','-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p',str(OUT/'S16_C03_NATIVE_STUDIOS_CANVAS.mp4')],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
urls={a['id']:'data:image/png;base64,'+base64.b64encode((ROOT/a['path']).read_bytes()).decode('ascii') for a in P['assets'] if a['type']=='image'}
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-gpu'])
    page=browser.new_page(viewport={'width':1280,'height':760},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content('<!doctype html><html><body style="margin:0"><canvas></canvas></body></html>')
    for script in ['src/core/timebase.js','src/core/animation.js','src/render/canvas.js']:
        page.add_script_tag(content=(NATIVE/script).read_text())
    loaded=page.evaluate('''async({project,urls})=>{
       window.project=project; window.images=await StudioS.loadImages(project,urls);
       const canvas=document.querySelector('canvas'); canvas.width=1280;canvas.height=760;
       return {images:[...window.images.keys()],canvas:[canvas.width,canvas.height]};
    }''',{'project':P,'urls':urls})
    print('renderer',loaded,flush=True)
    for i in frames:
        raw=page.evaluate('''(frame)=>{
            const canvas=document.querySelector('canvas');
            StudioS.drawFrame(canvas,window.project,frame,window.images,{captions:false});
            return canvas.toDataURL('image/png').split(',')[1];
        }''',i)
        data=base64.b64decode(raw)
        if i in (0,40,100):
            name={0:'01_original_chart.png',40:'02_markers_visible.png',100:'03_markers_and_bracket.png'}[i]
            (OUT/name).write_bytes(data)
        if video:video.stdin.write(data)
        if i in (0,40,100,149): print('frame',i,'done',flush=True)
    browser.close()
    if errors: raise RuntimeError('Native canvas browser errors: '+repr(errors))
finally:
    server.shutdown();server.server_close()
    if video:
        video.stdin.close(); ret=video.wait(timeout=30)
        if ret:raise RuntimeError('FFmpeg exit '+str(ret)+' '+video.stderr.read().decode()[-1000:])
print('finished',len(frames),'Studio S native Canvas frames',flush=True)
