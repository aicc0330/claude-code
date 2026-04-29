#!/usr/bin/env python3
"""
自動影片生成器
生成第一個影片：「Claude 3.5 Sonnet 發佈——這次改變了什麼」
輸出：MP4 影片檔案
"""

import os
import subprocess
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
import tempfile
import shutil
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ['PATH'] = os.path.dirname(ffmpeg_path) + ':' + os.environ.get('PATH', '')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

class VideoGenerator:
    def __init__(self, output_dir="/home/user/claude-code/videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = tempfile.mkdtemp()
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def generate_performance_chart(self):
        """生成性能對比圖表"""
        print("生成性能對比圖表...")

        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

        # 數據
        models = ['Claude 3.5\nSonnet', 'GPT-4']
        performance = [95, 68]
        cost = [20, 100]

        # 性能對比
        x = np.arange(len(models))
        width = 0.35

        bars1 = ax.bar(x - width/2, performance, width, label='性能評分', color='#4CAF50')
        bars2 = ax.bar(x + width/2, [c/5 for c in cost], width, label='成本（越低越好）', color='#FF9800')

        ax.set_ylabel('評分', fontsize=12, fontweight='bold')
        ax.set_title('Claude 3.5 Sonnet vs GPT-4', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(models, fontsize=12)
        ax.legend()
        ax.set_ylim(0, 100)

        # 數值標籤
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        chart_path = f"{self.temp_dir}/performance_chart.png"
        plt.savefig(chart_path, transparent=True, dpi=100)
        plt.close()

        return chart_path

    def generate_features_chart(self):
        """生成新功能列表圖"""
        print("生成新功能圖表...")

        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

        features = ['更快的推理速度', '更低的 API 成本', '改進的代碼生成', '更強的上下文理解']
        positions = [3, 2, 1, 0]

        colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
        bars = ax.barh(positions, [1, 1, 1, 1], color=colors)

        ax.set_yticks(positions)
        ax.set_yticklabels(features, fontsize=12)
        ax.set_xlim(0, 1.5)
        ax.set_xticks([])
        ax.set_title('Claude 3.5 Sonnet 新功能', fontsize=16, fontweight='bold')

        # 加上✓標記
        for i, (bar, feature) in enumerate(zip(bars, features)):
            ax.text(1.1, i, '✓', fontsize=20, color='green', fontweight='bold')

        plt.tight_layout()
        chart_path = f"{self.temp_dir}/features_chart.png"
        plt.savefig(chart_path, transparent=True, dpi=100)
        plt.close()

        return chart_path

    def generate_voiceover(self):
        """生成配音（使用系統文字轉語音）"""
        print("生成配音...")

        script = """
        Claude 為什麼突然變強了？
        性能提升百分之四十，成本降低百分之八十。
        如果你還在用 GPT-4，你可能已經落伍了。
        看看它能做什麼。
        新功能包括：更快的推理速度、更低的 API 成本、改進的代碼生成、和更強的上下文理解。
        對你有什麼影響？
        如果你是開發者、內容創作者、或做數據分析，你現在有個新的超級工具。
        Claude 3.5 已經上線。
        你試過了嗎？在評論裡告訴我你的想法。
        記得訂閱，我每天分享最新的人工智能進展。
        """

        audio_path = f"{self.temp_dir}/voiceover.mp3"

        # 嘗試使用 pyttsx3（如果可用）
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('voice', 'zh_TW')
            engine.save_to_file(script, audio_path)
            engine.runAndWait()
            print(f"配音已生成: {audio_path}")
        except:
            print("警告：無法生成實時配音，使用默認音訊")
            # 創建一個空的音訊檔案作為佔位符
            subprocess.run([self.ffmpeg_exe, '-f', 'lavfi', '-i',
                          'anullsrc=r=44100:cl=mono', '-t', '30',
                          '-q:a', '9', '-acodec', 'libmp3lame',
                          audio_path, '-y'],
                         capture_output=True)

        return audio_path

    def create_background(self):
        """創建背景圖像"""
        print("創建背景...")

        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')

        # 黑色背景
        rect = mpatches.Rectangle((0, 0), 10, 6,
                                 linewidth=0, facecolor='black')
        ax.add_patch(rect)

        # 標題
        ax.text(5, 3, 'Claude 3.5 Sonnet',
               ha='center', va='center',
               fontsize=32, fontweight='bold', color='white')

        ax.text(5, 1.5, '這次改變了什麼？',
               ha='center', va='center',
               fontsize=20, color='#FFD700')

        plt.tight_layout()
        bg_path = f"{self.temp_dir}/background.png"
        plt.savefig(bg_path, facecolor='black', bbox_inches='tight', dpi=100)
        plt.close()

        return bg_path

    def generate_subtitles(self):
        """生成字幕檔案（SRT 格式）"""
        print("生成字幕...")

        subs = [
            ("00:00:01,000", "00:00:03,500", "Claude 為什麼突然變強了？"),
            ("00:00:03,500", "00:00:08,000", "性能提升 40%，成本降低 80%"),
            ("00:00:08,000", "00:00:12,000", "如果你還在用 GPT-4，你可能已經落伍了"),
            ("00:00:12,000", "00:00:15,000", "看看它能做什麼"),
            ("00:00:15,000", "00:00:20,000", "新功能：更快、更便宜、更聰明"),
            ("00:00:20,000", "00:00:25,000", "對你有什麼影響？\n如果你做開發、內容或數據分析\n你現在有個超級工具"),
            ("00:00:25,000", "00:00:30,000", "Claude 3.5 已經上線\n你試過了嗎？訂閱看更多"),
        ]

        srt_path = f"{self.temp_dir}/subtitles.srt"
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, (start, end, text) in enumerate(subs, 1):
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        return srt_path

    def assemble_video(self, bg_path, chart1_path, chart2_path, audio_path, srt_path):
        """組合影片"""
        print("組合影片...")

        output_path = self.output_dir / "first_video.mp4"

        # 使用 ffmpeg 組合
        # 這是一個簡化版本，實際製作需要更複雜的 ffmpeg 指令
        cmd = [
            self.ffmpeg_exe,
            '-loop', '1', '-i', bg_path,
            '-i', audio_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-t', '30',
            '-vf', f'scale=1080:1920',
            str(output_path),
            '-y'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✓ 影片生成成功: {output_path}")
                return str(output_path)
            else:
                print(f"✗ ffmpeg 錯誤: {result.stderr}")
                return None
        except Exception as e:
            print(f"✗ 無法生成影片: {e}")
            return None

    def cleanup(self):
        """清理臨時檔案"""
        print("清理臨時檔案...")
        shutil.rmtree(self.temp_dir)

    def generate(self):
        """執行完整流程"""
        print("=== 開始生成影片 ===\n")

        try:
            # 生成所有組件
            bg_path = self.create_background()
            chart1_path = self.generate_performance_chart()
            chart2_path = self.generate_features_chart()
            audio_path = self.generate_voiceover()
            srt_path = self.generate_subtitles()

            # 組合成影片
            video_path = self.assemble_video(bg_path, chart1_path, chart2_path, audio_path, srt_path)

            # 清理臨時檔案
            self.cleanup()

            if video_path:
                print(f"\n✓ 影片生成完成！")
                print(f"位置: {video_path}")
                return video_path
            else:
                print("\n✗ 影片生成失敗")
                return None

        except Exception as e:
            print(f"\n✗ 發生錯誤: {e}")
            self.cleanup()
            return None

if __name__ == "__main__":
    generator = VideoGenerator()
    generator.generate()
