# Gitの練習 2025//07/25
# -*- coding: utf-8 -*-
import time
import sys

def countdown_timer():
    """
    カウントダウンタイマーのメイン関数
    """
    try:
        # ユーザーから秒数を取得
        seconds_str = input("カウントダウンする秒数を入力してください: ")
        total_seconds = int(seconds_str)

        print("タイマーを開始します...")

        # 指定された秒数だけカウントダウン
        for remaining in range(total_seconds, 0, -1):
            # 同じ行に残り時間を上書き表示
            sys.stdout.write(f"\r残り時間: {remaining:2d}秒")
            sys.stdout.flush()
            time.sleep(1)

        # 終了メッセージとベル
        sys.stdout.write("\rタイマー終了！\a\n")
        sys.stdout.flush()

    except ValueError:
        # 数字以外の入力があった場合のエラー処理
        print("\n無効な入力です。数字を入力してください。")
    except KeyboardInterrupt:
        # Ctrl+Cが押された場合の中断処理
        print("\nタイマーが中断されました。")

if __name__ == '__main__':
    countdown_timer()
