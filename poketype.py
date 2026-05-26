import japanize_matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Type:
    # タイプ名定義
    TYPE_NAMES = [
        "ノーマル",
        "ほのお",
        "みず",
        "くさ",
        "でんき",
        "こおり",
        "かくとう",
        "どく",
        "じめん",
        "ひこう",
        "エスパー",
        "むし",
        "いわ",
        "ゴースト",
        "ドラゴン",
        "あく",
        "はがね",
        "フェアリー",
    ]

    # 相性テーブル (18x18)
    MATCHUP_TABLE = [
        [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.5,
            0.0,
            1.0,
            1.0,
            0.5,
            1.0,
        ],
        [
            1.0,
            0.5,
            0.5,
            2.0,
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            0.5,
            1.0,
            0.5,
            1.0,
            2.0,
            1.0,
        ],
        [
            1.0,
            2.0,
            0.5,
            0.5,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.5,
            1.0,
            1.0,
            1.0,
        ],
        [
            1.0,
            0.5,
            2.0,
            0.5,
            1.0,
            1.0,
            1.0,
            0.5,
            2.0,
            0.5,
            1.0,
            0.5,
            2.0,
            1.0,
            0.5,
            1.0,
            0.5,
            1.0,
        ],
        [
            1.0,
            1.0,
            2.0,
            0.5,
            0.5,
            1.0,
            1.0,
            1.0,
            0.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.5,
            1.0,
            1.0,
            1.0,
        ],
        [
            1.0,
            0.5,
            0.5,
            2.0,
            1.0,
            0.5,
            1.0,
            1.0,
            2.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.5,
            1.0,
        ],
        [
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.5,
            1.0,
            0.5,
            0.5,
            0.5,
            2.0,
            0.0,
            1.0,
            2.0,
            2.0,
            0.5,
        ],
        [
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            0.5,
            0.5,
            1.0,
            1.0,
            1.0,
            0.5,
            0.5,
            1.0,
            1.0,
            0.0,
            2.0,
        ],
        [
            1.0,
            2.0,
            1.0,
            0.5,
            2.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.0,
            1.0,
            0.5,
            2.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
        ],
        [
            1.0,
            1.0,
            1.0,
            2.0,
            0.5,
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            0.5,
            1.0,
            1.0,
            1.0,
            0.5,
            1.0,
        ],
        [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            1.0,
            1.0,
            0.5,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.5,
            1.0,
        ],
        [
            1.0,
            0.5,
            1.0,
            2.0,
            1.0,
            1.0,
            0.5,
            0.5,
            1.0,
            0.5,
            2.0,
            1.0,
            1.0,
            0.5,
            1.0,
            2.0,
            0.5,
            0.5,
        ],
        [
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            2.0,
            0.5,
            1.0,
            0.5,
            2.0,
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.5,
            1.0,
        ],
        [
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.5,
            1.0,
            1.0,
        ],
        [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.5,
            0.0,
        ],
        [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.5,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            1.0,
            2.0,
            1.0,
            0.5,
            1.0,
            0.5,
        ],
        [
            1.0,
            0.5,
            0.5,
            1.0,
            0.5,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
            1.0,
            1.0,
            0.5,
            2.0,
        ],
        [
            1.0,
            0.5,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            0.5,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            0.5,
            1.0,
        ],
    ]

    @staticmethod
    def get_rating(effect):
        if effect >= 4.0:
            return "★"
        if effect >= 2.0:
            return "◎"
        if effect >= 1.0:
            return "○"
        if effect >= 0.5:
            return "△"
        if effect >= 0.25:
            return "▼"
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
                effect = (
                    cls.MATCHUP_TABLE[attacker_idx][i]
                    * cls.MATCHUP_TABLE[attacker_idx][j]
                )
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
                effect = (
                    Type.MATCHUP_TABLE[attacker_idx][i]
                    * Type.MATCHUP_TABLE[attacker_idx][j]
                )

            row_v.append(effect)
            row_l.append(Type.get_rating(effect))
        data_val.append(row_v)
        data_label.append(row_l)
    return pd.DataFrame(
        data_val, index=Type.TYPE_NAMES, columns=Type.TYPE_NAMES
    ), pd.DataFrame(data_label, index=Type.TYPE_NAMES, columns=Type.TYPE_NAMES)


def plot_type_heatmap(attacker_idx):
    df_val, df_label = get_matrix_data_labels(attacker_idx)

    plt.figure(figsize=(14, 12))

    # annotに文字列のDataFrame(df_label)を渡す
    sns.heatmap(
        df_val, annot=df_label, fmt="", cmap="coolwarm_r", center=1.5, linewidths=0.5
    )

    plt.title(
        f"攻撃タイプ: {Type.TYPE_NAMES[attacker_idx]} の防御相性評価 (単/複合タイプ対応)"
    )
    plt.xlabel("防御側 第2タイプ")
    plt.ylabel("防御側 第1タイプ")

    plt.savefig("type_matchup_fixed.png")
    print("グラフを 'type_matchup_fixed.png' として保存しました。")


def plot_multi_attacker_heatmap(attacker_bool_list):
    attacker_indices = [i for i, val in enumerate(attacker_bool_list) if val]
    selected_names = [Type.TYPE_NAMES[i] for i in attacker_indices]

    if not attacker_indices:
        print("攻撃タイプが選択されていません。")
        return

    data_val = np.zeros((18, 18))
    data_label = np.empty((18, 18), dtype=object)

    # --- データの算出 ---
    for i in range(18):
        for j in range(18):
            if i == j:
                effects = [Type.MATCHUP_TABLE[idx][i] for idx in attacker_indices]
            else:
                effects = [Type.MATCHUP_TABLE[idx][i] * Type.MATCHUP_TABLE[idx][j] for idx in attacker_indices]
            max_effect = max(effects)
            data_val[i, j] = max_effect
            data_label[i, j] = Type.get_rating(max_effect)

    # --- マスク範囲外のみをカウント ---
    # 下三角行列 (対角線含む) のインデックスを取得
    lower_indices = np.tril_indices(18)
    valid_data = data_val[lower_indices]
    
    counts = {4.0: 0, 2.0: 0, 1.0: 0, 0.5: 0, 0.25: 0, 0.0: 0}
    for val in valid_data:
        if val in counts:
            counts[val] += 1

    # --- ヒートマップ作成 ---
    fig, ax = plt.subplots(figsize=(14, 14))
    mask = np.triu(np.ones((18, 18), dtype=bool), k=1)
    
    sns.heatmap(
        pd.DataFrame(data_val, index=Type.TYPE_NAMES, columns=Type.TYPE_NAMES),
        annot=data_label,
        mask=mask,
        fmt="",
        vmin=0,
        vmax=4,
        cmap="coolwarm_r",
        center=1.5,
        linewidths=0.5,
        cbar=False,
        annot_kws={"size": 20},
        ax=ax
    )

    # --- 評価結果を下部に配置 ---
    summary_text = (
        f"【総合評価 (全171通りの組み合わせ)】\n"
        f"4倍:{counts[4.0]} / 2倍:{counts[2.0]} / 1倍:{counts[1.0]} / "
        f"0.5倍:{counts[0.5]} / 0.25倍:{counts[0.25]} / 0倍:{counts[0.0]}"
    )
    plt.figtext(0.5, 0.05, summary_text, ha="center", fontsize=20, bbox={"facecolor": "white", "alpha": 0.5, "pad": 10})

    type_list_str = "、".join(selected_names)
    plt.title(f"攻撃タイプ: {type_list_str} の最大倍率評価", fontsize=16)
    plt.xlabel("防御側 第2タイプ")
    plt.ylabel("防御側 第1タイプ")

    plt.tight_layout(rect=[0, 0.08, 1, 1]) # テキスト領域を確保
    plt.savefig("./datas/multi_attacker_matchup.png")
    print(f"グラフを保存しました。集計対象: {len(valid_data)}件")


# 実行例
attackers = [False] * 18
attackers[0] = True  # ノーマル
attackers[1] = True  # ほのお
attackers[2] = True  # みず
attackers[3] = True  # くさ
attackers[4] = True  # でんき
attackers[5] = True  # こおり
attackers[6] = True  # かくとう
attackers[7] = True  # どく
attackers[8] = True  # じめん
attackers[9] = True  # ひこう
attackers[10] = True  # エスパー
attackers[11] = True  # むし
attackers[12] = True  # いわ
attackers[13] = True  # ゴースト
attackers[14] = True  # ドラゴン
attackers[15] = True  # あく
attackers[16] = True # はがね
attackers[17] = True  # フェアリー

plot_multi_attacker_heatmap(attackers)