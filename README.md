# レシピ投稿ミニアプリ（Flask + PostgreSQL）

Render の無料プランで動かせる、最小構成のレシピ投稿アプリです。  
**1 ページのみ**で「一覧表示」と「新規追加」ができます。

---

## 機能

- レシピ一覧表示（新しい順）
- 新規レシピ追加
  - タイトル（必須）
  - 所要分数（整数・1 以上）
  - 説明（任意）
- 編集・削除は未実装（今後の拡張用）

---

## ローカル実行手順

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```
