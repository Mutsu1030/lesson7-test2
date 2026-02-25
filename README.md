# QRコード生成ツール（Render対応）

Python標準構成で動く最小のQRコード生成Webアプリです。  
Flask + qrcode + Pillow のみ使用し、Renderでそのまま公開できます。

---

## 🚀 ローカル実行手順

```bash
# 仮想環境を作成
python -m venv env
# mac/Linux
source env/bin/activate
# Windows
env\Scripts\activate

# 依存インストール
pip install -r requirements.txt

# 実行
python app.py
