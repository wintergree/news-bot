# summarizer.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(keyword: str, articles: list) -> str:
    """기사 목록을 받아 GPT로 3줄 핵심 요약 생성"""
    if not articles:
        return f"'{keyword}' 관련 뉴스를 찾지 못했습니다."

    # 기사 내용을 하나의 텍스트로 합치기
    content = "\n\n".join([
        f"제목: {a['title']}\n내용: {a['desc']}"
        for a in articles
    ])

    prompt = f"""다음은 '{keyword}' 관련 최신 뉴스 기사들입니다.

{content}

위 기사들을 바탕으로:
1. 핵심 내용을 3줄로 요약해주세요
2. 각 줄은 • 로 시작해주세요
3. 전문용어는 쉽게 풀어서 설명해주세요
4. 마지막에 한 줄로 시사점을 추가해주세요"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",    # 비용 절약형. gpt-4o도 가능
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3
    )
    return response.choices[0].message.content