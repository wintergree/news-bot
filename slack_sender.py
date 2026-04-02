# slack_sender.py
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def send_news_summary(keyword: str, summary: str, articles: list, user_name: str = ""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 원문 링크 버튼 (최대 3개)
    link_elements = []
    for i, article in enumerate(articles[:3], 1):
        link_elements.append({
            "type": "button",
            "text": {"type": "plain_text", "text": f"{i}. 원문 보기"},
            "url": article["link"]
        })

    requested_by = f" | 요청: @{user_name}" if user_name else ""

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📰 {keyword} 뉴스 브리핑"}
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn",
                          "text": f"🕐 {now} 기준{requested_by}"}]
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": summary}
        },
        {"type": "divider"},
        {
            "type": "actions",
            "elements": link_elements
        }
    ]

    try:
        client.chat_postMessage(
            channel=os.getenv("SLACK_CHANNEL_ID"),
            blocks=blocks,
            text=f"{keyword} 뉴스 요약"
        )
        print(f"[완료] '{keyword}' 슬랙 전송 성공")
    except SlackApiError as e:
        print(f"[오류] 슬랙 전송 실패: {e.response['error']}")
