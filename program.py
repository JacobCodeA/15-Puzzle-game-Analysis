import sys

import Board as Board
import DFS as D
import BFS as B
import a_star as a

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: program strategy <move_order/heuristics> <input_file> <solution_file> <stats_file>")
        exit(1)

    strategy = sys.argv[1]
    param = sys.argv[2]
    input_file = sys.argv[3]
    sol_file = sys.argv[4]
    stats_file = sys.argv[5]

    try:
        board = Board.Board.from_file(input_file)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        exit(1)

    if strategy == "dfs":
        solver = D.DFS(board, move_order=param, max_depth=20)
        solution, depth_, stats_ = solver.solve()
    elif strategy == "bfs":
        solver = B.BFS(board, move_order=param)
        solution, depth_, stats_ = solver.solve()
    elif strategy == "astr":
        solver = a.ASTAR(board, heuristic=param)
        solution, depth_, stats_ = solver.solve()
    else:
        print(f"Unknown strategy: {strategy}")
        exit(1)

    Board.Board.save_solution(sol_file, solution)
    Board.Board.save_stats(
        stats_file,
        depth_,
        stats_['visited'],
        stats_['processed'],
        stats_['max_depth'],
        stats_['time_ms']
    )