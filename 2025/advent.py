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

    def dayThreeP1(self):
        banks = self.data.splitlines()
        total_joltage = 0

        for bank in banks:
            battery1 = 0
            ending_idx = 0
            for i, digit in enumerate(bank[:-1]):
                if int(digit) > battery1:
                    battery1 = int(digit)
                    ending_idx = i
            
            battery2 = 0
            for digit in bank[ending_idx+1:]:
                battery2 = max(battery2, int(digit))
            
            total_joltage += int(str(battery1) + str(battery2))
        
        return total_joltage

    def dayThreeP2(self):
        banks = self.data.splitlines()
        total_joltage = 0

        for bank in banks:
            k = 12
            remove = len(bank) - k
            stack = []

            for digit in bank:
                while remove and stack and stack[-1] < digit:
                    stack.pop()
                    remove -= 1
                stack.append(digit)

            total_joltage += int("".join(stack[:k]))
        return total_joltage

    def dayFourP1(self):
        grid = [list(line) for line in self.data.splitlines()]
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        rows = len(grid)
        cols = len(grid[0])
        total = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '@':
                    continue
                    
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if nr in range(rows) and nc in range(cols) and grid[nr][nc] == '@':
                        count += 1
            
                if count < 4:
                    total += 1
        return total

    def dayFourP2(self):
        grid = [list(line) for line in self.data.splitlines()]
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        rows = len(grid)
        cols = len(grid[0])
        total_removed = 0

        while True:
            to_remove = []

            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] != '@':
                        continue
                    count = 0

                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if nr in range(rows) and nc in range(cols) and grid[nr][nc] == '@':
                            count += 1
                    if count < 4:
                        to_remove.append((r, c))
                        grid[r][c] = '.'
            
            if not to_remove:
                break
            total_removed += len(to_remove)

        return total_removed

if __name__ == "__main__":
    load_dotenv()
    cookies = { "session": os.getenv("SESSION") }
    
    dayOne = Day("https://adventofcode.com/2025/day/1/input");
    print("Day-1-P1:", dayOne.dayOneP1())
    print("Day-1-P2:", dayOne.dayOneP2())

    dayTwo = Day("https://adventofcode.com/2025/day/2/input")
    print("\nDay-2-P1:", dayTwo.dayTwoP1())
    print("Day-2-P2:", dayTwo.dayTwoP2())

    dayThree = Day("https://adventofcode.com/2025/day/3/input")
    print("\nDay-3-P1:", dayThree.dayThreeP1())
    print("Day-3-P2:", dayThree.dayThreeP2())

    dayFour = Day("https://adventofcode.com/2025/day/4/input")
    print("\nDay-4-P1:", dayFour.dayFourP1())
    print("Day-4-P2:", dayFour.dayFourP2())