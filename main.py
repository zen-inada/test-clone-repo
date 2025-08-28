# === main.py（MyAI.get_move の本文だけ編集可）===

from abc import ABC, abstractmethod
from typing import Tuple, List

Board = List[List[List[int]]]  # board[z][y][x]

# 変更禁止: 親インターフェース
class Alg3D(ABC):
    @abstractmethod
    def get_move(self, board: Board) -> Tuple[int, int]:
        """(x, y) を返す。0<=x,y<4"""
        ...

# ここから下だけロジック編集
class MyAI(Alg3D):
    SIZE = 4
    # 勝ち判定に使う3D方向（反対向きは走査でカバー）
    DIRS = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (-1, 1, 0), (-1, 0, 1),
        (0, -1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1),
    ]

    def get_move(self, board: Board) -> Tuple[int, int]:
        me = self._who_am_i(board)
        enemy = 3 - me

        legal = self._legal_moves(board)
        if not legal:
            return (0, 0)

        # ① 即勝ち
        for x, y in legal:
            if self._wins_if(board, x, y, me):
                return (x, y)

        # ② ブロック
        for x, y in legal:
            if self._wins_if(board, x, y, enemy):
                return (x, y)

        # ③ 中央優先（(1.5,1.5) への距離が最小）
        best = min(legal, key=lambda mv: abs(mv[0] - 1.5) + abs(mv[1] - 1.5))
        return best

    # ===== 補助 =====
    def _who_am_i(self, board: Board) -> int:
        c1 = sum(board[z][y][x] == 1 for z in range(4) for y in range(4) for x in range(4))
        c2 = sum(board[z][y][x] == 2 for z in range(4) for y in range(4) for x in range(4))
        return 1 if c1 <= c2 else 2

    def _top_z(self, board: Board, x: int, y: int) -> int:
        for z in range(self.SIZE):
            if board[z][y][x] == 0:
                return z
        return -1

    def _in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < self.SIZE and 0 <= y < self.SIZE and 0 <= z < self.SIZE

    def _check_win_from(self, board: Board, x: int, y: int, z: int, player: int) -> bool:
        for dx, dy, dz in self.DIRS:
            cnt = 1
            for d in range(1, 4):
                nx, ny, nz = x + dx*d, y + dy*d, z + dz*d
                if self._in_bounds(nx, ny, nz) and board[nz][ny][nx] == player:
                    cnt += 1
                else:
                    break
            for d in range(1, 4):
                nx, ny, nz = x - dx*d, y - dy*d, z - dz*d
                if self._in_bounds(nx, ny, nz) and board[nz][ny][nx] == player:
                    cnt += 1
                else:
                    break
            if cnt >= 4:
                return True
        return False

    def _wins_if(self, board: Board, x: int, y: int, player: int) -> bool:
        z = self._top_z(board, x, y)
        if z == -1:
            return False
        board[z][y][x] = player
        try:
            return self._check_win_from(board, x, y, z, player)
        finally:
            board[z][y][x] = 0  # 元に戻す

    def _legal_moves(self, board: Board) -> List[Tuple[int, int]]:
        return [(x, y)
                for y in range(self.SIZE)
                for x in range(self.SIZE)
                if self._top_z(board, x, y) != -1]

# ---- 変更禁止：ワーカーが呼ぶ入口（必ず残す）----
_ai = MyAI()

def get_move(board: Board) -> Tuple[int, int]:
    print("send_board")  # ハンドシェイクログ（stderrに回収されます）
    x, y = _ai.get_move(board)
    x, y = int(x), int(y)
    if not (0 <= x < 4 and 0 <= y < 4):
        raise ValueError(f"move out of range: {(x, y)}")
    return x, y
