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

    def dayTwoP1(self):
        product_ids = self.data.split(",")
        invalid_sum = 0

        for id_range in product_ids:
            first, second = id_range.split("-")
            for num in range(int(first), int(second) + 1):
                s = str(num)
                if len(s) % 2 == 0:
                    half = len(s) // 2
                    if s[:half] == s[half:]:
                        invalid_sum += num
        return invalid_sum
    
    def dayTwoP2(self):
        product_ids = self.data.split(",")
        invalid_sum = 0

        for id_range in product_ids:
            first, second = id_range.split("-")
            for num in range(int(first), int(second) + 1):
                s = str(num)

                # try every substring length
                for k in range(1, len(s) // 2 + 1):
                    if len(s) % k != 0:
                        continue  # uneven division
                    
                    repeats = len(s) // k
                    if repeats >= 2:
                        if s == s[:k] * repeats:
                            invalid_sum += num
                            break
        return invalid_sum

if __name__ == "__main__":
    load_dotenv()
    cookies = { "session": os.getenv("SESSION") }
    
    dayOne = Day("https://adventofcode.com/2025/day/1/input");
    print("Day-1-P1:", dayOne.dayOneP1())
    print("Day-1-P2:", dayOne.dayOneP2())
