import requests
from math import sqrt
from itertools import combinations
from collections import Counter, deque
from dotenv import load_dotenv
import os

class Day:
    def __init__(self, url):
        self.data = requests.get(url, cookies=cookies).text.strip();

    def dayOneP1(self):
        lines = self.data.splitlines();
        number = 50
        zeros = 0

        for step in lines:
            direction = step[0]
            amount = int(step[1:])

            if direction == 'R':
                number = (number + amount) % 100
            else:
                number = (number - amount) % 100
            if number == 0:
                zeros += 1

        return zeros
    
    def dayOneP2(self):
        lines = self.data.splitlines()
        number = 50
        zeros = 0

        for step in lines:
            direction = step[0]
            amount = int(step[1:])

            if direction == 'R':
                for _ in range(amount):
                    number = (number + 1) % 100
                    if number == 0:
                        zeros += 1
            else:
                for _ in range(amount):
                    number = (number - 1) % 100
                    if number == 0:
                        zeros += 1

        return zeros

if __name__ == "__main__":
    load_dotenv()
    cookies = { "session": os.getenv("SESSION") }
    
    dayOne = Day("https://adventofcode.com/2025/day/1/input");
    print("Day-1-P1:", dayOne.dayOneP1())
    print("Day-1-P2:", dayOne.dayOneP2())
