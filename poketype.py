import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Type:
    # タイプ名定義
    TYPE_NAMES = [
        "ノーマル", "ほのお", "みず", "くさ", "でんき", "こおり", "かくとう", 
        "どく", "じめん", "ひこう", "エスパー", "むし", "いわ", "ゴースト", 
        "ドラゴン", "あく", "はがね", "フェアリー"
    ]

    # 相性テーブル (18x18)
    MATCHUP_TABLE = [
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 1.0, 1.0, 0.5, 1.0],
        [1.0, 0.5, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 1.0, 2.0, 1.0],
        [1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0],
        [1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 0.5, 1.0],
        [1.0, 1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0],
        [1.0, 0.5, 0.5, 2.0, 1.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0],
        [2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.0, 1.0, 2.0, 2.0, 0.5],
        [1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 0.0, 2.0],
        [1.0, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0],
        [1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0],
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.5, 1.0],
        [1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0, 0.5, 0.5],
        [1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0],
        [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 0.0],
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5],
        [1.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0],
        [1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 0.5, 1.0]
    ]

    @staticmethod
    def get_rating(effect):
        if effect >= 4.0: return "★"
        if effect >= 2.0: return "◎"
        if effect >= 1.0: return "○"
        if effect >= 0.5: return "△"
        if effect >= 0.25: return "▼"
        return "✕"

    @classmethod
    def display_matrix(cls, attacker_idx):
        attacker_name = cls.TYPE_NAMES[attacker_idx]
        
        # 複合タイプの相性を計算して行列を作成
        data = []
        for i in range(18):
            row = []
            for j in range(18):
                # iが第1タイプ、jが第2タイプ
                effect = cls.MATCHUP_TABLE[attacker_idx][i] * cls.MATCHUP_TABLE[attacker_idx][j]
                row.append(cls.get_rating(effect))
            data.append(row)
        
        # pandas DataFrameで整形
        df = pd.DataFrame(data, index=cls.TYPE_NAMES, columns=cls.TYPE_NAMES)
        
        print(f"攻撃タイプ: {attacker_name}")
        print(df)

# 実行例: ほのお(1)の相性
def get_matrix_data(attacker_idx):
    data = []
    for i in range(18):
        row = []
        for j in range(18):
            effect = Type.MATCHUP_TABLE[attacker_idx][i] * Type.MATCHUP_TABLE[attacker_idx][j]
            row.append(effect)
        data.append(row)
    return pd.DataFrame(data, index=Type.TYPE_NAMES, columns=Type.TYPE_NAMES)

def plot_type_heatmap(attacker_idx):
    df = get_matrix_data(attacker_idx)
    
    plt.figure(figsize=(12, 10))
    # 日本語フォント設定（環境に合わせて変更してください）
    plt.rcParams['font.family'] = 'sans-serif' 
    
    # ヒートマップ描画
    sns.heatmap(df, annot=True, cmap="RdYlGn", center=1.0, fmt=".1f", linewidths=.5)
    
    plt.title(f"攻撃タイプ: {Type.TYPE_NAMES[attacker_idx]} の相性倍率")
    plt.show()

# 実行
plot_type_heatmap(1)