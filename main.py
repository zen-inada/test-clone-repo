def get_move(board):
    print("send_board")  # ←ハンドシェイク用（必須）

    import random

    SIZE = 4
    DIRECTIONS = [
        (1, 0, 0), (0, 1, 0), (1, 1, 0), (-1, 1, 0)
    ]

    def is_valid(x, y, z):
        return 0 <= x < SIZE and 0 <= y < SIZE and 0 <= z < SIZE

    def get_top_z(x, y):
        for z in range(SIZE):
            if board[z][y][x] == 0:
                return z
        return -1  # full

    def check_win(x, y, z, player):
        for dx, dy, dz in [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1),
            (1, 1, 1), (-1, 1, 0), (-1, 0, 1),
            (0, -1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1)
        ]:
            count = 1
            for d in range(1, 4):
                nx, ny, nz = x + dx*d, y + dy*d, z + dz*d
                if is_valid(nx, ny, nz) and board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            for d in range(1, 4):
                nx, ny, nz = x - dx*d, y - dy*d, z - dz*d
                if is_valid(nx, ny, nz) and board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def simulate_move(x, y, player):
        z = get_top_z(x, y)
        if z == -1:
            return False
        board[z][y][x] = player
        result = check_win(x, y, z, player)
        board[z][y][x] = 0  # undo
        return result

    def get_all_moves():
        moves = []
        for x in range(SIZE):
            for y in range(SIZE):
                if get_top_z(x, y) != -1:
                    moves.append((x, y))
        return moves

    # 推定ターンから手番判定
    count1 = sum(board[z][y][x] == 1 for z in range(SIZE) for y in range(SIZE) for x in range(SIZE))
    count2 = sum(board[z][y][x] == 2 for z in range(SIZE) for y in range(SIZE) for x in range(SIZE))
    me = 1 if count1 <= count2 else 2
    enemy = 3 - me

    legal_moves = get_all_moves()

    # ① 勝てる手を探す
    for x, y in legal_moves:
        if simulate_move(x, y, me):
            return (x, y)

    # ② 相手の勝ち手をブロック
    for x, y in legal_moves:
        if simulate_move(x, y, enemy):
            return (x, y)

    # ③ 中央優先戦略（2,1）や (1,2)
    center_pref = sorted(legal_moves, key=lambda mv: abs(mv[0]-1.5) + abs(mv[1]-1.5))
    return center_pref[0]
