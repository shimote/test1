# -*- coding: utf-8 -*-
import datetime
from display_datetime import get_current_datetime_str

def test_get_current_datetime_str():
    """
    get_current_datetime_str 関数のテスト
    """
    # 関数の実行結果を取得
    result = get_current_datetime_str()
    # 現在時刻を期待されるフォーマットで取得
    now = datetime.datetime.now()
    expected = now.strftime("現在の日時は %Y年%m月%d日 %H時%M分%S秒 です。")
    # 秒までを比較（実行タイミングのズレを考慮）
    assert result[:-3] == expected[:-3]
