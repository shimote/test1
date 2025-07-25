# -*- coding: utf-8 -*-
import datetime

def get_current_datetime_str():
    """
    現在の日時をフォーマットされた文字列として返します。
    """
    # 現在の日時を取得
    now = datetime.datetime.now()
    # 表示フォーマットを指定
    time_str = now.strftime("現在の日時は %Y年%m月%d日 %H時%M分%S秒 です。")
    # 文字列を返す
    return time_str

import time
import msvcrt

if __name__ == "__main__":
    # キーが押されるまで1秒ごとに現在時刻を更新して表示
    print("何かキーを押すと終了します。")
    while not msvcrt.kbhit():
        # 現在時刻を表示（カーソルを行頭に戻して上書き）
        print(get_current_datetime_str(), end="\r")
        # 1秒待機
        time.sleep(1)
    print("\n終了しました。")
