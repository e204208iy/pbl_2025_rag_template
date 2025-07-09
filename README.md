## 動作確認済み環境
- Python 3.9.6
- venv
- node v18.18.0
## 🚀 セットアップ手順
このプロジェクトを実行するための手順です。

### 1. リポジトリをクローン
```bash
git clone <リポジトリのURL>
cd my-chatbot-project
```
2. バックエンドのセットアップ
```
cd backend
```

#### 仮想環境を作成して有効化
```python
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 必要なライブラリをインストール
pip install -r requirements.txt

# .envファイルを作成してAPIキーを設定
cp .env.example .env
# .envファイルを開き、ご自身のOpenAI APIキーを記述してください
# 例 : OPENAI_API_KEY="sk-○○○"
```
### 3. フロントエンドのセットアップ
２つ目のターミナルを開き、reactの環境を構築
```bash
cd frontend

# 必要なライブラリをインストール
npm install
```
### 4. アプリケーションの起動

ターミナル1 (バックエンド):

```bash
cd backend
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
uvicorn main:app --reload
```
ターミナル2 (フロントエンド):

```bash
cd frontend
npm start
# ブラウザで http://localhost:3000 を開いてください。
```

