# main.py
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from naver_news import search_news
from summarizer import summarize
from slack_sender import send_news_summary

load_dotenv()
app = FastAPI()

@app.get("/")
def health_check():
    """Railway 헬스체크용"""
    return {"status": "ok", "service": "뉴스요약봇"}

@app.post("/slack/news")
async def slack_news_command(
    background_tasks: BackgroundTasks,
    text: str = Form(default=""),           # 슬랙이 보내는 검색어
    response_url: str = Form(default=""),   # 슬랙이 보내는 응답 URL
    user_name: str = Form(default=""),      # 요청한 사용자 이름
):
    keyword = text.strip()

    # 키워드 없이 /뉴스만 입력한 경우
    if not keyword:
        return JSONResponse(content={
            "response_type": "ephemeral",   # 본인에게만 보임
            "text": "검색어를 입력해주세요. 예) `/뉴스 AI반도체`"
        })

    # 슬랙에 즉시 "검색 중..." 응답 (3초 제한 대응)
    background_tasks.add_task(
        process_and_send, keyword, response_url, user_name
    )

    return JSONResponse(content={
        "response_type": "in_channel",      # 채널 전체에 보임
        "text": f"🔍 *{user_name}* 님이 *{keyword}* 뉴스를 요청했습니다. 잠시만 기다려주세요..."
    })

def process_and_send(keyword: str, response_url: str, user_name: str):
    """백그라운드에서 검색 → 요약 → 슬랙 전송"""
    print(f"[처리 시작] '{keyword}' - 요청자: {user_name}")

    articles = search_news(keyword, display=5)
    print(f"  → 기사 {len(articles)}건 수집")

    summary = summarize(keyword, articles)
    print(f"  → 요약 완료")

    send_news_summary(keyword, summary, articles, user_name)
    print(f"  → 슬랙 전송 완료")