import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

# LangChainの関連モジュール
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

# .envファイルから環境変数を読み込む
load_dotenv()

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 修正点 1: historyを削除 ---
# フロントエンドから受け取るデータモデルを単純化
class ChatRequest(BaseModel):
    text: str


# ストリーミング応答を生成するジェネレータ関数
# --- 修正点 2: history引数を削除 ---
async def stream_generator(user_input: str):
    # コールバックハンドラはリクエストごとに新しいインスタンスを作成
    callback = AsyncIteratorCallbackHandler()

    # LLMの初期化
    # streaming=Trueとcallbacks=[callback]がストリーミングの鍵
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True,
        callbacks=[callback],
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful chatbot."),
        ("human", "{input}"),
    ])

    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

    # LLMの実行をバックグラウンドタスクとして開始
    task = asyncio.create_task(
        chain.acall({"input": user_input})
    )

    # コールバックハンドラからトークンを一つずつ取得してyieldする
    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"ストリームの途中でエラーが発生しました: {e}")
    finally:
        # タスクの完了を待つ
        await task

@app.post("/chat")
async def chat_stream(request: ChatRequest):
    # StreamingResponseを使って、ジェネレータからの出力をリアルタイムで送信
    # --- 修正点 6: historyを渡さないように変更 ---
    return StreamingResponse(
        stream_generator(request.text),
        media_type="text/plain"
    )
