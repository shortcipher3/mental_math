'''
Scripts to practice some of the "Secrets
of Mental Math" a book with techniques
written by Arthur T. Benjamin
'''
import math
from numpy.random import choice, randint
import numpy as np
import time
from random import randrange
from datetime import datetime
from datetime import timedelta
import json

try:
  import androidhelper
  droid = androidhelper.Android()
except:
  droid = None

def say(text):
  if droid is not None:
    droid.ttsSpeak(text)
    speakingEnd = droid.ttsIsSpeaking().result
    while speakingEnd:
      speakingEnd = droid.ttsIsSpeaking().result
  else:
    print(text)

class ProblemInterface:

  def __init__(self, pause, **kwargs):
    self.pause = pause

  #* init, pause, any selection, which holidays, date range
  def human_readable(self) -> (str, str):
    raise NotImplementedError("Inheriting class needs to implement this")

  def generate_quiz(num_problems, **kwargs):# -> Quiz:
    raise NotImplementedError("Inheriting class needs to implement this")

  def match_answer(self, answer) -> bool:
    raise NotImplementedError("Inheriting class needs to implement this")

  def to_latex(self, **kwargs) -> (str, str):
    raise NotImplementedError("Inheriting class needs to implement this")

  def ask_pause_answer(self) -> None:
    """Ask aloud, pause, answer"""
    problem, answer = self.human_readable()
    droid.ttsSpeak(problem)
    time.sleep(self.pause)
    droid.ttsSpeak(answer)

  def print_pause_answer(self) -> None:
    """Print aloud, pause, answer"""
    problem, answer = self.human_readable()
    print(problem)
    time.sleep(self.pause)
    print(answer)

  def ask_input(self) -> bool:
    """ask input"""
    problem, answer = self.human_readable()
    droid.ttsSpeak(problem)
    your_answer = input()
    return self.match_answer(your_answer)

  def print_input(self) -> bool:
    """print input"""
    problem, answer = self.human_readable()
    print(problem)
    your_answer = input()
    return self.match_answer(your_answer)


class Quiz:

  def __init__(self, problems, log=None):#: list(ProblemInterface)
    self.problems = problems
    self.finished = False
    self.log = log

  def set_log(self, log=None):
    self.log = log
    return self

  def worksheet(self, speak=True, grade=True, write=True, log=None) -> None:
    grades = []
    times = []
    types = []
    if log is not None:
      self.log = log
    for problem in self.problems:
      q, a = problem.human_readable()
      types.append(str(type(problem).__name__))
      if speak:
        say(q)
      if write:
        print(q)
      if grade:
        t1 = time.time()
        answer = input()
        t2 = time.time()
        grades.append(problem.match_answer(answer))
        times.append(t2 - t1)
      else:
        time.sleep(problem.pause)
      if speak:
        say(a)
      if write:
        print(a)
    self.grades = grades
    self.times = times
    self.types = types
    self.finished = True
    if self.log is not None:
      with open(self.log, 'a+') as f:
        f.write(self.get_summary())
        f.write('\n')
    print(self.get_summary())


  def html_quiz(self, columns: int = 4, horizontal: bool = False) -> (str, str):
    """Return (questions_html, answers_html) worksheets using MathJax."""
    head = '''
<!DOCTYPE html>
<html>
<head>
<title>Mental Math Worksheet</title>
<meta charset="utf-8"/>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
<style>
table { border-collapse: collapse; }
td { padding: 6px 12px; vertical-align: top; }
h2 { margin-top: 1.5em; }
</style>
</head>
<body>
'''
    qs = head + '<h2>Questions</h2><table>\n<tr>'
    ans = head + '<h2>Answers</h2><table>\n<tr>'
    m = 0
    for problem in self.problems:
      q, a = problem.to_latex(horizontal=horizontal)
      if m and (m % columns) == 0:
        qs += '\n</tr><tr>'
        ans += '\n</tr><tr>'
      qs += f'\n  <td>\\({q}\\)</td>'
      ans += f'\n  <td>\\({a}\\)</td>'
      m += 1
    qs += '\n</tr>\n</table>\n</body>\n</html>'
    ans += '\n</tr>\n</table>\n</body>\n</html>'
    return qs, ans


  def get_summary(self):
    if not self.finished:
      raise RuntimeError("Complete the worksheet before getting a summary")
    # Handle non-graded worksheets safely
    if len(self.times) == 0 or len(self.grades) == 0:
      summary = {
        "quiz_date": datetime.now().isoformat(),
        "problem_types": [t for t in np.unique(self.types)],
        "problem_count": len(self.problems),
        "graded": False
      }
      return json.dumps(summary)
    summary = {
                "quiz_date": datetime.now().isoformat(),
                "problem_types": [t for t in np.unique(self.types)],
                "problem_count": len(self.problems),
                "correct_count": int(np.sum(self.grades)),
                "total_time": float(np.sum(self.times)),
                "mean_time": float(np.mean(self.times)),
                "max_time": float(np.max(self.times)),
                "min_time": float(np.min(self.times)),
                "median_time": float(np.median(self.times)),
                "std_time": float(np.std(self.times)),
                "correct": float(np.mean(self.grades)),
                "graded": True
              }
    return json.dumps(summary)


class DayOfTheWeek(ProblemInterface):
  '''
  Practice: given a date produce the day
  of the week
  '''

  def datetime_to_calendar(dt: datetime):
    '''Convert month day year'''
    months = ['January', 'February',
              'March', 'April', 'May',
              'June', 'July', 'August',
              'September', 'October',
              'November', 'December']
    month = months[dt.month-1]
    return f'{month} {dt.day} {dt.year}'

  def weekday_to_name(day: int) -> str:
    days = {
      0: 'sunday',
      1: 'monday',
      2: 'tuesday',
      3: 'wednesday',
      4: 'thursday',
      5: 'friday',
      6: 'saturday',
      }
    return days[day]

  def name_to_weekday(day: str) -> int:
    days = {
      'sunday': 0,
      'monday': 1,
      'tuesday': 2,
      'wednesday': 3,
      'thursday': 4,
      'friday': 5,
      'saturday': 6,
      }
    return days[day.lower()]

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

  def generate_quiz(num_problems,
                    start=datetime(1780, 1, 1),
                    end=datetime(2050, 1, 1),
                    pause=20):# -> Quiz:
    problems = []
    for k in range(num_problems):
      dt = DayOfTheWeek.random_date(start, end)
      problems.append(DayOfTheWeek(dt, pause=pause))
    return Quiz(problems)

  def __init__(self, date_time, pause=20):
    super(DayOfTheWeek, self).__init__(pause)
    self.date_time = date_time
    self.answer = (self.date_time.weekday() + 1) % 7

  def human_readable(self) -> (str, str):
    caldt = DayOfTheWeek.datetime_to_calendar(self.date_time)
    q = f'What day of the week was {caldt}?'
    a = f'{caldt} was a {DayOfTheWeek.weekday_to_name(self.answer)}'
    return q, a

  def match_answer(self, answer) -> bool:
    "supports 3, Wednesday, wednesday"
    try:
      answer = int(answer)
    except:
      answer = DayOfTheWeek.name_to_weekday(answer)
    return self.answer == answer

  def to_latex(self) -> (str, str):
    return self.human_readable()


class FloatingHoliday(ProblemInterface):
  '''
  Practice: given a floating holiday and
  the year produce the day of the month
  '''

  holidays = {
    'Thanksgiving Day': {
     'weekday': 4, 'week': 4, 'month': 11},
    'Martin Luther King Junior Day': {
     'weekday': 1, 'week': 3, 'month': 1},
    'Presidents Day': {
     'weekday': 1, 'week': 3, 'month': 2},
    'Memorial Day': {
     'weekday': 1, 'week': 5, 'month': 5},
    'Mothers Day': {
     'weekday': 7, 'week': 2, 'month': 5},
    'Fathers Day': {
     'weekday': 7, 'week': 3, 'month': 6},
    'Labor Day': {
     'weekday': 1, 'week': 1, 'month': 9},
    'Columbus Day': {
     'weekday': 1, 'week': 2, 'month': 10},
    'Canadian Thanksgiving Day': {
     'weekday': 1, 'week': 2, 'month': 10},
    }

  def floating_holiday(holiday, year):
    """
    Given a year and a holiday return the
    datetime object
    """
    if holiday['week'] == 5:
      return FloatingHoliday.floating_last_day(holiday, year)
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
      holiday_dt = dt - td
      wkday = (holiday_dt.weekday() + 1) % 7
      if wkday == weekday:
        return holiday_dt
    raise Exception

  def datetime_to_calendar(dt: datetime):
    '''Convert month day year'''
    months = ['January', 'February',
              'March', 'April', 'May',
              'June', 'July', 'August',
              'September', 'October',
              'November', 'December']
    month = months[dt.month-1]
    return f'{month} {dt.day} {dt.year}'

  def generate_quiz(num_problems,
                    start=1780,
                    end=2050,
                    pause=20):# -> Quiz:
    problems = []
    years = range(start, end)
    holidays = list(FloatingHoliday.holidays.keys())
    rng = range(len(holidays))
    hs = choice(rng, (num_problems, ))
    for h in hs:
      holiday = holidays[h]
      year = choice(years, (1,))[0]
      problems.append(FloatingHoliday(holiday, year, pause))
    return Quiz(problems)

  def __init__(self, holiday, year, pause=30):
      super(FloatingHoliday, self).__init__(pause)
      self.holiday = holiday
      self.year = year
      holiday = FloatingHoliday.holidays[self.holiday]
      self.dt = FloatingHoliday.floating_holiday(holiday, year)
      self.calendar_date = FloatingHoliday.datetime_to_calendar(self.dt)

  def human_readable(self) -> (str, str):
    h = f'{self.holiday} of {self.year}'
    q = f'What day of the month was {h}'
    a = f'{h} was {self.calendar_date}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
        answer = int(answer)
    except:
        pass
    return self.dt.day == answer

  def to_latex(self) -> (str, str):
    return self.human_readable()


def vertical_problem(op1, op2, op, ans) -> (str, str):
  '''
  op1: the first operand
  op2: the second operand
  op: the operator
  ans: the answer
  '''
  if ans != '':
    _, q = vertical_problem(op1, op2, op, '')
  else:
    q = ''
  a = f'''\\begin{{array}}{{r}}
    &{op1}\\\\
    {op}\\!\\!\\!\\!\\!\\!&{op2}\\\\
    \\hline
    &{ans}
    \\end{{array}}
    '''
  return q, a


class Addition(ProblemInterface):
  '''Practice Addition'''

  def generate_quiz(num_problems, digits_1=1, digits_2=1, pause=30):# -> Quiz:
    range1 = range(10**(digits_1-1), 10**digits_1)
    range2 = range(10**(digits_2-1), 10**digits_2)
    x = choice(range1, (num_problems, ),
               False if num_problems<(10**digits_1) else True)
    y = choice(range2, (num_problems, ),
               False if num_problems<(10**digits_2) else True)
    problems = []
    for a, b in zip(x, y):
      problems.append(Addition(a, b, pause))
    return Quiz(problems)

  def __init__(self, operand_1, operand_2, pause=30):
      super(Addition, self).__init__(pause)
      self.operand_1 = operand_1
      self.operand_2 = operand_2
      self.answer = operand_1 + operand_2

  def human_readable(self) -> (str, str):
    problem = f'{self.operand_1} plus {self.operand_2}'
    q = f'What is {problem}'
    a = f'{problem} equals {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.answer

  def to_latex(self, horizontal=True) -> (str, str):
    if horizontal:
      problem = f'{self.operand_1} + {self.operand_2}'
      return problem, f'{problem} = {self.answer}'
    return vertical_problem(self.operand_1,
                            self.operand_2,
                            '+',
                            self.answer)


class Subtraction(ProblemInterface):
  '''Practice subtraction'''

  def generate_quiz(num_problems, digits_1=1, digits_2=1, pause=30):# -> Quiz:
    range1 = range(10**(digits_1-1), 10**digits_1)
    range2 = range(10**(digits_2-1), 10**digits_2)
    x = choice(range1, (num_problems, ),
               False if num_problems<(10**digits_1) else True)
    y = choice(range2, (num_problems, ),
               False if num_problems<(10**digits_2) else True)
    problems = []
    for a, b in zip(x, y):
      problems.append(Subtraction(a, b, pause))
    return Quiz(problems)

  def __init__(self, operand_1, operand_2, pause=30):
      super(Subtraction, self).__init__(pause)
      self.operand_1 = operand_1
      self.operand_2 = operand_2
      self.answer = operand_1 - operand_2

  def human_readable(self) -> (str, str):
    problem = f'{self.operand_1} minus {self.operand_2}'
    q = f'What is {problem}'
    a = f'{problem} equals {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.answer

  def to_latex(self, horizontal=True) -> (str, str):
    if horizontal:
      problem = f'{self.operand_1} - {self.operand_2}'
      return problem, f'{problem} = {self.answer}'
    return vertical_problem(self.operand_1,
                            self.operand_2,
                            '-',
                            self.answer)


class Multiplication(ProblemInterface):
  '''Practice multiplication'''

  def generate_quiz(num_problems, digits_1=1, digits_2=1, pause=30):# -> Quiz:
    range1 = range(10**(digits_1-1), 10**digits_1)
    range2 = range(10**(digits_2-1), 10**digits_2)
    x = choice(range1, (num_problems, ),
               False if num_problems<(10**digits_1) else True)
    y = choice(range2, (num_problems, ),
               False if num_problems<(10**digits_2) else True)
    problems = []
    for a, b in zip(x, y):
      problems.append(Multiplication(a, b, pause))
    return Quiz(problems)

  def __init__(self, operand_1, operand_2, pause=30):
      super(Multiplication, self).__init__(pause)
      self.operand_1 = operand_1
      self.operand_2 = operand_2
      self.answer = operand_1 * operand_2

  def human_readable(self) -> (str, str):
    problem = f'{self.operand_1} times {self.operand_2}'
    q = f'What is {problem}'
    a = f'{problem} equals {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.answer

  def to_latex(self, horizontal=True) -> (str, str):
    if horizontal:
      problem = f'{self.operand_1} \\times {self.operand_2}'
      return problem, f'{problem} = {self.answer}'
    return vertical_problem(self.operand_1,
                            self.operand_2,
                            '\\times',
                            self.answer)


class Division(ProblemInterface):
  '''Practice division'''

  def generate_quiz(num_problems, digits_1=1, digits_2=1, pause=30):# -> Quiz:
    range1 = range(10**(digits_1-1), 10**digits_1)
    range2 = range(10**(digits_2-1), 10**digits_2)
    x = choice(range1, (num_problems, ),
               False if num_problems<(10**digits_1) else True)
    y = choice(range2, (num_problems, ),
               False if num_problems<(10**digits_2) else True)
    problems = []
    for a, b in zip(x, y):
      problems.append(Division(a, b, pause))
    return Quiz(problems)

  def __init__(self, dividend, divisor, pause=30):
      super(Division, self).__init__(pause)
      self.dividend = dividend
      self.divisor = divisor
      self.quotient = dividend / divisor

  def human_readable(self) -> (str, str):
    problem = f'{self.dividend} divided by {self.divisor}'
    q = f'What is {problem}'
    a = f'{problem} equals {self.quotient}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.quotient

  def to_latex(self) -> (str, str):
    #TODO support long division notation
    q = f'{self.dividend} / {self.divisor}'
    a = f'{q} = {self.quotient}'
    return q, a


class WholeRoots(ProblemInterface):
  '''
  Practice getting whole roots of n digit
  numbers
  '''

  def generate_quiz(num_problems, digits=2, n=2, pause=30):# -> Quiz:
    rng = range(10**(digits-1), 10**digits)
    x = choice(rng, (num_problems, ),
               False if num_problems<(10**digits) else True)
    problems = []
    for a in x:
      problems.append(WholeRoots(a, n, pause))
    return Quiz(problems)

  def __init__(self, answer, power, pause=30):
      super(WholeRoots, self).__init__(pause)
      self.raised_value = answer**power
      self.power = power
      self.answer = answer

  def human_readable(self) -> (str, str):
    problem = f'{self.power} root of {self.raised_value}'
    q = f'What is the {problem}?'
    a = f'The {problem} is {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.answer

  def to_latex(self) -> (str, str):
    q = f'\\sqrt[{self.power}]{{{self.raised_value}}}'
    a = f'{q}={self.answer}'
    return q, a


class Powers(ProblemInterface):
  '''Practice exponentiation'''

  def generate_quiz(num_problems, digits=2, power=2, pause=30):  # -> Quiz:
    rng = range(10**(digits-1), 10**digits)
    x = choice(rng, (num_problems,),
               replace=False if num_problems < (10**digits) else True)
    problems = []
    for a in x:
      problems.append(Powers(a, power, pause))
    return Quiz(problems)

  def __init__(self, value, power, pause=30):
      super(Powers, self).__init__(pause)
      self.value = value
      self.power = power
      self.answer = value ** power

  def human_readable(self) -> (str, str):
    problem = f'{self.value} to the power of {self.power}'
    q = f'What is {problem}?'
    a = f'{problem} equals {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.answer

  def to_latex(self) -> (str, str):
    p = f'{self.value}^{self.power}'
    a = f'{p} = {self.answer}'
    return p, a


class Roots(ProblemInterface):
  '''
  Practice getting approximate roots of n
  digit numbers
  '''

  def generate_quiz(num_problems, digits=2, power=2, pause=30, abs_tol=0.1):  # -> Quiz:
    rng = range(10**(digits-1), 10**digits)
    x = choice(rng, (num_problems,),
               replace=False if num_problems < (10**digits) else True)
    problems = []
    for a in x:
      problems.append(Roots(a, power, pause, abs_tol))
    return Quiz(problems)

  def __init__(self, raised_value, power, pause=30, abs_tol=0.1):
      super(Roots, self).__init__(pause)
      self.raised_value = raised_value
      self.power = power
      self.answer = raised_value ** (1.0 / power)
      self.abs_tol = abs_tol

  def human_readable(self) -> (str, str):
    problem = f'{self.power} root of {self.raised_value}'
    q = f'What is the {problem}?'
    a = f'The {problem} is {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = float(answer)
      return math.isclose(answer, self.answer, abs_tol=self.abs_tol)
    except:
      return False

  def to_latex(self) -> (str, str):
    q = f'\\sqrt[{self.power}]{{{self.raised_value}}}'
    a = f'{q} = {self.answer}'
    return q, a


class Modulo(ProblemInterface):
  '''Practice modulo'''

  def generate_quiz(num_problems, digits=3, modulo=9, pause=30):  # -> Quiz:
    rng = range(10**(digits-1), 10**digits)
    xs = choice(rng, (num_problems,),
                replace=False if num_problems < (10**digits) else True)
    problems = []
    for v in xs:
      problems.append(Modulo(v, modulo, pause))
    return Quiz(problems)

  def __init__(self, value, modulo, pause=30):
    super(Modulo, self).__init__(pause)
    self.value = value
    self.modulo = modulo
    self.answer = value % modulo

  def human_readable(self) -> (str, str):
    q = f'What is {self.value} mod {self.modulo}?'
    a = f'{self.value} mod {self.modulo} equals {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      return False
    return answer == self.answer

  def to_latex(self) -> (str, str):
    q = f'{self.value} \\bmod {self.modulo}'
    a = f'{q} = {self.answer}'
    return q, a


if __name__ == '__main__':
  # Example 1: Create an HTML worksheet (questions + answers)
  quiz_add = Addition.generate_quiz(num_problems=12, digits_1=2, digits_2=2, pause=5)
  qs_html, ans_html = quiz_add.html_quiz(columns=4, horizontal=True)
  with open('addition_questions.html', 'w') as f:
    f.write(qs_html)
  with open('addition_answers.html', 'w') as f:
    f.write(ans_html)
  print('Saved addition_questions.html and addition_answers.html')

  # Example 2: Audible (if androidhelper present) date problems, no grading
  dow_quiz = DayOfTheWeek.generate_quiz(num_problems=5, pause=4)
  print('Starting audible day-of-week practice (no input required)...')
  dow_quiz.worksheet(speak=True, write=False, grade=False)

  # Example 3: Terminal input + grading for multiplication
  mult_quiz = Multiplication.generate_quiz(num_problems=5, digits_1=2, digits_2=1, pause=3)
  print('Starting multiplication quiz (enter answers)...')
  mult_quiz.worksheet(speak=False, write=True, grade=True)

  # Example 4: Approximate roots with tolerance
  roots_quiz = Roots.generate_quiz(num_problems=3, digits=3, power=2, abs_tol=0.05)
  print('Approximate square roots (enter decimal answers)...')
  roots_quiz.worksheet(speak=False, write=True, grade=True)

  # Example 5: Modulo practice
  mod_quiz = Modulo.generate_quiz(num_problems=5, digits=4, modulo=9)
  print('Modulo quiz (enter remainder)...')
  mod_quiz.worksheet(speak=False, write=True, grade=True)
