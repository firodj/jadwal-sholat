#!/usr/bin/env python

from datetime import datetime, timedelta
from colorama import Fore, Style, init

try:
  from data import schedules
except ImportError:
  from bs4 import BeautifulSoup as Soup
  from bs4.element import Tag

  f = open('data.py', 'w')
  f.write("schedules = {\n")
  soup = Soup(open('data.xml').read())
  schedules = {}
  for data in soup.findAll('data'):
    schedule = {}
    fields = []
    for tag in data.children:
      if type(tag) != Tag:
        continue
      schedule[tag.name] = tag.text
      if not tag.name in ['year', 'month', 'date']:
        fields.append(tag.name)
    schedule_date = schedule.get('year','00') + schedule.get('month','00') + schedule.get('date','00')
    schedules[schedule_date] = schedule

    f.write('"' + schedule_date + '": {')
    for field in fields:
      f.write('"' + field + '": "' + schedule[field] + '", ')
    f.write("},\n")
  f.write("\n}\n")
  f.close()

def delta(today, hhmm):
  praytime = datetime.strptime(today + ' ' + hhmm, '%Y%m%d %H:%M')
  delta = praytime - datetime.now()
  return delta

today = datetime.now().strftime('%Y%m%d')
schedule = schedules.get(today)

if schedule:
  init()
  rows = [('isha','Isya'),('maghrib','Maghrib'),('ashr','Ashar'),('dzuhr','Dzuhur'),('fajr','Subuh')]
  nexts = {}

  nearest = None
  for row in rows:
    nearnext = delta(today, schedule[row[0]])
    nexts[row[0]] = nearnext

    if nearnext.days < 0:
      continue
    if nearest is None:
      nearest = row[0]
      continue
    if nexts[nearest] > nexts[row[0]]:
      nearest = row[0]

  print 'Jam:', datetime.now().strftime('%H:%I:%S %Y-%m-%d');
  for row in rows:
    if nearest == row[0]:
      print Fore.GREEN + Style.BRIGHT + row[1],
    else:
      print row[1],

    print schedule[row[0]],

    if nearest == row[0]:
      print nexts[row[0]], Fore.RESET + Style.RESET_ALL
    else:
      print
