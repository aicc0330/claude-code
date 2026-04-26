# 完整開發規格書：全亞洲 AI 科技情報短影音工廠
## Information Arbitrage × 全亞洲多語系變現

---

## 一、 核心商業模式與技術架構

### 商業目標
透過 **Information Arbitrage（資訊套利）**，全自動監控歐美頂尖 AI 科技 YouTube 頻道，將第一手技術情報（開源模型、算力硬體、影視製作）轉譯並裂變為**全亞洲多國語系**的短影音，快速變現並擴張影像工作室的跨國影響力與規模。

### 目標市場與語言

```
東亞市場（人口 15 億）
├─ 繁體中文（台灣）- YouTube Shorts 月活躍：500 萬+
├─ 日本語（日本）- YouTube Shorts 月活躍：2000 萬+
└─ 韓國語（韓國）- YouTube Shorts 月活躍：800 萬+

東南亞市場（人口 7 億，增長最快）
├─ ไทย（泰國）- TikTok 滲透率 85%，年輕人佔 60%
├─ Tiếng Việt（越南）- 字幕內容消費量年增 40%
└─ Bahasa Indonesia（印尼）- 東南亞最大社群媒體市場

南亞市場（未來機會）
├─ हिन्दी（印度） - 可選擇性納入 Phase 2
└─ 其他次要語言 - 按 ROI 評估

總覆蓋：每支內容 6-8 種語言，覆蓋亞洲 30 億人口
```

### 技術堆棧

```
【資訊來源層】
  YouTube (歐美頻道)
    ↓
【監控 & 收集層】
  IFTTT (自動 URL 收集)
  Google Sheets (人工篩選隊列)
  YouTube to NotebookLM (一鍵批量匯入)
    ↓
【雲端智能過濾層】
  NotebookLM (多筆記本分類結構)
  NotebookLM MCP (自動化控制)
    ↓
【本地自動化編導層】
  Claude Code (核心編排引擎)
  YT Search Skill (監控自動化)
  Python 腳本 (輔助工具)
    ↓
【本地知識大腦層】
  ~/studio_ai_brain/ (持續成長記憶)
  Git (版本控制)
    ↓
【多語系生成層】
  Claude API (多語言改寫)
  ElevenLabs V3 API (情緒配音)
  PixVerse / Kling (B-roll 生成)
  MoviePy (自動剪輯)
    ↓
【發佈層】
  TikTok / Instagram Reels / YouTube Shorts
  (同步 6-8 語言版本)
```

---

## 二、 Ubuntu 本機端完整目錄結構

### 2.1 頂層結構

```bash
# 初始化
mkdir -p ~/ai_content_hub/{01_raw_ingest,02_knowledge_base,03_video_scripts,04_automation_scripts,05_logs}
mkdir -p ~/studio_ai_brain/{01_Inbox,02_Concepts,03_Sources}
cd ~/ai_content_hub && git init
```

### 2.2 完整的目錄樹

```
~/ai_content_hub/
│
├─ 01_raw_ingest/                    # 【來源暫存區】
│  ├─ notebooklm_exports/            # NotebookLM 匯出的 Markdown 報告
│  │  ├─ 20260427_ai_image_gen.md
│  │  ├─ 20260427_gpu_hardware.md
│  │  └─ 20260427_video_editing.md
│  │
│  ├─ youtube_raw_transcripts/       # YouTube 原始字幕（備份用）
│  │  ├─ mattWolfe_happyHorse.txt
│  │  └─ twoMinutePapers_gpu.txt
│  │
│  └─ processed_flag/                # 已處理的標記檔案
│     └─ 20260427_processed.log
│
├─ 02_knowledge_base/                # 【知識成長區】
│  ├─ concepts/                      # 核心知識節點
│  │  ├─ AI_IMAGE_GENERATION.md      # 某主題的持續更新筆記
│  │  ├─ GPU_HARDWARE_TRENDS.md
│  │  ├─ VIDEO_PRODUCTION.md
│  │  ├─ LLM_APPLICATIONS.md
│  │  ├─ VOICE_TECHNOLOGY.md
│  │  └─ VIRAL_HOOKS.md              # 爆款開場白資料庫
│  │
│  ├─ metadata/                      # 知識元數據
│  │  ├─ language_support.json       # 各主題的支援語言清單
│  │  ├─ source_tracking.json        # 來源追蹤記錄
│  │  └─ update_history.json         # 更新時間軸
│  │
│  └─ index.md                       # 知識導航與關聯圖
│
├─ 03_video_scripts/                 # 【多語系腳本產出區】
│  ├─ zh_TW/                         # 繁體中文（台灣）
│  │  ├─ 20260427_ai_image_gen_zh.md
│  │  └─ script_templates_zh.md
│  │
│  ├─ ja_JP/                         # 日本語
│  ├─ ko_KR/                         # 韓國語
│  ├─ th_TH/                         # ไทย
│  ├─ vi_VN/                         # Tiếng Việt
│  ├─ id_ID/                         # Bahasa Indonesia
│  │
│  ├─ visual_prompts/                # B-roll 視覺生成提示
│  │  ├─ ai_image_gen_visuals.txt
│  │  └─ gpu_rendering_visuals.txt
│  │
│  └─ emotional_tags/                # ElevenLabs 情緒標籤
│     ├─ ai_breakthroughs_tags.json
│     └─ tutorial_tags.json
│
├─ 04_automation_scripts/            # 【Python 自動化腳本】
│  ├─ radar.py                       # YT Search 監聽
│  ├─ notebooklm_connector.py        # NotebookLM MCP 操控
│  ├─ brain_router.py                # 本地大腦路由引擎
│  ├─ screenplay_engine.py           # 編劇系統（故事框架化）
│  ├─ localization_engine.py         # 多語系改寫引擎
│  ├─ audio_generator.py             # 配音生成（ElevenLabs API）
│  ├─ video_generator.py             # B-roll 與影片生成協調
│  ├─ scheduler.py                   # Cron 排程管理
│  ├─ requirements.txt               # Python 依賴清單
│  └─ config.json                    # 全局配置
│
├─ 05_logs/                          # 【執行日誌】
│  ├─ daily.log
│  ├─ errors.log
│  ├─ api_costs.log
│  └─ performance.log
│
└─ .git/                             # Git 版本控制
   └─ (自動管理)

~/studio_ai_brain/                   # 【本地知識大腦】
├─ 01_Inbox/
│  ├─ raw_transcripts/
│  └─ notebooklm_exports/
│
├─ 02_Concepts/
│  ├─ AI_IMAGE_GENERATION.md
│  ├─ GPU_HARDWARE_TRENDS.md
│  └─ [持續生長的主題筆記]
│
├─ 03_Sources/
│  └─ [已處理的摘要備份]
│
├─ index.md
└─ .git/                             # 本地大腦也使用 Git
```

---

## 三、 四階段全自動工作流（完整版本）

### 階段一：全球雷達自動捕獲 (YouTube Monitoring)

**工具**：Claude Code + YT Search Skill

**執行頻率**：每日 00:00 (午夜)

**具體步驟**：
```python
# radar.py
keywords = [
    # AI 影像生成
    "AI image generation", "stable diffusion", "happy horse",
    "DALL-E", "Midjourney", "open source models",
    
    # 硬體算力
    "GPU benchmark", "NVIDIA H100", "RTX 4090", "AI compute",
    "data center", "training infrastructure",
    
    # 影視製作
    "AI video generation", "PixVerse", "Kling", "motion capture",
    "visual effects", "AI filmmaking",
    
    # LLM 應用
    "Claude", "GPT-4", "LLM deployment", "enterprise AI",
    
    # 多語言配音
    "speech synthesis", "voice cloning", "ElevenLabs",
    "multilingual AI", "subtitle generation"
]

# 搜尋結果：取前 5 部最新、最熱門的英文影片
# 儲存格式：JSON
{
    "timestamp": "2026-04-27T00:15:00Z",
    "videos": [
        {
            "url": "https://youtube.com/watch?v=xxx1",
            "title": "...",
            "channel": "...",
            "duration": "45:32",
            "language": "en",
            "category": "ai_image_generation"
        },
        ...
    ]
}
```

**成功指標**：✓ 每日捕獲 5-10 部新影片

---

### 階段二：NotebookLM MCP 自動提煉生肉 (Content Extraction)

**工具**：Claude Code + NotebookLM MCP

**執行頻率**：每日 01:30 (凌晨)

**具體步驟**：

#### 2.1 自動匯入至 NotebookLM
```python
# notebooklm_connector.py

# 讀取昨天的 YouTube URL 清單
urls = load_json('01_raw_ingest/youtube_urls.json')

# NotebookLM MCP 自動匯入
for url in urls[:5]:  # 限制 5 部以控制成本
    notebook = determine_target_notebook(url)  # 自動判斷應該放進哪個筆記本
    nlm.add_source(
        notebook_id=notebook['id'],
        source_type="youtube",
        source_url=url
    )
```

#### 2.2 指令 NotebookLM 生成綜合報告
```
NotebookLM Prompt:

你是一位 AI 科技分析師，專精於協助亞洲市場的短影音製作人。

請分析這 5 部最新影片，生成一份結構化報告，包含：

### 1. 核心技術突破
- 列出 3-5 項最重要的新技術或更新
- 每項必須附上『來自哪部影片』的標註
- 標記『官方確認』或『第三方評測』

### 2. 市場影響與商業價值
- 這項技術對亞洲市場的意義
- 預期採用時間表
- 商業機會在哪裡

### 3. 硬體與成本需求
- 涉及的硬體（GPU 型號、規格）
- 市場報價（如有）
- 成本效益分析

### 4. 實際應用步驟
- 如果影片展示了實際操作，列出步驟
- 工具清單
- 常見問題與解決方案

### 5. 亞洲在地化機會
- 這項技術如何應用於台灣、日本、韓國、泰國、越南、印尼市場
- 各地區的特殊需求或限制
- 本地化改進方向

### 6. 後續追蹤
- 還有哪些相關影片或資源值得研究
- 下月的預期更新或發佈

---

輸出格式：結構化 Markdown，用繁體中文撰寫
```

#### 2.3 自動下載報告
```python
# 下載 Markdown 報告到本機
report = nlm.export_report(
    notebook_id=notebook['id'],
    format="markdown",
    output_path="01_raw_ingest/notebooklm_exports/20260427_synthesis.md"
)
```

**成功指標**：✓ 每日一份高質量的綜合報告存入本機

---

### 階段三：多語系影視腳本裂變 (Localization & Screenplay)

**工具**：Claude Code + Claude API + Local Brain

**執行頻率**：每日 03:00 (凌晨)

**具體步驟**：

#### 3.1 讀取報告 + 更新本地大腦
```python
# brain_router.py

report = load_markdown('01_raw_ingest/notebooklm_exports/xxx.md')

# 自動分類報告內容
topics = extract_topics(report)  # ['AI 影像生成', '硬體趨勢', ...]

# 觸發「滾動式記憶更新」
for topic in topics:
    concept_file = f"02_knowledge_base/concepts/{topic.upper()}.md"
    
    if exists(concept_file):
        # 讀取現有知識點
        existing = load_markdown(concept_file)
        
        # 融合新資訊（不覆蓋，只補充）
        merged = merge_knowledge(existing, report_section)
        
        # 寫回檔案
        save_markdown(concept_file, merged)
    else:
        # 建立新主題檔案
        create_new_concept(topic, report_section)

# 更新 index.md
update_knowledge_index()
```

#### 3.2 轉換成故事框架（編劇系統）
```python
# screenplay_engine.py

report = load_markdown('01_raw_ingest/notebooklm_exports/xxx.md')

screenplay = screenplay_engine.analyze_content(report)

# Claude API：分析 → 故事框架化
claude_prompt = f"""
分析這份技術報告，產出 60 秒短影音的故事框架：

技術報告：
{report}

場景設計（3 場景結構）：
1. 場景 1 (0-15秒)：問題 / 痛點
2. 場景 2 (15-45秒)：解決方案 / 技術優勢
3. 場景 3 (45-60秒)：結果 / 行動呼籲

輸出格式：JSON，包含場景描述、對白、視覺指示
"""

story = claude.messages.create(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": claude_prompt}]
)

save_json('screenplay.json', story)
```

#### 3.3 多語系改寫（全亞洲語言）
```python
# localization_engine.py

screenplay = load_json('screenplay.json')

languages = {
    'zh_TW': '繁體中文（台灣市場）- 融入職場、自媒體情境',
    'ja_JP': '日本語（日本市場）- 融入企業效率化、動漫製作情境',
    'ko_KR': '韓國語（韓國市場）- 融入 K-beauty、遊戲產業情境',
    'th_TH': 'ไทย（泰國市場）- 融入電商、年輕族群文化',
    'vi_VN': 'Tiếng Việt（越南市場）- 融入新創生態、年輕創業者情境',
    'id_ID': 'Bahasa Indonesia（印尼市場）- 融入數位經濟、社群文化'
}

for lang_code, lang_description in languages.items():
    localization_prompt = f"""
    根據這份英文短影音劇本，為 {lang_description} 改寫。
    
    原劇本：{screenplay}
    
    改寫原則：
    1. 保留技術準確性，但用當地語言邏輯表達
    2. 用當地常見的例子替換英文例子
    3. 融入該地區的文化與商業背景
    4. 確保 Hook（前 3 秒開場白）對當地觀眾有吸引力
    5. CTA（行動呼籲）適應當地平台與消費習慣
    
    輸出格式：結構化 Markdown，包含：
    - 場景對白
    - 視覺指示（B-roll Prompt）
    - 字幕
    - ElevenLabs 情緒標籤
    """
    
    localized = claude.messages.create(
        model="claude-3-5-sonnet",
        messages=[{"role": "user", "content": localization_prompt}]
    )
    
    save_markdown(f'03_video_scripts/{lang_code}/script_{date}.md', localized)
```

**成功指標**：✓ 生成 6-8 個語言版本的完整腳本

---

### 階段四：影視化生成與自動發佈 (Video Generation & Publishing)

**工具**：ElevenLabs + PixVerse + MoviePy + API 自動化

**執行頻率**：每日 06:00 - 12:00 (早上到中午)

#### 4.1 配音生成（多語言 + 情緒）
```python
# audio_generator.py

for lang_code in ['zh_TW', 'ja_JP', 'ko_KR', 'th_TH', 'vi_VN', 'id_ID']:
    script = load_markdown(f'03_video_scripts/{lang_code}/script.md')
    
    # 為每句話加上情緒標籤
    for sentence in script['voiceover']:
        emotion = determine_emotion(sentence)  # 'excited', 'calm', 'urgent'
        
        audio = elevenlabs.generate_voice(
            text=sentence,
            language=lang_code,
            emotion_tag=emotion,
            voice_id="professional_tech_narrator"
        )
        
        save_audio(audio, f'06_video_assets/voiceovers/{lang_code}_{idx}.mp3')
```

#### 4.2 B-roll 與視覺資產生成
```python
# video_generator.py

for shot in script['visual_prompts']:
    # PixVerse / Kling 自動生成 B-roll
    video = pixverse.generate_video(
        prompt=shot['prompt'],
        duration=shot['duration'],
        style="tech_professional"
    )
    
    save_video(video, f'06_video_assets/b_roll/{shot_id}.mp4')
```

#### 4.3 自動剪輯與合成
```python
# video_assembler.py (使用 MoviePy)

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip

for lang_code in languages:
    # 組合音檔、影片、字幕
    voiceover = AudioFileClip(f'voiceovers/{lang_code}.mp3')
    b_rolls = [VideoFileClip(f) for f in get_b_roll_files(lang_code)]
    subtitles = load_subtitles(f'03_video_scripts/{lang_code}/subtitles.vtt')
    
    # 自動對軌 + 調色 + 字幕
    final_video = assemble_and_grade(b_rolls, voiceover, subtitles, lang_code)
    
    # 三種格式輸出
    final_video.write_videofile(f'07_final_output/tiktok_vertical/{lang_code}_v1.mp4', size=(1080, 1920))
    final_video.write_videofile(f'07_final_output/youtube_shorts/{lang_code}_v1.mp4', size=(1080, 1920))
    final_video.write_videofile(f'07_final_output/4k/{lang_code}_v1.mp4', size=(3840, 2160))
```

#### 4.4 多平台自動發佈
```python
# auto_publisher.py

for lang_code in languages:
    metadata = generate_metadata(lang_code, date)
    
    # TikTok
    tiktok_api.post_video(
        video_path=f'tiktok_vertical/{lang_code}_v1.mp4',
        caption=metadata['caption'],
        hashtags=metadata['hashtags'],
        schedule_time=get_optimal_posting_time(lang_code)
    )
    
    # Instagram Reels
    instagram_api.post_reel(...)
    
    # YouTube Shorts
    youtube_api.post_short(...)
```

**成功指標**：✓ 18 個成品影片（6 語言 × 3 格式）同步發佈

---

## 四、 交給 Claude Code 的「啟動開發指令」

### 完整指令（複製貼上）

```
Claude Code，我們現在要在 Ubuntu 環境下開發一套『全亞洲 AI 科技情報短影音工廠』。

這是一個完整的、跨越雲端 + 本機的自動化系統，涵蓋監控、提煉、編導、多語系、影視化、發佈的完整流程。

【第一步：環境準備】
1. 幫我全局 (globally) 安裝並設置 NotebookLM MCP
2. 幫我全局安裝 YT Search Skill
3. 在 ~/ai_content_hub 中初始化 Git 倉庫
4. 建立上述的完整目錄結構

【第二步：Python 腳本開發】
請為我撰寫以下 6 支核心 Python 腳本，放在 04_automation_scripts/:

1. radar.py
   - 使用 YouTube API v3 監聽指定的歐美頻道與關鍵字
   - 每日 00:00 自動搜尋並存儲前 5-10 部最新英文影片 URL
   - 輸出格式：JSON (存入 01_raw_ingest/youtube_urls.json)

2. notebooklm_connector.py
   - 使用 NotebookLM MCP 自動匯入 YouTube URL
   - 自動判斷應該匯入到哪個 NotebookLM 筆記本（基於內容分類）
   - 自動指令 NotebookLM 生成綜合報告
   - 自動下載報告到本機 01_raw_ingest/notebooklm_exports/
   - 輸出格式：Markdown

3. brain_router.py
   - 讀取 NotebookLM 報告
   - 實現「滾動式記憶更新」邏輯（追加，不覆蓋）
   - 自動分類信息，更新 02_knowledge_base 中的對應主題檔案
   - 保持源追蹤（標註每項信息的來源）
   - 更新 index.md

4. screenplay_engine.py
   - 讀取知識點，轉換成故事框架（3 場景結構）
   - 生成場景對白、視覺指示、情緒標籤
   - 輸出格式：JSON

5. localization_engine.py
   - 讀取劇本，產出全亞洲多國語系版本
   - 語言清單：繁中、日、韓、泰、越、印尼文（共 6 種）
   - 每個語言版本必須融入當地文化與商業背景
   - 輸出格式：結構化 Markdown，按語言放入 03_video_scripts/{lang_code}/

6. scheduler.py
   - 使用 APScheduler 或 schedule 庫，設定每日自動排程
   - 00:00 → radar.py
   - 01:30 → notebooklm_connector.py
   - 03:00 → brain_router.py + screenplay_engine.py + localization_engine.py
   - 06:00 → audio_generator.py + video_generator.py
   - 08:00 → video_assembler.py + auto_publisher.py

【第三步：API 整合】
1. ElevenLabs V3 API - 多語系情緒配音
2. Claude API - 多語系改寫與故事框架化
3. YouTube Data API v3 - 監控
4. 各社群平台 API（TikTok / Instagram / YouTube）- 發佈

【第四步：成本控制】
請為 04_automation_scripts/ 寫一份 requirements.txt，包含：
- youtube-transcript-api
- yt-dlp
- google-auth-oauthlib
- elevenlabs
- anthropic (Claude SDK)
- moviepy
- schedule / APScheduler
- requests

【第五步：測試與驗證】
1. 先用「最新開源 AI 模型」這個關鍵字進行首次測試
2. 搜尋結果應該捕獲 3-5 部最新英文影片
3. 這些影片應該自動匯入 NotebookLM
4. NotebookLM 應該生成綜合報告並下載到本機
5. 本地大腦應該自動更新
6. 應該產出 6 語言版本的腳本
7. 應該生成配音與視覺資產
8. 最終應該生成 18 個成品影片（6 語言 × 3 格式）

【最後：交給我什麼？】
1. 完整的可執行 Python 腳本（已測試）
2. requirements.txt 與安裝指南
3. 簡單的執行手冊（如何每日運行、如何除錯）
4. Cron 配置範例（用於 Ubuntu 自動排程）
5. 成本監控儀表板（追蹤 API 費用）

謝謝！
```

---

## 五、 經濟效益與 ROI 分析

### 5.1 月度成本結構

| 項目 | 成本 | 說明 |
|------|------|------|
| NotebookLM | $0 | 完全免費 |
| Claude API (多語系改寫) | USD $40 | ~200 通話/月 |
| ElevenLabs V3 (配音) | USD $100 | 6 語言 × 30 日 |
| PixVerse / Kling (B-roll) | USD $30 | 批次生成折扣 |
| YouTube API | USD $0-5 | 免費層內 |
| 社群平台 API | USD $0 | 官方免費 |
| **Total** | **USD $170-175** | **年度 USD $2000** |

### 5.2 預期收入（保守估計）

```
假設：
- 每月發佈 30 支影片 × 6 語言 = 180 支
- 每支平均 100K 觀看
- CPM (Cost Per Mille) = USD $3-5
- 轉換率 (訂閱 → 商業合作) = 0.1%

月度收入預期：
  基礎廣告收益：180 支 × 100K × USD $4 CPM = USD $72,000
  商業合作（客製化內容）：USD $5,000 - $10,000
  課程 / 產品銷售：USD $3,000 - $5,000
  
  **月度總收入：USD $80,000 - $87,000**
  **年度收入：USD $1,000,000+**

ROI: (USD $1,000,000 - USD $2,000) / USD $2,000 = **49,900%**
```

### 5.3 關鍵成功因素

✅ **自動化程度**：系統須達到 95% 自動化，人工僅做品質檢查
✅ **內容品質**：每支影片必須符合短影音爆款標準（Hook + Value + CTA）
✅ **語言品質**：每個語言版本必須自然流暢，不能生硬翻譯
✅ **發佈時機**：針對各地區的最佳發佈時間進行排程
✅ **社群互動**：自動回覆評論、與粉絲互動（可用額外 AI 輔助）

---

## 六、 風險與緩解策略

### 6.1 技術風險

| 風險 | 影響 | 緩解策略 |
|------|------|---------|
| API 額度用完 | 系統停擺 | 監控 API 成本，設定每日上限 |
| NotebookLM 政策變更 | 整套系統失效 | 維護備用方案（本地 LLM） |
| YouTube 封號 | 無法監控更新 | 使用多個頻道源，避免過度依賴 |
| 語言品質下降 | 影片表現差 | 人工抽檢（每週 5% 樣本） |

### 6.2 商業風險

| 風險 | 影響 | 緩解策略 |
|------|------|---------|
| 內容農場競爭 | 流量分散 | 強化品牌差異化、建立粉絲社群 |
| 平台政策變更 | 被限流或下架 | 多平台發佈，不依賴單一平台 |
| 著作權爭議 | 法律問題 | 始終標註原始來源，不聲稱原創 |

---

## 七、 里程碑與驗收標準

### Week 1: 環境搭建
- [ ] NotebookLM MCP 安裝並認證成功
- [ ] 本機目錄結構建立完成
- [ ] Git 倉庫初始化

### Week 2-3: 核心腳本開發
- [ ] radar.py 能正常搜尋並存儲 YouTube URL
- [ ] notebooklm_connector.py 能自動匯入並生成報告
- [ ] brain_router.py 能正確更新知識庫

### Week 4: 多語系與影視化
- [ ] screenplay_engine.py 產出高質量故事框架
- [ ] localization_engine.py 生成 6 語言版本
- [ ] audio_generator.py 生成情緒配音

### Week 5: 全流程測試
- [ ] 首次完整運行（從 YouTube 監控到多平台發佈）
- [ ] 產出 18 個成品影片
- [ ] 人工檢驗品質（無明顯缺陷）

### Week 6+: 優化與上線
- [ ] 自動化排程運行
- [ ] 每日監控日誌
- [ ] 根據數據反饋調整

