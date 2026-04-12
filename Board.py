import random

class Board:
    MOVE_MAP = {
        'L': lambda z, w, h: z-1 if z % w > 0 else None,
        'R': lambda z, w, h: z+1 if z % w < w-1 else None,
        'U': lambda z, w, h: z-w if z // w > 0 else None,
        'D': lambda z, w, h: z+w if z // w < h-1 else None
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width * height
        self.tiles = list(range(1, self.size)) + [0]
        self.goal = self.tiles.copy()
        self.zero_index = self.size - 1
        self.depth = 0
        self.neighbours_map = [self._compute_neighbours(i) for i in range(self.size)]

    def _compute_neighbours(self, index):
        neighbours = []
        row, col = divmod(index, self.width)
        if col > 0: neighbours.append(index - 1)
        if col < self.width - 1: neighbours.append(index + 1)
        if row > 0: neighbours.append(index - self.width)
        if row < self.height - 1: neighbours.append(index + self.width)
        return neighbours

    def swap(self, i, j):
        if self.tiles[i] == 0:
            self.zero_index = j
        elif self.tiles[j] == 0:
            self.zero_index = i
        self.tiles[i], self.tiles[j] = self.tiles[j], self.tiles[i]

    def load_from_list(self, tiles):
        if len(tiles) != self.size:
            raise ValueError("Wrong number of elements")
        if set(tiles) != set(range(self.size)):
            raise ValueError("Tiles must be 0..N unique")
        self.tiles = tiles.copy()
        self.zero_index = self.tiles.index(0)

    def randomise(self, itr=7, avoid_backtracking=True):
        self.depth = itr
        previous = None
        for _ in range(itr):
            zero = self.zero_index
            neighbours = self.neighbours_map[zero]
            if avoid_backtracking and previous is not None:
                neighbours = [n for n in neighbours if n != previous]
            move = random.choice(neighbours)
            previous = zero
            self.swap(zero, move)

    def is_solvable(self):
        inv_count = 0
        arr = [x for x in self.tiles if x != 0]
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]: inv_count += 1
        if self.width % 2 == 1:
            return inv_count % 2 == 0
        else:
            row_from_bottom = self.height - (self.zero_index // self.width)
            return (inv_count + row_from_bottom) % 2 == 1

    def hamming(self):
        distance = 0
        for i in range(self.size):
            if self.tiles[i] != self.zero_index and self.tiles[i] != self.goal[i]:
                distance += 1
        return distance

    def manhattan(self):
        distance = 0
        for i in range(self.size):
            value = self.tiles[i]
            if value != 0:
                row_now, col_now = value // self.width, value % self.width
                target_index = value - 1
                row_target, col_target = target_index // self.width, target_index % self.width

                distance += abs(row_now - row_target) + abs(col_now - col_target)
        return distance

    def is_complete(self):
        return self.tiles == self.goal

    def print_board(self):
        for i in range(self.size):
            if i % self.width == 0: print()
            print(f"{self.tiles[i]:2}", end=" ")
        print("\n")

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            lines = f.read().splitlines()
        height, width = map(int, lines[0].split())
        tiles = []
        for line in lines[1:]:
            tiles.extend(map(int, line.split()))
        board = cls(width, height)
        board.load_from_list(tiles)
        return board

    @staticmethod
    def save_solution(filename, solution):
        with open(filename, "w") as f:
            if solution is None:
                f.write("-1\n")
            else:
                f.write(f"{len(solution)}\n")
                f.write("".join(solution) + "\n")

    @staticmethod
    def save_stats(filename, depth, visited, processed, max_depth, time_ms):
        with open(filename, "w") as f:
            f.write(f"{depth}\n")
            f.write(f"{visited}\n")
            f.write(f"{processed}\n")
            f.write(f"{max_depth}\n")
            f.write(f"{time_ms}\n")