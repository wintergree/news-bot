# naver_news.py
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

def search_news(keyword: str, display: int = 5) -> list:
    """네이버 뉴스 API로 키워드 검색 후 기사 목록 반환"""
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
        "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET")
    }
    params = {
        "query": keyword,
        "display": display,
        "sort": "date"       # 최신순
    }

    res = requests.get(url, headers=headers, params=params)

    if res.status_code != 200:
        print(f"[오류] 네이버 API 호출 실패: {res.status_code}")
        return []

    items = res.json().get("items", [])
    articles = []
    for item in items:
        articles.append({
            "title":   _clean(item["title"]),
            "desc":    _clean(item["description"]),
            "link":    item["link"],
            "pubDate": item["pubDate"]
        })
    return articles

def _clean(text: str) -> str:
    """HTML 태그 제거"""
    return re.sub(r"<.*?>", "", text)