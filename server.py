"""HighDusting.ca web server. Python 3.10+. Quote data stays outside public routes."""
import argparse, io, json, os, re, sqlite3, time, uuid, threading
from notifications import configure_database, send_pending, settings
from collections import defaultdict
from email.parser import BytesParser
from email.policy import default
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get('HIGHDUSTING_DATA_DIR', str(ROOT / '.data'))).resolve()
MAX_BODY = 51 * 1024 * 1024
rate = defaultdict(list)
notification_lock = threading.Lock()

def notify_quotes():
    if not notification_lock.acquire(blocking=False): return
    try: send_pending(DATA)
    finally: notification_lock.release()

def init():
    DATA.mkdir(parents=True, exist_ok=True, mode=0o700)
    (DATA/'uploads').mkdir(exist_ok=True, mode=0o700)
    with sqlite3.connect(DATA/'quotes.sqlite3') as db:
        db.execute('CREATE TABLE IF NOT EXISTS quotes (reference TEXT PRIMARY KEY, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, details TEXT NOT NULL, attachments TEXT NOT NULL)')
        configure_database(db)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        self.send_header('X-Frame-Options','DENY')
        super().end_headers()
    def json_response(self,code,data):
        body=json.dumps(data).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if any(part.startswith('.') for part in path.split('/') if part) or '..' in path.split('/'):
            return self.send_error(404)
        permitted = path in ['/', '/index.html','/styles.css','/app.js','/formspree.js','/favicon.svg','/robots.txt','/sitemap.xml','/404.html'] or path.startswith(('/assets/','/services/','/privacy/','/locations/','/industries/','/fr/','/guides/'))
        if not permitted: return self.not_found()
        target=(ROOT/path.lstrip('/')).resolve()
        if not target.is_relative_to(ROOT) or not target.exists(): return self.not_found()
        if target.is_dir() and not (target/'index.html').exists():return self.not_found()
        return super().do_GET()
    def do_HEAD(self):
        # Use the same allowlist as GET; suppress the response body.
        original=self.wfile;self.wfile=io.BytesIO()
        try:
            self.do_GET();raw=self.wfile.getvalue();original.write(raw.split(b'\r\n\r\n',1)[0]+b'\r\n\r\n')
        finally:self.wfile=original
    def not_found(self):
        body=(ROOT/'404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_POST(self):
        if self.path != '/api/quotes': return self.json_response(404,{'error':'Not found'})
        origin=self.headers.get('Origin')
        if origin and urlsplit(origin).netloc != self.headers.get('Host'):return self.json_response(403,{'error':'Please submit the form from this website.'})
        ip=self.client_address[0];now=time.time();rate[ip]=[t for t in rate[ip] if now-t<600]
        if len(rate[ip])>=10:return self.json_response(429,{'error':'Too many requests. Please wait a few minutes or call us.'})
        try:length=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.json_response(400,{'error':'Invalid request size.'})
        if length<=0 or length>MAX_BODY:return self.json_response(413,{'error':'Please upload no more than 5 files, 10 MB each.'})
        ct=self.headers.get('Content-Type','')
        if not ct.startswith('multipart/form-data;'):return self.json_response(400,{'error':'Please use the quote form.'})
        self.connection.settimeout(30)
        try:
            raw=self.rfile.read(length)
            if len(raw)!=length:raise ValueError('Incomplete upload. Please try again.')
            message=BytesParser(policy=default).parsebytes(('Content-Type: '+ct+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+raw)
            if not message.is_multipart():raise ValueError('Invalid form data.')
            fields={};files=[]
            for part in message.iter_parts():
                name=part.get_param('name',header='content-disposition');filename=part.get_filename();payload=part.get_payload(decode=True) or b''
                if filename:
                    if name!='photos':raise ValueError('Unexpected file field.')
                    if len(payload)>10*1024*1024:raise ValueError('Each file must be 10 MB or smaller.')
                    kind=part.get_content_type()
                    ext={'image/jpeg':'.jpg','image/png':'.png','image/webp':'.webp','video/mp4':'.mp4','video/quicktime':'.mov'}.get(kind)
                    valid= (kind=='image/jpeg' and payload.startswith(b'\xff\xd8\xff')) or (kind=='image/png' and payload.startswith(b'\x89PNG\r\n\x1a\n')) or (kind=='image/webp' and payload.startswith(b'RIFF') and payload[8:12]==b'WEBP') or (kind in ['video/mp4','video/quicktime'] and payload[4:8] in [b'ftyp',b'moov',b'wide'])
                    if not ext or not valid:raise ValueError('Please use valid JPG, PNG, WebP, MP4 or MOV files.')
                    files.append((Path(filename).name[:200],ext,payload))
                elif name and name!='photos':
                    if len(payload)>12000:raise ValueError('A field is too long.')
                    fields[name]=payload.decode('utf-8').strip()
            if len(files)>5:raise ValueError('Please select no more than 5 files.')
            for field in ['facility','city','areas','dust','name','company','email','phone']:
                if not fields.get(field):raise ValueError('Please complete all required fields.')
            if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',fields['email']):raise ValueError('Please enter a valid email address.')
            if len(re.sub(r'\D','',fields['phone']))<7:raise ValueError('Please enter a valid phone number.')
            if fields.get('area') and (not fields['area'].isdigit() or not 1<=int(fields['area'])<=100000000):raise ValueError('Please enter a valid facility area.')
            source=fields.get('source_page','/')
            if len(source)>512 or not source.startswith('/') or source.startswith('//') or any(ord(c)<32 for c in source):raise ValueError('Invalid originating page.')
            fields['source_page']=source
            origin_page=fields.get('originating_page',source)
            if len(origin_page)>512 or not origin_page.startswith('/') or origin_page.startswith('//') or any(ord(c)<32 for c in origin_page):raise ValueError('Invalid originating page.')
            fields['originating_page']=origin_page
            fields['selected_city']=fields['city']
            if len(fields.get('selected_service',''))>120:raise ValueError('Invalid service selection.')
            reference='HD-'+uuid.uuid4().hex[:10].upper();attachments=[];saved=[]
            try:
                for filename,ext,payload in files:
                    stored=reference+'-'+uuid.uuid4().hex+ext
                    p=DATA/'uploads'/stored;p.write_bytes(payload);p.chmod(0o600);saved.append(p)
                    attachments.append({'original_name':filename,'stored_name':stored,'size':len(payload)})
                with sqlite3.connect(DATA/'quotes.sqlite3') as db:
                    db.execute('INSERT INTO quotes(reference,details,attachments) VALUES(?,?,?)',(reference,json.dumps(fields),json.dumps(attachments)))
                    db.execute('INSERT INTO notification_outbox(reference) VALUES(?)',(reference,))
            except Exception:
                for p in saved:p.unlink(missing_ok=True)
                raise
            rate[ip].append(now)
            threading.Thread(target=notify_quotes,daemon=True).start()
            return self.json_response(201,{'reference':reference})
        except (ValueError,UnicodeError) as exc:return self.json_response(400,{'error':str(exc)})
        except Exception:return self.json_response(500,{'error':'Your request could not be saved. Please try again or call (833) 696-9996.'})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=int(os.environ.get('PORT','4321')));parser.add_argument('--host',default='127.0.0.1');args=parser.parse_args();init()
    print(f'HighDusting.ca running at http://{args.host}:{args.port}',flush=True)
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
