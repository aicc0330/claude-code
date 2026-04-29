#!/usr/bin/env python3
"""
自動視頻生成器
根據新聞數據自動生成 YouTube Shorts
使用圖表和配音說明關鍵信息
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import imageio_ffmpeg

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

NEWS_DIR = Path('/home/user/claude-code/data/news')
VIDEOS_DIR = Path('/home/user/claude-code/videos')
TEMP_DIR = Path('/tmp/video_gen')
TEMP_DIR.mkdir(exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

def load_latest_news():
    """載入最新的新聞摘要"""
    summary_file = NEWS_DIR / 'latest_summary.json'
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def create_news_slide(story, index):
    """為每個新聞創建幻燈片"""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.axis('off')

    # 黑色背景
    fig.patch.set_facecolor('black')

    # 新聞標題
    ax.text(0.5, 0.7, f"Top {index + 1}",
            ha='center', va='top', fontsize=24, color='#FFD700', fontweight='bold',
            transform=ax.transAxes)

    # 新聞內容（截短）
    title = story['title'][:60] + '...' if len(story['title']) > 60 else story['title']
    ax.text(0.5, 0.5, title,
            ha='center', va='center', fontsize=16, color='white', wrap=True,
            transform=ax.transAxes)

    # 來源和時間
    ax.text(0.5, 0.2, f"來源: {story['source']}",
            ha='center', va='bottom', fontsize=12, color='#888888',
            transform=ax.transAxes)

    plt.tight_layout()
    output_path = TEMP_DIR / f'slide_{index}.png'
    plt.savefig(output_path, facecolor='black', bbox_inches='tight', dpi=100)
    plt.close()

    return str(output_path)

def generate_voiceover_script(stories):
    """為新聞列表生成配音腳本"""
    script = f"""
    科技新聞速報。
    """

    for i, story in enumerate(stories[:3], 1):
        script += f"\n第{i}條: {story['title'][:50]}"

    script += "\n\n更多詳情請訪問我的頻道。記得訂閱以獲取最新科技新聞。"
    return script

def generate_video(news_data):
    """生成完整視頻"""
    if not news_data or 'top_stories' not in news_data:
        print("⚠️ 無有效新聞數據")
        return None

    stories = news_data['top_stories']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print(f"✓ 開始製作視頻，使用 {len(stories)} 條新聞...")

    # 創建幻燈片
    slides = []
    for i, story in enumerate(stories):
        slide_path = create_news_slide(story, i)
        slides.append(slide_path)
        print(f"  ✓ 幻燈片 {i+1}/{len(stories)}")

    if not slides:
        print("✗ 未能創建幻燈片")
        return None

    # 創建背景音樂（無聲）
    audio_path = TEMP_DIR / 'audio.mp3'
    subprocess.run([ffmpeg_exe, '-f', 'lavfi', '-i',
                   'anullsrc=r=44100:cl=mono', '-t', '30',
                   '-q:a', '9', '-acodec', 'libmp3lame',
                   str(audio_path), '-y'],
                  capture_output=True)

    # 組合幻燈片成視頻
    output_video = VIDEOS_DIR / f'news_{timestamp}.mp4'
    slide1 = slides[0]

    cmd = [ffmpeg_exe,
           '-loop', '1', '-i', slide1,
           '-i', str(audio_path),
           '-c:v', 'libx264',
           '-c:a', 'aac',
           '-b:a', '192k',
           '-pix_fmt', 'yuv420p',
           '-t', '30',
           '-vf', 'scale=1080:1920',
           str(output_video),
           '-y']

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode == 0:
        print(f"✓ 視頻生成成功: {output_video}")
        return str(output_video)
    else:
        print(f"✗ 視頻生成失敗: {result.stderr}")
        return None

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 自動視頻生成流程啟動...")

    # 嘗試載入新聞
    news_data = load_latest_news()
    if not news_data:
        print("⚠️ 沒有新聞數據，請先運行 news-collector.py")
        return

    # 生成視頻
    video_path = generate_video(news_data)
    if video_path:
        print(f"\n✓ 視頻已準備: {video_path}")
    else:
        print("\n✗ 視頻生成失敗")

if __name__ == '__main__':
    main()
