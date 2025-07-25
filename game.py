# -*- coding: utf-8 -*-
import random

def guessing_game():
    """
    数字当てゲームのメイン関数
    """
    # 1から100までのランダムな整数を生成
    answer = random.randint(1, 100)
    attempts = 0
    
    print("1から100までの数字を当ててください。")

    while True:
        try:
            # ユーザーからの入力を受け取る
            guess_str = input("あなたの予想: ")
            guess = int(guess_str)
            attempts += 1

            # 入力された数字と答えを比較
            if guess < answer:
                print("もっと大きい")
            elif guess > answer:
                print("もっと小さい")
            else:
                # 正解した場合
                print(f"正解です！ {attempts}回で当たりました！")
                break
        except ValueError:
            # 数字以外の入力があった場合のエラー処理
            print("無効な入力です。数字を入力してください。")

if __name__ == '__main__':
    guessing_game()