import os
import requests
from math import sqrt
from itertools import combinations
from collections import Counter
from dotenv import load_dotenv

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
    
    def dayFiveP1(self):
        sections = self.data.split("\n\n")
        ranges = [tuple(map(int, r.split("-"))) for r in sections[0].splitlines()]
        ingredients = [int(num) for num in sections[1].splitlines()]
        total_fresh = 0

        for num in ingredients:
            for r in ranges:
                if num in range(r[0], r[1] + 1):
                    total_fresh += 1
                    break
        return total_fresh
        
    def dayFiveP2(self):
        sections = self.data.split("\n\n")
        ranges = [tuple(map(int, r.split("-"))) for r in sections[0].splitlines()]
        ranges.sort()
        merged = []
    
        curr_start, curr_end = ranges[0]
        for start, end in ranges[1:]:
            if start <= curr_end + 1:
                curr_end = max(curr_end, end)
            else:
                merged.append((curr_start, curr_end))
                curr_start, curr_end = start, end
        
        merged.append((curr_start, curr_end))
        return sum((end - start + 1) for start, end in merged)

    def daySixP1(self):
        lines = [line.split() for line in self.data.splitlines()]
        numbers = lines[:-1]
        operators = lines[-1]
        grand_total = 0

        for i in range(len(numbers[0])):
            op = operators[i]
            if op == "+":
                total = 0
                for r in range(len(numbers)):
                    total += int(numbers[r][i])
                grand_total += total
            else:
                total = 1
                for r in range(len(numbers)):
                    total *= int(numbers[r][i])
                grand_total += total
        return grand_total

    def daySixP2(self):
        table = [list(line.strip('\n'))[::-1] for line in self.data.splitlines()]
        oper = ''.join(table[-1]).split()
        table = [''.join(t).strip() for t in zip(*table[:-1])] # transpose
        table = [s.split('|') for s in '|'.join(table).split('||')]
        res = 0
        for i in range(len(table)):
            res += eval(oper[i].join(table[i]))
        return res

    def daySevenP1(self):
        diagram = [list(line) for line in self.data.splitlines()]
        split_count = 0

        for row in range(len(diagram)):
            for col in range(len(diagram[0])):
                if diagram[row][col] == "^" and diagram[row - 1][col] == "|":
                    # split
                    diagram[row][col - 1] = diagram[row][col + 1] = "|"
                    split_count += 1
                elif row and (diagram[row - 1][col] == "S" or diagram[row - 1][col] == "|"):
                    # beam start or continue
                    diagram[row][col] = "|"
        return split_count

    def daySevenP2(self):
        diagram = [list(line) for line in self.data.splitlines()]
        R, C = len(diagram), len(diagram[0])

        # Find starting position
        start = None
        for c in range(len(diagram[0])):
            if diagram[0][c] == "S":
                start = c

        beams = [0] * len(diagram[0])
        beams[start] = 1

        for r in range(1, R):
            row = diagram[r]
            new_beams = [0] * C
            for c in range(C):
                if beams[c] > 0:
                    if row[c] == "^":
                        # beam splits
                        if c - 1 >= 0: new_beams[c - 1] += beams[c]
                        if c + 1 < C: new_beams[c + 1] += beams[c]
                    else:
                        # beam continues straight
                        new_beams[c] += beams[c]
            beams = new_beams
        return sum(beams)

    def dayEightP1(self):
        boxes = [tuple(map(int, line.split(","))) for line in self.data.splitlines()]
        parent = list(range(len(boxes)))

        def find(x):
            if parent[x] != x: parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py: parent[px] = py
        
        # compute all pairwise distances
        edges = []
        for (i, a), (j, b) in combinations(enumerate(boxes), 2):
            dist = sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
            edges.append((dist, i, j))
        
        edges.sort(key=lambda x: x[0])  # sort edges by distance
        for _, i, j in edges[:1000]: union (i, j)  # connect the 1000 closest pairs

        # count sizes of connected components
        sizes = Counter(find(i) for i in range(len(boxes)))
        largest_three = sorted(sizes.values(), reverse=True)[:3]

        result = 1
        for size in largest_three: result *= size
        return result

    def dayEightP2(self):
        boxes = [tuple(map(int, line.split(","))) for line in self.data.splitlines()]
        n = len(boxes)
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            if parent[x] != x: parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1
            return True
        
        # compute all pairwise distances
        edges = []
        for (i, a), (j, b) in combinations(enumerate(boxes), 2):
            dist = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
            edges.append((dist, i, j))
        
        edges.sort(key=lambda x: x[0])  # sort edges by distance

        components = n
        last_pair = None
        for _, i, j in edges:
            if union(i, j):
                last_pair = (i, j)
                components -= 1
                if components == 1: break

        # multiply the x coordinates of the last connected pair
        x_product = boxes[last_pair[0]][0] * boxes[last_pair[1]][0]
        return x_product

    def dayNineP1(self):
        tiles = [tuple(int(n) for n in line.split(',')) for line in self.data.splitlines()]
        max_area = 0
        for x1, y1 in tiles:
            for x2, y2 in tiles:
                area = abs(x1 - x2 + 1) * abs(y1 - y2 + 1)
                max_area = max(max_area, area)
        return max_area

    def dayNineP2(self):
        tiles = [[int(n) for n in line.split(',')] for line in self.data.splitlines()]
        tiles.append(tiles[0])
        verticals = sorted([(tiles[i][0], min(tiles[i][1], tiles[i + 1][1]), max(tiles[i][1], tiles[i + 1][1])) for i in range(len(tiles) - 1) if tiles[i][0] == tiles[i + 1][0]], key=lambda x: x[0])
        horizontals = sorted([(tiles[i][1], min(tiles[i][0], tiles[i + 1][0]), max(tiles[i][0], tiles[i + 1][0])) for i in range(len(tiles) - 1) if tiles[i][1] == tiles[i + 1][1]], key=lambda x: x[0])
        outside_verticals = [(vertical[0] + (1 if sum([1 for v in verticals[i + 1:] if v[1] <= (vertical[1] + vertical[2]) // 2 < v[2]]) % 2 == 0 else -1), vertical[1] + 1, vertical[2] - 1) for i, vertical in enumerate(verticals)]
        outside_horizontals = [(horizontal[0] + (1 if sum([1 for v in horizontals[i + 1:] if v[1] <= (horizontal[1] + horizontal[2]) // 2 < v[2]]) % 2 == 0 else -1), horizontal[1] + 1, horizontal[2] - 1) for i, horizontal in enumerate(horizontals)]
        max_area = 0
        for i, tile1 in enumerate(tiles):
            for tile2 in tiles[i + 1:]:
                area = (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)
                if area > max_area:
                    for vertical in outside_verticals:
                        if min(tile1[0], tile2[0]) <= vertical[0] <= max(tile1[0], tile2[0]) and min(tile1[1], tile2[1]) <= vertical[2] and vertical[1] <= max(tile1[1], tile2[1]):
                            break
                    else:
                        for horizontal in outside_horizontals:
                            if min(tile1[1], tile2[1]) <= horizontal[0] <= max(tile1[1], tile2[1]) and min(tile1[0], tile2[0]) <= horizontal[2] and horizontal[1] <= max(tile1[0], tile2[0]):
                                break
                        else:
                            max_area = area
        return max_area

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

    dayFive = Day("https://adventofcode.com/2025/day/5/input")
    print("\nDay-5-P1:", dayFive.dayFiveP1())
    print("Day-5-P2:", dayFive.dayFiveP2())

    daySix = Day("https://adventofcode.com/2025/day/6/input")
    print("\nDay-6-P1:", daySix.daySixP1())
    print("Day-6-P2:", daySix.daySixP2())

    daySeven = Day("https://adventofcode.com/2025/day/7/input")
    print("\nDay-7-P1:", daySeven.daySevenP1())
    print("Day-7-P2:", daySeven.daySevenP2())

    dayEight = Day("https://adventofcode.com/2025/day/8/input")
    print("\nDay-8-P1:", dayEight.dayEightP1())
    print("Day-8-P2:", dayEight.dayEightP2())

    dayNine = Day("https://adventofcode.com/2025/day/9/input")
    print("\nDay-9-P1:", dayNine.dayNineP1())
    print("Day-9-P2:", dayNine.dayNineP2())