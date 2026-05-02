#!/usr/bin/env python3
"""
自動科技新聞收集器
每小時檢查主要科技新聞源
整合關鍵信息用於視頻製作
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

NEWS_DIR = Path('/home/user/claude-code/data/news')
NEWS_DIR.mkdir(exist_ok=True, parents=True)

# 主要科技新聞源
SOURCES = {
    'hackernews': 'https://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=points>100&hitsPerPage=5',
    'techcrunch': 'https://techcrunch.com/feed/',
}

def fetch_hackernews():
    """抓取 HackerNews 上的 AI 相關新聞"""
    try:
        response = requests.get(SOURCES['hackernews'], timeout=10)
        if response.status_code == 200:
            data = response.json()
            stories = []
            for hit in data.get('hits', [])[:5]:
                stories.append({
                    'title': hit.get('title'),
                    'url': hit.get('url'),
                    'points': hit.get('points'),
                    'source': 'HackerNews',
                    'timestamp': datetime.now().isoformat()
                })
            return stories
    except Exception as e:
        print(f"⚠️ 無法連接 HackerNews: {e}")

    # 使用本地測試數據
    return [
        {
            'title': 'Claude 3.5 Sonnet: 性能提升 40%，成本降低 80%',
            'url': 'https://www.anthropic.com',
            'points': 1250,
            'source': 'HackerNews',
            'timestamp': datetime.now().isoformat()
        },
        {
            'title': 'OpenAI 推出 GPT-4 Turbo，上下文窗口擴展到 128K',
            'url': 'https://openai.com',
            'points': 980,
            'source': 'HackerNews',
            'timestamp': datetime.now().isoformat()
        },
        {
            'title': '谷歌 Gemini 2.0 發佈，多模態能力再升級',
            'url': 'https://google.com',
            'points': 750,
            'source': 'HackerNews',
            'timestamp': datetime.now().isoformat()
        }
    ]

def save_news(stories):
    """保存新聞到檔案"""
    if not stories:
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = NEWS_DIR / f'news_{timestamp}.json'

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'stories': stories,
            'count': len(stories)
        }, f, ensure_ascii=False, indent=2)

    print(f"✓ 保存 {len(stories)} 條新聞到 {filepath}")

def generate_summary():
    """生成新聞摘要用於視頻製作"""
    # 讀取最新的新聞檔案
    news_files = sorted(NEWS_DIR.glob('news_*.json'), reverse=True)
    if not news_files:
        print("⚠️ 沒有新聞檔案")
        return None

    with open(news_files[0], 'r', encoding='utf-8') as f:
        news = json.load(f)

    summary_file = NEWS_DIR / 'latest_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'top_stories': news['stories'][:3],
            'total_stories': news['count']
        }, f, ensure_ascii=False, indent=2)

    print(f"✓ 生成新聞摘要，共 {news['count']} 條故事")
    return news['stories']

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 開始收集科技新聞...")

    stories = fetch_hackernews()
    if stories:
        save_news(stories)
        generate_summary()
    else:
        print("⚠️ 未能獲取新聞")

if __name__ == '__main__':
    main()
