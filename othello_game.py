# -*- coding: utf-8 -*-
import ipywidgets as widgets
from ipycanvas import Canvas, hold_canvas
from IPython.display import display

# --- 定数とゲーム設定 ---
BOARD_SIZE = 8  # 盤面のサイズ (8x8)
CELL_SIZE = 50  # 各セルのピクセルサイズ
BOARD_PIXELS = BOARD_SIZE * CELL_SIZE # 盤面の合計ピクセルサイズ
LINE_COLOR = '#000000' # 盤面の線の色
BOARD_COLOR = '#008000' # 盤面の背景色 (緑)
PLAYER_COLORS = {1: 'Black', 2: 'White'} # プレイヤーの色
PLAYER_HEX_COLORS = {1: '#000000', 2: '#FFFFFF'} # プレイヤーの色の16進コード

class OthelloGame:
    """
    ipycanvasとipywidgetsを使ったインタラクティブなオセロゲームを管理するクラス。
    """
    def __init__(self):
        # --- ウィジェットの初期化 ---
        self.canvas = Canvas(width=BOARD_PIXELS, height=BOARD_PIXELS)
        self.turn_label = widgets.Label(value="") # 現在のプレイヤーを表示するラベル
        self.score_label = widgets.Label(value="") # スコアを表示するラベル
        self.reset_button = widgets.Button(description="リセット") # リセットボタン

        # --- イベントハンドラの設定 ---
        self.canvas.on_mouse_down(self.handle_mouse_click)
        self.reset_button.on_click(self.reset_game)

        # --- ゲームの初期化 ---
        self.reset_game()

        # --- UIの表示 ---
        # VBoxを使ってウィジェットを縦に並べる
        self.ui = widgets.VBox([
            widgets.HBox([self.turn_label, self.score_label]), # ラベルを横に並べる
            self.canvas,
            self.reset_button
        ])

    def reset_game(self, b=None):
        """ゲームの状態を初期設定にリセットする。"""
        # 盤面を初期化 (0: 空, 1: 黒, 2: 白)
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # 中央の4つの石を配置
        mid = BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = 2  # 白
        self.board[mid][mid] = 2          # 白
        self.board[mid - 1][mid] = 1      # 黒
        self.board[mid][mid - 1] = 1      # 黒
        
        self.current_player = 1  # 黒プレイヤーから開始
        self.update_ui()
        self.draw_board()

    def draw_board(self):
        """キャンバスに現在の盤面を描画する。"""
        with hold_canvas(self.canvas):
            # 背景を描画
            self.canvas.fill_style = BOARD_COLOR
            self.canvas.fill_rect(0, 0, BOARD_PIXELS, BOARD_PIXELS)
            
            # グリッド線を描画
            self.canvas.stroke_style = LINE_COLOR
            self.canvas.line_width = 1
            for i in range(BOARD_SIZE + 1):
                self.canvas.stroke_line(i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_PIXELS)
                self.canvas.stroke_line(0, i * CELL_SIZE, BOARD_PIXELS, i * CELL_SIZE)

            # 石を描画
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    player = self.board[r][c]
                    if player != 0:
                        self.canvas.fill_style = PLAYER_HEX_COLORS[player]
                        self.canvas.fill_circle(
                            c * CELL_SIZE + CELL_SIZE / 2,
                            r * CELL_SIZE + CELL_SIZE / 2,
                            CELL_SIZE / 2 - 4 # 石の半径
                        )

    def handle_mouse_click(self, x, y):
        """マウスクリックイベントを処理し、石を置く。"""
        # ピクセル座標を盤面の行と列に変換
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)

        # 有効な手か確認
        flipped_stones = self.get_flipped_stones(row, col, self.current_player)
        if self.board[row][col] == 0 and flipped_stones:
            # 石を置く
            self.board[row][col] = self.current_player
            # 相手の石を裏返す
            for r_flip, c_flip in flipped_stones:
                self.board[r_flip][c_flip] = self.current_player
            
            # プレイヤーを交代
            self.current_player = 3 - self.current_player # 1 -> 2, 2 -> 1
            
            # UIと盤面を更新
            self.update_ui()
            self.draw_board()

            # 次のプレイヤーが有効な手を持っているか確認
            if not self.has_valid_move(self.current_player):
                # 有効な手がない場合、もう一度プレイヤーを交代
                self.current_player = 3 - self.current_player
                if not self.has_valid_move(self.current_player):
                    # どちらのプレイヤーも手がない場合、ゲーム終了
                    self.end_game()
                else:
                    # 手をスキップしたことを通知
                    self.turn_label.value = f"{PLAYER_COLORS[3 - self.current_player]}は有効な手がなくスキップしました。{PLAYER_COLORS[self.current_player]}の番です。"


    def get_flipped_stones(self, row, col, player):
        """指定された場所に石を置いた場合に裏返る石のリストを返す。"""
        if self.board[row][col] != 0:
            return []

        opponent = 3 - player
        flipped = []
        # 8方向（上下左右、斜め）をチェック
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            stones_to_flip_in_dir = []
            # 盤面内で、相手の石が続く限り進む
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == opponent:
                stones_to_flip_in_dir.append((r, c))
                r += dr
                c += dc
            # 自分の石で挟んでいれば、裏返す石のリストに追加
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                flipped.extend(stones_to_flip_in_dir)
        return flipped

    def has_valid_move(self, player):
        """指定されたプレイヤーが有効な手を持っているか確認する。"""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == 0 and self.get_flipped_stones(r, c, player):
                    return True
        return False

    def update_ui(self):
        """ラベルのテキストを現在のゲーム状態で更新する。"""
        p1_score = sum(row.count(1) for row in self.board)
        p2_score = sum(row.count(2) for row in self.board)
        self.turn_label.value = f"現在のプレイヤー: {PLAYER_COLORS[self.current_player]}"
        self.score_label.value = f"スコア: 黒 {p1_score} - 白 {p2_score}"

    def end_game(self):
        """ゲーム終了時の処理。勝者を判定して表示する。"""
        p1_score = sum(row.count(1) for row in self.board)
        p2_score = sum(row.count(2) for row in self.board)
        if p1_score > p2_score:
            winner_text = "黒の勝ちです！"
        elif p2_score > p1_score:
            winner_text = "白の勝ちです！"
        else:
            winner_text = "引き分けです！"
        self.turn_label.value = f"ゲーム終了！ {winner_text}"

# --- ゲームの開始 ---
# OthelloGameクラスのインスタンスを作成し、UIを表示する
othello_game = OthelloGame()
display(othello_game.ui)
