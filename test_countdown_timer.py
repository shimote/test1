# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, call
from io import StringIO
import time
import sys
import countdown_timer

class TestCountdownTimer(unittest.TestCase):
    """
    カウントダウンタイマーのテストクラス
    """

    @patch('time.sleep', return_value=None) # time.sleepをモック化して待機時間をなくす
    @patch('builtins.input', return_value='3') # inputが常に'3'を返すように設定
    def test_timer_flow(self, mock_input, mock_sleep):
        """
        タイマーが正常に動作し、正しい出力が得られるかをテストする
        """
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            countdown_timer.countdown_timer()
            output = fake_out.getvalue()

        # 期待される出力を定義
        expected_output = (
            "タイマーを開始します...\n"
            "\r残り時間:  3秒"
            "\r残り時間:  2秒"
            "\r残り時間:  1秒"
            "\rタイマー終了！\a\n"
        )
        # \rのせいで単純比較が難しいので、行ごとに比較
        self.assertIn("タイマーを開始します...", output)
        self.assertIn("\r残り時間:  3秒", output)
        self.assertIn("\r残り時間:  2秒", output)
        self.assertIn("\r残り時間:  1秒", output)
        self.assertIn("\rタイマー終了！\a\n", output)

    @patch('builtins.input', return_value='abc')
    def test_invalid_input(self, mock_input):
        """
        無効な入力（数字以外）があった場合にエラーメッセージが表示されるかをテストする
        """
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            countdown_timer.countdown_timer()
            output = fake_out.getvalue().strip()

        self.assertEqual(output, "無効な入力です。数字を入力してください。")

    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """
        Ctrl+Cで中断された場合にメッセージが表示されるかをテストする
        """
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            countdown_timer.countdown_timer()
            output = fake_out.getvalue().strip()

        self.assertEqual(output, "タイマーが中断されました。")

if __name__ == '__main__':
    unittest.main()
