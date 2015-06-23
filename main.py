from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
import time

today = time.strftime('%Y%m%d')

soup = Soup(open('data.xml').read())
schedules = {}
for data in soup.findAll('data'):
  schedule = {}
  for tag in data.children:
    if type(tag) != Tag:
      continue
    schedule[tag.name] = tag.text
  schedule_date = schedule.get('year','00') + schedule.get('month','00') + schedule.get('date','00')
  schedules[schedule_date] = schedule

  if schedule_date == today:
    print 'Jam:', time.strftime('%H:%I:%S');
    print 'Tanggal:', schedule_date
    print 'Magrib ', schedule['maghrib']
    print 'Ashar  ', schedule['ashr']
    print 'Dzhuhur', schedule['dzuhr']
    print 'Shubuh ', schedule['fajr']
    break
