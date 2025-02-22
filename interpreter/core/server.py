import asyncio
import json
from typing import Generator

import uvicorn
from fastapi import Body, FastAPI, Request, Response, WebSocket
from fastapi.responses import PlainTextResponse, StreamingResponse

import interpreter


def server(interpreter, host="0.0.0.0", port=9999):
    app = FastAPI()



    from fastapi.responses import StreamingResponse
    @app.post("/stream/chat/completions")
    async def stream_endpoint(request: Request):
        async def event_stream():
            data = await request.json() 
            for response in interpreter.chat(message=data["message"], stream=True):
                yield response  # 这里可以是 yield f"data: {response}\n\n" 如果你想要遵循 SSE 格式

        return StreamingResponse(event_stream(), media_type="text/event-stream")
    
    from fastapi.responses import JSONResponse
    @app.post("/chat/completions")
    async def chat_endpoint(request: Request):
        data = await request.json()
        messages = []
        for response in interpreter.chat(message=data["message"], stream=False):
            messages.append(response)
        return JSONResponse(content={"messages": messages})

    # Post endpoint
    # @app.post("/iv0", response_class=PlainTextResponse)
    # async def i_post_endpoint(request: Request):
    #     message = await request.body()
    #     message = message.decode("utf-8")  # Convert bytes to string

    #     async def event_stream() -> Generator[str, None, None]:
    #         for response in interpreter.chat(
    #             message=message, stream=True, display=False
    #         ):
    #             if (
    #                 response.get("type") == "message"
    #                 and response["role"] == "assistant"
    #                 and "content" in response
    #             ):
    #                 yield response["content"] + "\n"
    #             if (
    #                 response.get("type") == "message"
    #                 and response["role"] == "assistant"
    #                 and response.get("end") == True
    #             ):
    #                 yield " \n"

    #     return StreamingResponse(event_stream(), media_type="text/plain")

    @app.get("/test")
    async def test_ui():
        return PlainTextResponse(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Chat</title>
            </head>
            <body>
                <form action="" onsubmit="sendMessage(event)">
                    <textarea id="messageInput" rows="10" cols="50" autocomplete="off"></textarea>
                    <button>Send</button>
                </form>
                <div id="messages"></div>
                <script>
                    var ws = new WebSocket("ws://localhost:8000/");
                    var lastMessageElement = null;
                    ws.onmessage = function(event) {
                        if (lastMessageElement == null) {
                            lastMessageElement = document.createElement('p');
                            document.getElementById('messages').appendChild(lastMessageElement);
                        }
                        lastMessageElement.innerHTML += event.data;
                    };
                    function sendMessage(event) {
                        event.preventDefault();
                        var input = document.getElementById("messageInput");
                        var message = input.value;
                        if (message.startsWith('{') && message.endsWith('}')) {
                            message = JSON.stringify(JSON.parse(message));
                        }
                        ws.send(message);
                        var userMessageElement = document.createElement('p');
                        userMessageElement.innerHTML = '<b>' + input.value + '</b><br>';
                        document.getElementById('messages').appendChild(userMessageElement);
                        lastMessageElement = document.createElement('p');
                        document.getElementById('messages').appendChild(lastMessageElement);
                        input.value = '';
                    }
                </script>
            </body>
            </html>
            """,
            media_type="text/html",
        )

    @app.websocket("/")
    async def i_test(websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            while data.strip().lower() != "stop":  # Stop command
                task = asyncio.create_task(websocket.receive_text())

                # This would be terrible for production. Just for testing.
                try:
                    data_dict = json.loads(data)
                    if set(data_dict.keys()) == {"role", "content", "type"} or set(
                        data_dict.keys()
                    ) == {"role", "content", "type", "format"}:
                        data = data_dict
                except json.JSONDecodeError:
                    pass

                for response in interpreter.chat(
                    message=data, stream=True, display=False
                ):
                    if task.done():
                        data = task.result()  # Get the new message
                        break  # Break the loop and start processing the new message
                    # Send out assistant message chunks
                    if (
                        response.get("type") == "message"
                        and response["role"] == "assistant"
                        and "content" in response
                    ):
                        await websocket.send_text(response["content"])
                        await asyncio.sleep(0.01)  # Add a small delay
                    if (
                        response.get("type") == "message"
                        and response["role"] == "assistant"
                        and response.get("end") == True
                    ):
                        await websocket.send_text("\n")
                        await asyncio.sleep(0.01)  # Add a small delay
                if not task.done():
                    data = (
                        await task
                    )  # Wait for the next message if it hasn't arrived yet

    print(
        "\nOpening a simple `interpreter.chat(data)` POST endpoint at http://localhost:8000/chat."
    )
    print(
        "Opening an `i.protocol` compatible WebSocket endpoint at http://localhost:8000/."
    )
    print("\nVisit http://localhost:9999/test to test the WebSocket endpoint.\n")

    uvicorn.run(app, host=host, port=port)


