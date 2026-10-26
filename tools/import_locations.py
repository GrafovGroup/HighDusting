"""Import StatCan table 98-10-0002-01 (2021 CSD geography), no live scraping needed for builds."""
import csv,io,json,zipfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
provinces=[('10','NL','newfoundland-and-labrador','Newfoundland and Labrador'),('11','PE','prince-edward-island','Prince Edward Island'),('12','NS','nova-scotia','Nova Scotia'),('13','NB','new-brunswick','New Brunswick'),('24','QC','quebec','Quebec'),('35','ON','ontario','Ontario'),('46','MB','manitoba','Manitoba'),('47','SK','saskatchewan','Saskatchewan'),('48','AB','alberta','Alberta'),('59','BC','british-columbia','British Columbia'),('60','YT','yukon','Yukon'),('61','NT','northwest-territories','Northwest Territories'),('62','NU','nunavut','Nunavut')]
lookup={p[0]:p for p in provinces}
z=zipfile.ZipFile(sys.argv[1]);rows=[]
division=''
for r in csv.DictReader(io.TextIOWrapper(z.open('98100002.csv'),encoding='utf-8-sig')):
 if r['DGUID'].startswith('2021A0003'):division=r['GEO']
 if not r['DGUID'].startswith('2021A0005'):continue
 uid=r['DGUID'][9:];p=lookup[uid[:2]];population=r['Population and dwelling counts (13): Population, 2021 [1]']
 rows.append({'id':uid,'name':r['GEO'],'province':p[1],'division':division,'population':int(population) if population else None})
(ROOT/'data/municipalities.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/provinces.json').write_text(json.dumps([dict(code=p[1],slug=p[2],name=p[3]) for p in provinces],indent=2))
print(f'Imported {len(rows)} census subdivisions across {len(provinces)} provinces/territories.')
