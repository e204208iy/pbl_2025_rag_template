🚀 セットアップ手順
このプロジェクトを実行するための手順です。

1. リポジトリをクローン
Bash

git clone <リポジトリのURL>
cd my-chatbot-project
2. バックエンドのセットアップ
Bash

cd backend

# 仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 必要なライブラリをインストール
pip install -r requirements.txt

# .envファイルを作成してAPIキーを設定
cp .env.example .env
# .envファイルを開き、ご自身のOpenAI APIキーを記述してください
補足: .env.exampleというファイルを事前に作成し、「ここにAPIキーを入力してください」というテンプレートを書いておくと、さらに親切です。

3. フロントエンドのセットアップ
Bash

cd ../frontend

# 必要なライブラリをインストール
npm install
4. アプリケーションの起動
ターミナルを2つ開き、それぞれで以下のコマンドを実行します。

ターミナル1 (バックエンド):

Bash

cd backend
source venv/bin/activate
uvicorn main:app --reload
ターミナル2 (フロントエンド):

Bash

cd frontend
npm start
ブラウザで http://localhost:3000 を開いてください。

