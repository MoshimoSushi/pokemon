import platform
import subprocess
import japanize_matplotlib  # noqa: F401
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Type:
    TYPE_NAMES = [
        "ノーマル", "ほのお", "みず", "くさ", "でんき", "こおり",
        "かくとう", "どく", "じめん", "ひこう", "エスパー", "むし",
        "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー",
    ]

    # 相性テーブル (18x18) を最初から NumPy 配列として定義
    MATCHUP_TABLE = np.array([
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
    ])

    # 記号マッピングの高速化（ベクター対応マップ）
    RATING_MAP = np.array(["✕", "▼", "△", "○", "◎", "★"])
    RATING_THRESHOLDS = np.array([0.25, 0.5, 1.0, 2.0, 4.0])

    @classmethod
    def get_rating_matrix(cls, matrix):
        """行列データに一括で記号をマッピングする（高速）"""
        # 各値がどの閾値の間に収まるかをインデックス化
        indices = np.digitize(matrix, cls.RATING_THRESHOLDS)
        return cls.RATING_MAP[indices]


def plot_multi_attacker_heatmap(attacker_bool_list):
    attacker_indices = [i for i, val in enumerate(attacker_bool_list) if val]
    selected_names = [Type.TYPE_NAMES[i] for i in attacker_indices]

    if not attacker_indices:
        print("攻撃タイプが選択されていません。")
        return

    # --- NumPyによる高速一括計算 (ベクトル化) ---
    # 選択された攻撃タイプの相性テーブルを抽出 (N, 18)
    sub_table = Type.MATCHUP_TABLE[attacker_indices]

    # 外積計算をブロードキャストで行い、(N, 18, 18) のテンソルを作成
    # 各要素は「特定の攻撃タイプにおける、防御第1タイプ×防御第2タイプ」の倍率
    all_effects = sub_table[:, :, np.newaxis] * sub_table[:, np.newaxis, :]

    # 異なるタイプの組み合わせ（i != j）の場合は外積の結果をそのまま使い、
    # 同じタイプ（i == j）の場合は単タイプ相性（元の倍率）を適用する
    for n in range(len(attacker_indices)):
        diag_vals = sub_table[n]
        np.fill_diagonal(all_effects[n], diag_vals)

    # 攻撃タイプごとの最大倍率を一括取得 (18, 18)
    data_val = np.max(all_effects, axis=0)
    data_label = Type.get_rating_matrix(data_val)

    # --- 下三角行列のデータ集計 ---
    lower_indices = np.tril_indices(18)
    valid_data = data_val[lower_indices]
    
    unique, counts_core = np.unique(valid_data, return_counts=True)
    counts = {4.0: 0, 2.0: 0, 1.0: 0, 0.5: 0, 0.25: 0, 0.0: 0}
    for u, c in zip(unique, counts_core):
        if u in counts:
            counts[u] = c

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
        annot_kws={"size": 18},
        ax=ax
    )

    # --- 評価結果とタイトルの配置 ---
    summary_text = (
        f"【総合評価 (全171通りの組み合わせ)】\n"
        f"4倍:{counts[4.0]} / 2倍:{counts[2.0]} / 1倍:{counts[1.0]} / "
        f"0.5倍:{counts[0.5]} / 0.25倍:{counts[0.25]} / 0倍:{counts[0.0]}"
    )
    plt.figtext(0.5, 0.04, summary_text, ha="center", fontsize=18, bbox={"facecolor": "white", "alpha": 0.8, "pad": 10})

    type_list_str = "、".join(selected_names)
    plt.title(f"攻撃タイプ: {type_list_str} の最大倍率評価", fontsize=16, pad=20)
    plt.xlabel("防御側 第2タイプ", labelpad=10)
    plt.ylabel("防御側 第1タイプ", labelpad=10)

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    
    img_path = "./datas/multi_attacker_matchup.png"
    plt.savefig(img_path)
    print(f"グラフを保存しました。集計対象: {len(valid_data)}件")
    
    # --- 自動開く処理 ---
    current_os = platform.system()
    try:
        if current_os == "Darwin":
            subprocess.run(["open", img_path])
        elif current_os == "Windows":
            subprocess.run(["cmd", "/c", f"start {img_path}"])
        elif current_os == "Linux":
            try:
                subprocess.run(["xdg-open", img_path], check=True, stderr=subprocess.DEVNULL)
            except (FileNotFoundError, subprocess.CalledProcessError):
                try:
                    win_path_bytes = subprocess.check_output(["wslpath", "-w", img_path])
                    win_path = win_path_bytes.decode("utf-8").strip()
                    subprocess.run(["explorer.exe", win_path])
                    print("WSL環境からWindowsのビューアーで画像を開きました。")
                except Exception as wsl_err:
                    print(f"画像は {img_path} に正常に保存されています。: {wsl_err}")
    except Exception as e:
        print(f"画像を開く際にエラーが発生しました: {e}")


def select_attackers_interactive():
    """コンソールから対話形式で攻撃タイプを選択する関数（名前・番号両対応）"""
    print("=" * 50)
    print(" 攻撃タイプ選択メニュー (名前または番号で入力可能)")
    print("=" * 50)
    
    # 2列で見やすく表示
    for i in range(9):
        p1 = f"[{i:2d}] {Type.TYPE_NAMES[i]:<6}"
        p2 = f"[{i+9:2d}] {Type.TYPE_NAMES[i+9]:<6}"
        print(f"{p1}\t{p2}")
        
    print("=" * 50)
    print("※ 入力例: '1, 2' または 'ほのお、みず' または 'ほのお じめん'")
    print("※ 全選択の場合は 'all' と入力してください。")
    print("=" * 50)

    user_input = input("攻撃タイプを入力してください: ").strip()

    if user_input.lower() == "all":
        return [True] * 18

    # 区切り文字（カンマ、読点、スペース）をスペースに統一して分割
    normalized = user_input.replace(",", " ").replace("、", " ").replace(" ", " ")
    tokens = [t.strip() for t in normalized.split(" ") if t.strip() != ""]

    attacker_bool_list = [False] * 18
    valid_selection = False

    for token in tokens:
        # 数字として処理できるか試行
        if token.isdigit():
            idx = int(token)
            if 0 <= idx < 18:
                attacker_bool_list[idx] = True
                valid_selection = True
            else:
                print(f"警告: 範囲外の番号 [{idx}] は無視されました。")
        # 文字列（タイプ名）として処理
        elif token in Type.TYPE_NAMES:
            idx = Type.TYPE_NAMES.index(token)
            attacker_bool_list[idx] = True
            valid_selection = True
        else:
            print(f"警告: 認識できない入力 [{token}] は無視されました。")

    if not valid_selection:
        print("有効なタイプが選択されませんでした。")
        return None
        
    return attacker_bool_list


if __name__ == "__main__":
    chosen_attackers = select_attackers_interactive()
    if chosen_attackers is not None:
        plot_multi_attacker_heatmap(chosen_attackers)