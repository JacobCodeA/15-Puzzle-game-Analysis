from collections import deque
import time
import Board


class BFS:
    def __init__(self, board, move_order="LRUD"):
        self.start = board
        self.width = board.width
        self.height = board.height
        self.size = board.size

        self.move_order = move_order
        self.move_map = Board.Board.MOVE_MAP

        self.visited_count = 0
        self.processed_count = 0
        self.max_reached_depth = 0

        self.goal = tuple(range(1, self.size)) + (0,)

    def solve(self):
        if not self.start.is_solvable():
            print("Puzzle is NOT solvable")
            return None, -1, {}

        start_time = time.time()

        start_state = tuple(self.start.tiles)
        start_zero = self.start.zero_index

        fifo = deque()
        fifo.append((start_state, start_zero, 0))

        visited = set()
        parent = {}

        visited_add = visited.add
        fifo_popleft = fifo.popleft
        fifo_append = fifo.append

        width = self.width
        height = self.height
        move_map = self.move_map
        goal = self.goal

        found = None

        while fifo:
            state, zero, depth = fifo_popleft()

            self.max_reached_depth = max(self.max_reached_depth, depth)

            if state in visited:
                continue
            visited_add(state)
            self.visited_count += 1

            if state == goal:
                found = state
                break

            for move in self.move_order:
                n_index = move_map[move](zero, width, height)
                if n_index is None:
                    continue

                lst = list(state)
                lst[zero], lst[n_index] = lst[n_index], lst[zero]
                new_state = tuple(lst)

                if new_state in visited:
                    continue

                parent[new_state] = (state, move)

                fifo_append((new_state, n_index, depth + 1))
                self.processed_count += 1

        end_time = time.time()

        path = []
        if found is not None:
            cur = found
            while cur != start_state:
                prev, move = parent[cur]
                path.append(move)
                cur = prev
            path.reverse()

        stats = {
            "visited": self.visited_count,
            "processed": self.processed_count,
            "max_depth": self.max_reached_depth,
            "time_ms": round((end_time - start_time) * 1000, 3)
        }

        if found is None:
            return None, -1, stats

        return path, len(path), stats