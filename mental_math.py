'''
Scripts to practice some of the "Secrets
of Mental Math" a book with techniques
written by Arthur T. Benjamin
'''
from numpy.random import choice, randint
import time
from random import randrange
from datetime import datetime
from datetime import timedelta

try:
  import androidhelper
  droid = androidhelper.Android()
except:
  droid = None

def say(text):
  if droid is not None:
    droid.ttsSpeak(text)
    print(text)
  else:
    print(text)

def date_time2calendar(dt):
  '''Convert month day year'''
  months = ['January', 'February',
            'March', 'April', 'May',
            'June', 'July', 'August',
            'September', 'October',
            'November', 'December']
  month = months[dt.month-1]
  return f'{month} {dt.day} {dt.year}'

def random_date(start, end):
  """
  This function will return a random
  datetime between two datetime objects.
  """
  delta = end - start
  day_secs = delta.days * 24 * 60 * 60
  int_delta = day_secs + delta.seconds
  random_second = randrange(int_delta)
  td = timedelta(seconds=random_second)
  return start + td

def floating_holiday(holiday, year):
  """
  Given a year and a holiday return the
  datetime object
  """
  if holiday['week'] == 5:
    return floating_last_day(holiday,
                              year)
  for k in range(1, 8):
    day = int((holiday['week']-1)*7 + k)
    dt = datetime(year, holiday['month'],
                  day)
    wkday = dt.weekday() + 1
    if wkday == holiday['weekday']:
      return dt
  raise Exception

def floating_last_day(holiday, year):
  """
  Given a year and a holiday return the
  datetime object representing the last
  day of the month with the given weekday
  """
  month = (holiday['month'] + 1) % 12
  weekday = holiday['weekday']
  for k in range(1, 8):
    dt = datetime(year, month, 1)
    day_secs = k * 24 * 60 * 60
    td = timedelta(seconds=day_secs)
    hol_dt = dt - td
    wkday = (hol_dt.weekday() + 1) % 7
    if wkday == weekday:
      return hol_dt
  raise Exception

def weekday(dt):
  '''get weekday'''
  days = ['Monday', 'Tuesday',
          'Wednesday', 'Thursday',
          'Friday', 'Saturday',
          'Sunday']
  return days[dt.weekday()]


def multiplication(num_problems=10,
                 pause=30, digits_1=2,
                 digits_2=2):
  '''Practice multiplication'''
  p1 = f'multiplication of {digits_1}'
  p2 = f'digit numbers by {digits_2}'
  p3 = 'digit numbers'
  say(f'{p1} {p2} {p3}')
  range1 = range(10**(digits_1-1),
                 10**digits_1)
  range2 = range(10**(digits_2-1),
                 10**digits_2)
  x = choice(range1, (num_problems, ),
             False)
  y = choice(range2, (num_problems, ),
             True)
  for k in range(num_problems):
    problem = f'{x[k]} times {y[k]}'
    say(f'What is {problem}')
    time.sleep(pause)
    say(f'{problem} equals {x[k]*y[k]}')

def addition(num_problems=10, pause=30,
             digits_1=2, digits_2=2):
  '''Practice Addition'''
  p1 = f'addition of {digits_1} digit'
  p2 = f'numbers by {digits_2} digit numbers'
  say(f'{p1} {p2}')
  range1 = range(10**(digits_1-1), 10**digits_1)
  range2 = range(10**(digits_2-1), 10**digits_2)
  x = choice(range1, (num_problems, ),
             False)
  y = choice(range2, (num_problems, ),
             False)
  for k in range(num_problems):
    problem = f'{x[k]} plus {y[k]}'
    say(f'What is {problem}')
    time.sleep(pause)
    say(f'{problem} equals {x[k]+y[k]}')

def subtraction(num_problems=10, pause=30,
                digits_1=2, digits_2=2):
  '''Practice subtraction'''
  p1 = f'subtraction of {digits_1} digit'
  p2 = f'numbers by {digits_2} digit numbers'
  say(f'{p1} {p2}')
  range1 = range(10**(digits_1-1), 10**digits_1)
  range2 = range(10**(digits_2-1), 10**digits_2)
  x = choice(range1, (num_problems, ),
             False)
  y = choice(range2, (num_problems, ),
             False)
  for k in range(num_problems):
    problem = f'{x[k]} minus {y[k]}'
    say(f'What is {problem}')
    time.sleep(pause)
    say(f'{problem} equals {x[k]-y[k]}')

def whole_roots(num_problems=10, pause=30,
                digits=2, n=2):
  '''
  Practice getting whole roots of n digit
  numbers
  '''
  p1 = f'whole {n} roots of {digits}'
  p2 = 'digit numbers'
  say(f'{p1} {p2}')
  rng = range(10**(digits-1), 10**digits)
  x = choice(rng, (num_problems, ), False)
  for k in range(num_problems):
    problem = f'{n} root of {x[k]**n}'
    say(f'What is the {problem}?')
    time.sleep(pause)
    say(f'The {problem} is {x[k]}')

def roots(num_problems=10, pause=30,
          digits=2, n=2):
  '''
  Practice getting approximate roots of n
  digit numbers
  '''
  p1 = f'{n} roots of {digits}'
  p2 = 'digit numbers'
  say(f'{p1} {p2}')
  rng = range(10**(digits-1), 10**digits)
  x = choice(rng, (num_problems, ), False)
  for k in range(num_problems):
    problem = f'{n} root of {x[k]}'
    say(f'What is the {problem}?')
    time.sleep(pause)
    say(f'The {problem} is {x[k]**(1.0/n)}')

def powers(num_problems=10, pause=30,
           digits=2, n=2):
  '''Practice exponentiation'''
  p1 = f'{n} powers of {digits}'
  p2 = 'digit numbers'
  say(f'{p1} {p2}')
  rng = range(10**(digits-1), 10**digits)
  x = choice(rng, (num_problems, ), False)
  for k in range(num_problems):
    problem = f'{x[k]} to the power of {n}'
    say(f'What is {problem}?')
    time.sleep(pause)
    say(f'{problem} equals {x[k]**(n)}')

def calendar_days(num_problems=10,
                  pause=30):
  '''
  Practice: given a date produce the day
  of the week
  '''
  say('days of the week')
  start = datetime(1780, 1, 1)
  end = datetime(2050, 1, 1)
  dates = []
  for k in range(num_problems):
    dates.append(random_date(start, end))
  for date in dates:
    caldt = date_time2calendar(date)
    say(f'What day of the week was {caldt}?')
    time.sleep(pause)
    say(f'{caldt} was a {weekday(date)}')

def floating_holidays(num_problems=2,
                      pause=30,
                      practice_holidays=[]):
  '''
  Practice: given a floating holiday and
  the year produce the day of the month
  '''
  say('floating holidays')
  holidays = [
  {'holiday': 'Thanksgiving',
   'weekday': 4, 'week': 4, 'month': 11},
  {'holiday': 'Martin Luther King Junior',
   'weekday': 1, 'week': 3, 'month': 1},
  {'holiday': 'Presidents',
   'weekday': 1, 'week': 3, 'month': 2},
  {'holiday': 'Memorial',
   'weekday': 1, 'week': 5, 'month': 5},
  {'holiday': 'Labor',
   'weekday': 1, 'week': 1, 'month': 9},
  {'holiday': 'Columbus',
   'weekday': 1, 'week': 2, 'month': 10},
  ]
  if len(practice_holidays) > 0:
      holidays = [h for h in holidays
            if h['holiday'] in
            practice_holidays]
  years = range(1780, 2050)
  rng = range(len(holidays))
  x = choice(rng, (num_problems, ))
  for k in x:
    holiday = holidays[k]
    year = choice(years, (1,))[0]
    dt = floating_holiday(holiday, year)
    h = f'{holiday["holiday"]} Day of {year}'
    say(f'What day of the month was {h}')
    time.sleep(pause)
    calendar_date = date_time2calendar(dt)
    say(f'{h} was {calendar_date}')
# Thanksgiving 4th Thursday
# Martin Luther King Jr Day 3rd Monday in January
# Presidents Day 3rd Monday in February
# Memorial day last Monday in May
# Labor day first Monday in September
# Columbus day 2nd Monday in October

def modulo(num_problems=10, pause=30,
           digits=6, modulo=9):
  ''' Practice modulo '''
  say('modulo ' + str(modulo))
  start = 10**(digits-1)
  end = 10**digits
  for k in range(num_problems):
    n = randint(start, end)
    problem = f'{n} modulo {modulo}'
    say(f'What is {problem}')
    time.sleep(pause)
    say(f'{problem} is {n % modulo}')

def pegs(num_problems=10,
         n_digits=2,
         pause=5):
  #TODO give sounds/words not ready
  say('major system pegs')
  smallest = 10**(n_digits-1)
  largest = 10**(n_digits)-1
  ns = randint(smallest,
               largest,
               (num_problems,))
  for n in ns:
    say(f'Peg {n}')
    time.sleep(pause)
    say(f'Pegged {n}')

def peg(num_problems=10,
        pause=5):
  #TODO get working
  say('major system pegs')
  for k in range(num_problems):
    ops = randint(0, 10, (10, 2))
    for x, y in ops:
      say('Peg ' + str(x*10+y))
      time.sleep(pause)
    say('The complete number is:')
    time.sleep(pause)
    digits = [f'{x} {y}' for x, y in ops]
    say(' '.join(digits))

def memorize(num_problems=10,
             pause=5):
  #TODO get working
  say('major system pegs')
  for k in range(num_problems):
    ops = randint(0, 10, (10, 2))
    for x, y in ops:
      say('Peg ' + str(x*10+y))
      time.sleep(pause)
    say('The complete number is:')
    time.sleep(pause)
    digits = [f'{x} {y}' for x, y in ops]
    say(' '.join(digits))

if __name__ == '__main__':
  #pegs(1)
  calendar_days(num_problems=10, pause=20)
  floating_holidays(num_problems=10,
      pause=30)
  #floating_holidays(num_problems=10,
  # pause=30,
  # practice_holidays=[
  # 'Memorial'])
  #floating_holidays(num_problems=10,
  # pause=30,
  # practice_holidays=[
  # 'Columbus',
  # 'Presidents',
  # 'Martin Luther King Junior'])
  #modulo(num_problems=2, pause=30,
  # digits=6, modulo=9)
  #whole_roots(num_problems=2, pause=10,
  # digits=2, n=3)
  #whole_roots(num_problems=2, pause=10,
  # digits=2, n=2)
  #roots(num_problems=2, pause=10,
  # digits=2, n=2)
  #roots(num_problems=2, pause=10,
  # digits=2, n=3)
  #powers(num_problems=2, pause=30,
  # digits_1=2, digits_2=2)
  #powers(num_problems=2, pause=30,
  # digits_1=2, digits_2=3)
  #calendar_days(num_problems=2, pause=30)
  #memorize(num_problems=2, pause=5)
  #multiplication(num_problems=2, pause=10,
  # digits_1=2, digits_2=1)
  #subtraction(num_problems=2, pause=10,
  # digits_1=2, digits_2=1)
  #addition(num_problems=2, pause=10,
  # digits_1=2, digits_2=1)


# vim: set ts=2 sts=2 et sw=2 ft=python:

