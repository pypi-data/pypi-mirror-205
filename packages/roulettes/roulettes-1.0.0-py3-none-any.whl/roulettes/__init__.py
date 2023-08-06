__version__ = '1.0.0'

import random

def roulette(contents):
  
  try:
    for i in range(len(contents)):
      contents[i]['chance'] -= 0
      contents[i]['item'] += ''
  except:
    raise TypeError('Contents of a roulette must have this format: [{"item": <item>, "chance": <chance>}, {"item": <item>, "chance": <chance>}, ...]')

  chances = []
  for i in range(len(contents)):
    chances.append(contents[i]['chance'])

  if sum(chances) <= 0:
    raise ValueError("Suma of roulette contents' chances can't be zero or negative")
  
  reward_int = random.randrange(1, sum(chances))
  bruh = 0
  for i in range(len(chances)):
    for b in range(chances[i]):
      bruh += 1
      if bruh == reward_int:
        reward = contents[i]['item']

  return reward