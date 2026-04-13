import time
from Board import Board

class DFS:
    def __init__(self, board, move_order="LRUD", max_depth=50):
        self.start = board
        self.width = board.width
        self.height = board.height
        self.size = board.size

        self.move_order = move_order
        self.max_depth = max(max_depth, 20)

        self.best_solution = None
        self.best_depth = float('inf')

        self.visited_count = 0
        self.processed_count = 0
        self.max_reached_depth = 0

        self.goal = tuple(range(1, self.size)) + (0,)
        self.move_map = Board.MOVE_MAP

        self.visited = set()
        self.path = []

    @staticmethod
    def board_to_state(board):
        return tuple(board.tiles)

    def is_goal(self, state):
        return state == self.goal

    def dfs(self, state, zero, depth):
        self.max_reached_depth = max(self.max_reached_depth, depth)

        if state in self.visited:
            return
        self.visited.add(state)
        self.visited_count += 1

        if depth >= self.max_depth or depth >= self.best_depth:
            return

        if state == self.goal:
            self.best_solution = self.path.copy()
            self.best_depth = depth
            return

        width = self.width
        height = self.height
        move_map = self.move_map

        for move in self.move_order:
            n_index = move_map[move](zero, width, height)
            if n_index is None:
                continue

            lst = list(state)
            lst[zero], lst[n_index] = lst[n_index], lst[zero]
            new_state = tuple(lst)

            self.path.append(move)
            self.processed_count += 1

            self.dfs(new_state, n_index, depth + 1)

            self.path.pop()

    def solve(self):
        if not self.start.is_solvable():
            print("Puzzle is NOT solvable")
            return None, -1, {}

        start_time = time.time()

        start_state = self.board_to_state(self.start)
        start_zero = self.start.zero_index

        self.dfs(start_state, start_zero, 0)

        end_time = time.time()

        stats = {
            "visited": self.visited_count,
            "processed": self.processed_count,
            "max_depth": self.max_reached_depth,
            "time_ms": round((end_time - start_time) * 1000, 3)
        }

        if self.best_solution is None:
            return None, -1, stats

        return self.best_solution, self.best_depth, stats