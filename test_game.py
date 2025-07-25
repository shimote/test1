# -*- coding: utf-8 -*>
import unittest
from unittest.mock import patch
from io import StringIO
import game

class TestGuessingGame(unittest.TestCase):
    """
    数字当てゲームのテストクラス
    """

    @patch('random.randint')
    def test_game_flow(self, mock_randint):
        """
        ゲームが正常に動作し、正しい回数で終了するかをテストする
        """
        # random.randintが常に50を返すように設定
        mock_randint.return_value = 50

        # ユーザー入力をシミュレート
        user_inputs = ['25', '75', '50']

        # input関数をモック化し、ユーザー入力を返すように設定
        with patch('builtins.input', side_effect=user_inputs):
            # 標準出力をキャプチャ
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                game.guessing_game()
                output = fake_out.getvalue().strip()

        # 期待される出力を定義
        expected_output = (
            "1から100までの数字を当ててください。\n"
            "もっと大きい\n"
            "もっと小さい\n"
            "正解です！ 3回で当たりました！"
        ).strip()

        # 出力が期待通りであることを確認
        self.assertEqual(output, expected_output)

    @patch('random.randint')
    def test_invalid_input(self, mock_randint):
        """
        無効な入力（数字以外）があった場合にエラーメッセージが表示されるかをテストする
        """
        mock_randint.return_value = 50
        user_inputs = ['abc', '50']

        with patch('builtins.input', side_effect=user_inputs):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                game.guessing_game()
                output = fake_out.getvalue().strip()

        expected_output = (
            "1から100までの数字を当ててください。\n"
            "無効な入力です。数字を入力してください。\n"
            "正解です！ 1回で当たりました！"
        ).strip()

        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
