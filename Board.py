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

    def load_from_list(self, tiles):
        if len(tiles) != self.size:
            raise ValueError("Wrong number of elements")
        if set(tiles) != set(range(self.size)):
            raise ValueError("Tiles must be 0..N unique")
        self.tiles = tiles.copy()
        self.zero_index = self.tiles.index(0)

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