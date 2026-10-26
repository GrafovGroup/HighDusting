"""Local-only quote review/export. Does not publish personal data."""
import argparse,json,sqlite3
from pathlib import Path
from server import DATA
p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True);sub.add_parser('list');sub.add_parser('report');ex=sub.add_parser('export');ex.add_argument('reference');ex.add_argument('output');args=p.parse_args()
if not (DATA/'quotes.sqlite3').exists():p.error('No quote database exists yet.')
with sqlite3.connect(DATA/'quotes.sqlite3') as db:
 if args.command=='list':
  for ref,date,details in db.execute('SELECT reference,created_at,details FROM quotes ORDER BY created_at DESC'):
   d=json.loads(details);print(f"{ref} | {date} | {d.get('company')} | {d.get('city')}")
 elif args.command=='report':
  from collections import Counter
  records=[json.loads(row[0]) for row in db.execute('SELECT details FROM quotes')]
  for key in ['selected_city','selected_service','source_page','originating_page']:
   print('\n'+key)
   for value,count in Counter(d.get(key) or '(not recorded)' for d in records).most_common():print(f'{count:5}  {value}')
 else:
  row=db.execute('SELECT reference,created_at,details,attachments FROM quotes WHERE reference=?',(args.reference,)).fetchone()
  if not row:p.error('Reference not found.')
  target=Path(args.output)
  with target.open('x') as f:json.dump(dict(reference=row[0],created_at=row[1],details=json.loads(row[2]),attachments=json.loads(row[3])),f,indent=2)
  target.chmod(0o600);print(f'Exported to {target.resolve()}')
