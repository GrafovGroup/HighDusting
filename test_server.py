import json, sqlite3, tempfile, threading, unittest
from unittest.mock import patch
import notifications
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from html.parser import HTMLParser
from urllib.parse import urlsplit
import server

class WebsiteTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();server.DATA=Path(cls.temp.name);server.init();cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.base=f'http://127.0.0.1:{cls.http.server_port}';threading.Thread(target=cls.http.serve_forever,daemon=True).start()
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.temp.cleanup()
 def request(self,path,data=None,headers=None):
  try:
   with urlopen(Request(self.base+path,data=data,headers=headers or {})) as r:return r.status,r.read()
  except HTTPError as r:return r.code,r.read()
 def submit(self,overrides=None,file=None):
  fields=dict(facility='Warehouse',city='Toronto, ON',areas='Test beams',dust='General dust',name='Test',company='Test',email='test@example.com',phone='4165550100');fields.update(overrides or {})
  boundary='TESTBOUNDARY';parts=[]
  for k,v in fields.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
  if file:
   name,mime,payload=file;parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="photos"; filename="{name}"\r\nContent-Type: {mime}\r\n\r\n'.encode()+payload+b'\r\n')
  parts.append(f'--{boundary}--\r\n'.encode());return self.request('/api/quotes',b''.join(parts),{'Content-Type':f'multipart/form-data; boundary={boundary}'})
 def test_quote_persistence_and_upload(self):
  image=(server.ROOT/'assets/overhead.webp').read_bytes();status,body=self.submit(file=('../../image.webp','image/webp',image));self.assertEqual(status,201);ref=json.loads(body)['reference']
  with sqlite3.connect(server.DATA/'quotes.sqlite3') as db:row=db.execute('SELECT details,attachments FROM quotes WHERE reference=?',(ref,)).fetchone()
  self.assertEqual(json.loads(row[0])['city'],'Toronto, ON');attachment=json.loads(row[1])[0];self.assertEqual(attachment['original_name'],'image.webp');self.assertEqual((server.DATA/'uploads'/attachment['stored_name']).read_bytes(),image)
 def test_missing_required(self):self.assertEqual(self.submit({'city':''})[0],400)
 def test_bad_email(self):self.assertEqual(self.submit({'email':'bad'})[0],400)
 def test_disguised_upload(self):self.assertEqual(self.submit(file=('bad.png','image/png',b'<script>bad</script>'))[0],400)
 def test_private_paths(self):
  for path in ['/.data/quotes.sqlite3','/server.py','/.git/config','/assets/../server.py','/api/quotes']:
   self.assertEqual(self.request(path)[0],404,path)
 def test_cross_origin(self):self.assertEqual(self.request('/api/quotes',b'bad',{'Origin':'https://other.example'})[0],403)
 def test_page_context_and_notification_outbox(self):
  status,body=self.submit({'city':'Montréal, QC','selected_service':'warehouse-high-dusting','source_page':'/services/warehouse-high-dusting/','originating_page':'/locations/quebec/montreal/'})
  self.assertEqual(status,201);ref=json.loads(body)['reference']
  with sqlite3.connect(server.DATA/'quotes.sqlite3') as db:
   details=json.loads(db.execute('SELECT details FROM quotes WHERE reference=?',(ref,)).fetchone()[0]);outbox=db.execute('SELECT status FROM notification_outbox WHERE reference=?',(ref,)).fetchone()
  self.assertEqual(details['selected_city'],'Montréal, QC');self.assertEqual(details['selected_service'],'warehouse-high-dusting');self.assertEqual(details['originating_page'],'/locations/quebec/montreal/');self.assertEqual(outbox[0],'pending')
 def test_invalid_originating_page(self):self.assertEqual(self.submit({'source_page':'https://example.com'})[0],400)
 def test_notification_failure_retains_request(self):
  status,body=self.submit();self.assertEqual(status,201);ref=json.loads(body)['reference']
  config={'HIGHDUSTING_SMTP_HOST':'smtp.example.com','HIGHDUSTING_SMTP_USER':'test','HIGHDUSTING_SMTP_PASSWORD':'test','HIGHDUSTING_EMAIL_FROM':'test@example.com','HIGHDUSTING_QUOTE_EMAIL':'test@example.com'}
  with patch('notifications.settings',return_value=config),patch('notifications.smtplib.SMTP_SSL',side_effect=RuntimeError('test failure')):
   result=notifications.send_pending(server.DATA)
  self.assertEqual(result['sent'],0)
  with sqlite3.connect(server.DATA/'quotes.sqlite3') as db:
   self.assertIsNotNone(db.execute('SELECT reference FROM quotes WHERE reference=?',(ref,)).fetchone());row=db.execute('SELECT status,attempts FROM notification_outbox WHERE reference=?',(ref,)).fetchone();self.assertEqual(row[0],'pending');self.assertGreaterEqual(row[1],1)
 def test_all_local_links(self):
  class Links(HTMLParser):
   def __init__(self):super().__init__();self.urls=[]
   def handle_starttag(self,tag,attrs):
    for key,val in attrs:
     if key in ['href','src'] and val and val.startswith('/'):self.urls.append(val)
  paths=set()
  for page in server.ROOT.rglob('*.html'):
   parser=Links();parser.feed(page.read_text());paths.update(urlsplit(url).path for url in parser.urls)
  for path in paths:self.assertEqual(self.request(path)[0],200,path)
if __name__=='__main__':unittest.main()
