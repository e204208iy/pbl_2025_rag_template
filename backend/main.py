import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) の設定
# フロントエンド(React)からのリクエストを許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangChainの設定
# temperature=0で、より決定的で一貫した応答を生成
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
# 会話履歴を保存するメモリ
memory = ConversationBufferMemory()
# メモリとLLMを組み合わせた会話チェーン
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

# フロントエンドから受け取るデータモデルを定義
class Message(BaseModel):
    text: str

# 応答をストリーミングするための非同期ジェネレータ関数
async def stream_generator(user_input: str):
    # LangChainのastream（非同期ストリーム）を使って応答をチャンクで取得
    async for chunk in conversation.astream({"input": user_input}):
        if "response" in chunk:
            yield chunk["response"]

# チャット用のAPIエンドポイント
@app.post("/chat")
async def chat_stream(message: Message):
    # StreamingResponseを使って、ジェネレータからの出力をリアルタイムで送信
    return StreamingResponse(stream_generator(message.text), media_type="text/event-stream")