import japanize_matplotlib
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

def get_matrix_data_labels(attacker_idx):
    data_val = []
    data_label = []
    for i in range(18):
        row_v = []
        row_l = []
        for j in range(18):
            # 第1タイプ(i)と第2タイプ(j)が同じ場合は単タイプ(倍率そのまま)
            # 異なる場合は複合タイプ(倍率を掛け合わせる)
            if i == j:
                effect = Type.MATCHUP_TABLE[attacker_idx][i]
            else:
                effect = Type.MATCHUP_TABLE[attacker_idx][i] * Type.MATCHUP_TABLE[attacker_idx][j]
            
            row_v.append(effect)
            row_l.append(Type.get_rating(effect))
        data_val.append(row_v)
        data_label.append(row_l)
    return pd.DataFrame(data_val, index=Type.TYPE_NAMES, columns=Type.TYPE_NAMES), \
           pd.DataFrame(data_label, index=Type.TYPE_NAMES, columns=Type.TYPE_NAMES)

def plot_type_heatmap(attacker_idx):
    df_val, df_label = get_matrix_data_labels(attacker_idx)
    
    plt.figure(figsize=(14, 12))
    
    # annotに文字列のDataFrame(df_label)を渡す
    sns.heatmap(df_val, annot=df_label, fmt="", cmap="RdYlGn", center=1.0, linewidths=.5)
    
    plt.title(f"攻撃タイプ: {Type.TYPE_NAMES[attacker_idx]} の防御相性評価 (単/複合タイプ対応)")
    plt.xlabel("防御側 第2タイプ")
    plt.ylabel("防御側 第1タイプ")
    
    plt.savefig("type_matchup_fixed.png")
    print("グラフを 'type_matchup_fixed.png' として保存しました。")

# 実行
plot_type_heatmap(1)