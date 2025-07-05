# シフト最適化ツール

このリポジトリには、シフト表を最適化して作成するシンプルなスクリプトが含まれています。

## 使い方

次の 2 つの CSV ファイルを準備します。

1. `shift.csv` – メンバーの空き情報をまとめた表です。最初の列にメンバー名を記載し、後続の列では `○` を使ってシフトに入れるかどうかを示します。
2. `attribute.csv` – メンバーの属性をまとめたファイルで、`name`、`gender`、`committee` の列を持ちます。委員会に所属している場合は `〇` を記載します。

最適化スクリプトを次のように実行します。

```bash
python shift_optimizer.py --shift path/to/shift.csv \
                          --attr path/to/attribute.csv \
                          --out path/to/output.csv
```

引数を省略した場合は、実行中にファイルパスの入力を求められます。
