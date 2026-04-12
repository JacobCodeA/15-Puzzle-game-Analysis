import time
import heapq
import Board


class ASTAR:
    def __init__(self, board, heuristic="manh", move_order="LRUD"):
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

        if heuristic == "manh":
            self.h_func = self.manhattan
        else:
            self.h_func = self.hamming

    def hamming(self, state):
        return sum(1 for i, v in enumerate(state) if v != 0 and v != self.goal[i])

    def manhattan(self, state):
        dist = 0
        width = self.width

        for i, v in enumerate(state):
            if v == 0:
                continue

            target = v - 1

            x1, y1 = divmod(i, width)
            x2, y2 = divmod(target, width)

            dist += abs(x1 - x2) + abs(y1 - y2)

        return dist

    def solve(self):
        start_time = time.time()

        start_state = tuple(self.start.tiles)
        start_zero = self.start.zero_index

        pq = []
        heapq.heappush(pq, (self.h_func(start_state), 0, start_state, start_zero))

        visited = {}
        parent = {}

        goal = self.goal
        move_map = self.move_map
        width = self.width
        height = self.height

        counter = 0

        while pq:
            f, g, state, zero = heapq.heappop(pq)

            self.max_reached_depth = max(self.max_reached_depth, g)

            if state in visited and visited[state] <= g:
                continue
            visited[state] = g
            self.visited_count += 1

            if state == goal:
                break

            for move in self.move_order:
                n_index = move_map[move](zero, width, height)
                if n_index is None:
                    continue

                lst = list(state)
                lst[zero], lst[n_index] = lst[n_index], lst[zero]
                new_state = tuple(lst)

                new_g = g + 1

                if new_state in visited and visited[new_state] <= new_g:
                    continue

                counter += 1
                self.processed_count += 1

                parent[new_state] = (state, move)

                heapq.heappush(
                    pq,
                    (new_g + self.h_func(new_state), new_g, new_state, n_index)
                )

        end_time = time.time()

        path = []
        if goal in parent or start_state == goal:
            cur = goal if goal in parent else start_state

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

        return path if path else None, len(path) if path else -1, stats