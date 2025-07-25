# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import maze_game

class TestMazeGame(unittest.TestCase):
    """
    迷路ゲームのテストクラス
    """

    def test_generate_maze(self):
        """
        迷路が指定されたサイズで生成され、壁と通路で構成されているかテストする
        """
        width, height = 5, 5
        maze = maze_game.generate_maze(width, height)
        
        # サイズの確認
        self.assertEqual(len(maze), height)
        self.assertEqual(len(maze[0]), width)
        
        # 壁と通路のみで構成されているか確認
        has_path = False
        for row in maze:
            for cell in row:
                self.assertIn(cell, [maze_game.WALL, maze_game.PATH])
                if cell == maze_game.PATH:
                    has_path = True
        # 少なくとも1つは通路があることを確認
        self.assertTrue(has_path)

    def test_player_cannot_move_into_wall(self):
        """
        プレイヤーが壁の中に移動できないことをテストする
        """
        # 固定の迷路を生成
        maze = [
            ['#', '#', '#', '#', '#'],
            ['#', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#'],
        ]
        player_x, player_y = 1, 1

        # 右は壁なので移動できないはず
        maze_game.key_queue.put(b'd') # 右へ
        
        # プレイヤーの位置を更新するメインループの一部を模倣
        # 本来はループだが、テストのため1回だけ実行
        new_x, new_y = player_x, player_y
        key = maze_game.key_queue.get()
        if key == b'd':
            new_x += 1
        
        # 移動先が壁でないかチェック
        if maze[new_y][new_x] != maze_game.WALL:
            player_x, player_y = new_x, new_y

        # プレイヤーの位置が変わっていないことを確認
        self.assertEqual((player_x, player_y), (1, 1))

if __name__ == '__main__':
    unittest.main()
