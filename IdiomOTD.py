# idioms taken from: https://www.saporedicina.com/english/list-chengyu/
import random


def idiomoftheday():
    rand = random.randint(0,149)
    with open('idioms', 'r', encoding='utf-8') as idioms:
        lines = idioms.readlines()
        return lines[rand]

