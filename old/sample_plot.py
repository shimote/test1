# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

# 1. ランダムなデータを10個生成
# 乱数シードを固定して、毎回同じ乱数を生成するようにします
np.random.seed(0)
x_data = np.random.rand(10)  # 0から1の範囲で10個の乱数を生成
y_data = np.random.rand(10)  # 0から1の範囲で10個の乱数を生成

# 2. 散布図を描画
# labelを指定することで、凡例に表示される名前を設定します
plt.scatter(x_data, y_data, label='ランダムデータ')

# 3. グラフにタイトルとX軸、Y軸のラベルを設定
plt.title('散布図のサンプル')  # グラフのタイトル
plt.xlabel('X軸')  # X軸のラベル
plt.ylabel('Y軸')  # Y軸のラベル

# 4. 凡例を追加
# loc='upper left'で、凡例を左上に表示します
plt.legend(loc='upper left')

# 5. グリッド線を表示（任意）
plt.grid(True)

# 6. グラフを表示
plt.show()
