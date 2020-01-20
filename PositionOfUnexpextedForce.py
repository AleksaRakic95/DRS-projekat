import random

def ForceLife(queueX, queueY):
    while True:
        randX = random.randrange(15, 765)
        randY = random.randrange(0, 4)
        nivoi = [565, 475, 385, 295]
        positionY = nivoi[randY]
        queueX.put(randX)
        queueY.put(positionY)

def ForceBomb(queueX, queueY):
    while True:
        randX = random.randrange(15, 765)
        randY = random.randrange(0, 4)
        nivoi = [565, 475, 385, 295]
        positionY = nivoi[randY]
        queueX.put(randX)
        queueY.put(positionY)
