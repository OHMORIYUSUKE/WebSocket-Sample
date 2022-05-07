from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fastapi.responses import HTMLResponse

from notifier import Notifier


app = FastAPI()
# プッシュ通知各種設定が定義されているインスタンス
notifier = Notifier()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
            // http get
            var HttpClient = function() {
                this.get = function(aUrl, aCallback) {
                    var anHttpRequest = new XMLHttpRequest();
                    anHttpRequest.onreadystatechange = function() { 
                        if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                            aCallback(anHttpRequest.responseText);
                    }

                    anHttpRequest.open( "GET", aUrl, true );            
                    anHttpRequest.send( null );
                }
            }
            const client = new HttpClient();
            client.get('http://localhost:8000/message', function(response) {
                // do something with response
                let jsonData = JSON.parse(response);
                console.log(jsonData);
                for(let i = 0; i < jsonData.length; i++){
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(jsonData[i].message)
                    message.appendChild(content)
                    messages.appendChild(message)
                }
            });
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

# ---
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

# 接続したいDBの基本情報を設定
DB_USER_NAME = "test"
DB_PW = "test"
DB_HOST = "db"
DB_NAME = "fuel_dev"

DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
    DB_USER_NAME,
    DB_PW,
    DB_HOST,
    DB_NAME,
)

# DBとの接続
ENGINE = create_engine(DATABASE, encoding="utf-8", echo=True)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するか
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)

from sqlalchemy import text
# ---
# Websocket用のパス
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # クライアントとのコネクション確立
    await notifier.connect(websocket)
    try:
        while True:
            # クライアントからメッセージの受け取り
            data = await websocket.receive_text()
            # 双方向通信する場合
            #  await websocket.send_text(f"Message text was: {data}")
            # db insert
            with ENGINE.begin() as conn:
                result = conn.execute(
                    text(
                        "INSERT INTO `message` (message) VALUES (:message)"
                    ),
                    {"message": f"Message text was: {data}"},
                )
            # ---
            # ブロードキャスト
            await notifier.push(f"Message text was: {data}")
    # セッションが切れた場合
    except WebSocketDisconnect:
        # 切れたセッションの削除
        notifier.remove(websocket)

# db get
@app.get("/message")
async def get_message():
    with ENGINE.begin() as conn:
        result = conn.execute(
            text(
                "SELECT * FROM `message`"
            )
        )
    message_list = []
    for data in result:
        message_list.append({"message": data.message})
    return message_list

# ブロードキャスト用のAPI
@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    # ブロードキャスト
    await notifier.push(f"! Push notification: {message} !")

# サーバ起動時の処理
@app.on_event("startup")
async def startup():
    # プッシュ通知の準備
    await notifier.generator.asend(None)