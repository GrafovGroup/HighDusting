"""Durable quote notification outbox. Recipient and sender must be configured explicitly."""
import argparse,json,os,re,smtplib,sqlite3,ssl,time,uuid
from email.message import EmailMessage
from pathlib import Path

DEFAULT_QUOTE_EMAIL = "info@highdusting.ca"

def configure_database(db):
 db.execute('CREATE TABLE IF NOT EXISTS notification_outbox (reference TEXT PRIMARY KEY REFERENCES quotes(reference), status TEXT NOT NULL DEFAULT "pending", attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT, delivered_at TEXT)')

def settings():
 keys=['HIGHDUSTING_SMTP_HOST','HIGHDUSTING_SMTP_USER','HIGHDUSTING_SMTP_PASSWORD','HIGHDUSTING_EMAIL_FROM']
 if not all(os.environ.get(k) for k in keys):return None
 result={k:os.environ[k] for k in keys}
 result['HIGHDUSTING_QUOTE_EMAIL']=os.environ.get('HIGHDUSTING_QUOTE_EMAIL') or DEFAULT_QUOTE_EMAIL
 for key in ['HIGHDUSTING_EMAIL_FROM','HIGHDUSTING_QUOTE_EMAIL']:
  if not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',result[key]):raise ValueError('Invalid notification address configuration')
 return result

def send_pending(data_dir,limit=20):
 config=settings()
 if not config:return {'sent':0,'configured':False}
 sent=0
 with sqlite3.connect(Path(data_dir)/'quotes.sqlite3',timeout=15) as db:
  configure_database(db)
  # This local worker is single-run; records remain pending after provider failure.
  rows=db.execute('SELECT o.reference,q.details FROM notification_outbox o JOIN quotes q ON q.reference=o.reference WHERE o.status="pending" ORDER BY q.created_at LIMIT ?',(limit,)).fetchall()
  for reference,raw in rows:
   details=json.loads(raw);message=EmailMessage();message['Subject']='New HighDusting.ca quote request '+reference;message['From']=config['HIGHDUSTING_EMAIL_FROM'];message['To']=config['HIGHDUSTING_QUOTE_EMAIL'];message['Message-ID']=f'<{reference}@highdusting.ca>'
   lines=[f'New quote request: {reference}',f'Company: {details.get("company","")}',f'Contact: {details.get("name","")}',f'Email: {details.get("email","")}',f'Phone: {details.get("phone","")}',f'Location: {details.get("city","")}',f'Service: {details.get("selected_service","")}',f'Originating page: {details.get("source_page","")}','', 'Full scope and private uploads are retained in the quote database.']
   message.set_content('\n'.join(lines))
   try:
    with smtplib.SMTP_SSL(config['HIGHDUSTING_SMTP_HOST'],int(os.environ.get('HIGHDUSTING_SMTP_PORT','465')),context=ssl.create_default_context(),timeout=20) as smtp:
     smtp.login(config['HIGHDUSTING_SMTP_USER'],config['HIGHDUSTING_SMTP_PASSWORD']);smtp.send_message(message)
    db.execute('UPDATE notification_outbox SET status="sent",attempts=attempts+1,last_error=NULL,delivered_at=CURRENT_TIMESTAMP WHERE reference=?',(reference,));sent+=1
   except Exception as exc:
    db.execute('UPDATE notification_outbox SET attempts=attempts+1,last_error=? WHERE reference=?',(type(exc).__name__,reference))
   db.commit()
 return {'sent':sent,'configured':True}

if __name__=='__main__':
 from server import DATA
 parser=argparse.ArgumentParser();parser.add_argument('--send-pending',action='store_true');args=parser.parse_args()
 if args.send_pending:print(json.dumps(send_pending(DATA)))
 else:print('Notification sender configured.' if settings() else f'Quote recipient: {DEFAULT_QUOTE_EMAIL}. Mail-provider sending settings are still required; requests remain saved in the outbox.')
