# -*- coding: utf-8 -*
import os
import random
import msvcrt
import threading
import queue
import sys

# 迷路のサイズ（奇数推奨）
WIDTH = 5
HEIGHT = 5

# 定数
WALL = '#'
PATH = ' '
PLAYER = '@'
GOAL = 'G'

# キー入力用のキュー
key_queue = queue.Queue()

def generate_maze(width, height):
    """
    ランダムな迷路を生成する（掘り進め法）
    """
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    start_x, start_y = (random.randint(0, width // 2 - 1) * 2 + 1, 
                        random.randint(0, height // 2 - 1) * 2 + 1)
    maze[start_y][start_x] = PATH
    stack = [(start_x, start_y)]
    
    while stack:
        cx, cy = stack[-1]
        directions = []
        if cx > 1 and maze[cy][cx - 2] == WALL: directions.append('W')
        if cx < width - 2 and maze[cy][cx + 2] == WALL: directions.append('E')
        if cy > 1 and maze[cy - 2][cx] == WALL: directions.append('N')
        if cy < height - 2 and maze[cy + 2][cx] == WALL: directions.append('S')
            
        if directions:
            direction = random.choice(directions)
            if direction == 'W':
                maze[cy][cx - 1], maze[cy][cx - 2] = PATH, PATH
                stack.append((cx - 2, cy))
            elif direction == 'E':
                maze[cy][cx + 1], maze[cy][cx + 2] = PATH, PATH
                stack.append((cx + 2, cy))
            elif direction == 'N':
                maze[cy - 1][cx], maze[cy - 2][cx] = PATH, PATH
                stack.append((cx, cy - 2))
            elif direction == 'S':
                maze[cy + 1][cx], maze[cy + 2][cx] = PATH, PATH
                stack.append((cx, cy + 2))
        else:
            stack.pop()
    return maze

def draw_maze(maze, player_pos, goal_pos):
    """
    迷路を描画する（ちらつき防止版）
    """
    # 画面をクリア
    os.system('cls' if os.name == 'nt' else 'clear')
    # 描画内容をバッファにためる
    screen_buffer = []
    for y, row in enumerate(maze):
        row_buffer = []
        for x, cell in enumerate(row):
            if (x, y) == player_pos:
                row_buffer.append(PLAYER)
            elif (x, y) == goal_pos:
                row_buffer.append(GOAL)
            else:
                row_buffer.append(cell)
        screen_buffer.append("".join(row_buffer))
    screen_buffer.append("\n操作: [w/↑]上 [a/←]左 [s/↓]下 [d/→]右  [q]終了")
    # バッファの内容を一度に出力
    sys.stdout.write("\n".join(screen_buffer))
    sys.stdout.flush()

def read_key_input():
    """
    キー入力をバックグラウンドで継続的に読み取る
    """
    while True:
        key = msvcrt.getch()
        key_queue.put(key)

def main():
    """
    ゲームのメイン処理
    """
    maze = generate_maze(WIDTH, HEIGHT)
    player_x, player_y = (1, 1)
    goal_x, goal_y = (WIDTH - 2, HEIGHT - 2)
    maze[player_y][player_x] = PATH
    maze[goal_y][goal_x] = PATH

    input_thread = threading.Thread(target=read_key_input, daemon=True)
    input_thread.start()

    # 初回描画
    draw_maze(maze, (player_x, player_y), (goal_x, goal_y))

    while True:
        # キー入力があるまで待機
        key = key_queue.get()

        new_x, new_y = player_x, player_y
        player_moved = False

        if key in [b'w', b'W']:
            new_y -= 1
        elif key in [b's', b'S']:
            new_y += 1
        elif key in [b'a', b'A']:
            new_x -= 1
        elif key in [b'd', b'D']:
            new_x += 1
        elif key in [b'q', b'Q']:
            print("\n\nゲームを終了します。")
            break
        elif key == b'\xe0': 
            second_key = key_queue.get()
            if second_key == b'H': new_y -= 1
            elif second_key == b'P': new_y += 1
            elif second_key == b'K': new_x -= 1
            elif second_key == b'M': new_x += 1

        if (new_x, new_y) != (player_x, player_y):
            if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and maze[new_y][new_x] != WALL:
                player_x, player_y = new_x, new_y
                player_moved = True

        if player_moved:
            draw_maze(maze, (player_x, player_y), (goal_x, goal_y))
            if (player_x, player_y) == (goal_x, goal_y):
                print("\n\nクリア！おめでとうございます！")
                break

if __name__ == '__main__':
    main()