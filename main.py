import gradio as gr
from datetime import datetime
from src.logic import process_ticket_request
from src.models import TicketRequest, Viewer


def ticket_request_interface(date, time, *ages):
    # 文字列からdatetimeオブジェクトへの変換
    datetime_str = f"{date} {time}"
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    # 年齢リストからViewerオブジェクトのリストを作成
    viewers = [Viewer(age=age) for age in ages if age is not None]  # None値を除外

    # TicketRequestオブジェクトの作成
    ticket_request = TicketRequest(currentDateTime=dt, viewers=viewers)

    # チケットリクエストを処理
    response = process_ticket_request(ticket_request)

    # レスポンスを文字列に変換して返す
    if response:
        if response.message:
            return f"Message: {response.message}"
        else:
            return f"Session DateTime: {response.sessionDateTime}, Total Price: {response.totalPrice}"
    else:
        return "No response generated."


# Gradioインターフェイスの定義
demo = gr.Interface(
    fn=ticket_request_interface,
    inputs=[
        gr.Textbox(label="Select Date (YYYY-MM-DD)"),
        gr.Textbox(label="Select Time (HH:MM)"),
        gr.Number(label="Viewer1 Age", minimum=0, maximum=100),
        gr.Number(
            label="Viewer2 Age", minimum=0, maximum=100, value=None
        ),
        gr.Number(
            label='Viewer3 Age', minimum=0, maximum=100, value=None
        ),
        gr.Number(
            label="Viewer4 Age", minimum=0, maximum=100, value=None
        ),
        gr.Number(
            label="Viewer5 Age", minimum=0, maximum=100, value=None
        ),
        gr.Number(
            label="Viewer6 Age", minimum=0, maximum=100, value=None
        ),

    ],
    outputs="text",
    description="Enter the date and time for the movie session, and the ages of viewers to process the ticket request.",
)

# Gradio Webアプリを起動
demo.launch()
