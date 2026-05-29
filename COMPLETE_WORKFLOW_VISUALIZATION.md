# 完整工作流運作說明
## Claude Code 在「全亞洲 AI 創意內容工廠」中的角色與協作模式

---

## 🎯 系統全景圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                     全亞洲 AI 創意內容工廠                             │
│                   (Asia-Wide AI Creative Factory)                    │
└─────────────────────────────────────────────────────────────────────┘

     ┌──────────────────┐
     │  歐美 AI 新聞源  │
     │  (YouTube, RSS)  │
     └────────┬─────────┘
              │
              ↓
    ┏━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  【階段 1】            ┃
    ┃ 全球資訊監聽 (Radar)  ┃  ← Claude Code 操控
    ┃  YT Search + RSS      ┃
    ┗━━━━━━━━━┬─────────────┛
              │ (YouTube URLs)
              ↓
    ┏━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  【階段 2】             ┃
    ┃ 提煉生肉 (Extraction)  ┃  ← Claude Code 操控 NotebookLM MCP
    ┃ NotebookLM 匯入分析   ┃
    ┗━━━━━━━━━┬─────────────┛
              │ (Markdown 技術報告)
              ↓
    ┏━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  【階段 3】             ┃
    ┃ 編劇系統 (Screenplay)  ┃  ← Claude Code AI 轉換邏輯
    ┃ 故事框架化             ┃
    ┗━━━━━━━━━┬─────────────┛
              │ (故事大綱 + 場景分解 + 鏡頭計畫表)
              ↓
    ┏━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  【階段 4】             ┃
    ┃ 多語系裂變             ┃  ← Claude Code 調用 LLM API
    ┃ (6 種亞洲語言)        ┃
    ┗━━━━━━━━━┬─────────────┛
              │ (繁中、日、韓、泰、越、印尼腳本)
              ↓
    ┏━━━━━━━━━━━━━━━━━━━━━━┐
    ┃  【階段 5】             │
    ┃ 影視化 (Video Gen)    │  ← Claude Code 協調外部 API
    ┃ • 配音生成             │     (ElevenLabs, PixVerse)
    ┃ • B-roll 生成         │
    ┃ • 自動剪輯             │
    ┗━━━━━━━━━┬─────────────┘
              │ (18 個最終成品影片)
              ↓
    ┌──────────────────────┐
    │  全亞洲短影音發佈    │
    │  (6語言 × 3格式)     │
    │  TikTok/Reels/YT    │
    └──────────────────────┘
              │
              ↓
         💰 變現
```

---

## 📊 具體的時間線與執行流程

### 📅 Day 0 - 初始化設置（一次性）

```
09:00 AM
┌─────────────────────────────────────────┐
│ Step 1: 環境準備                         │
│ Claude Code 執行                        │
└─────────────────────────────────────────┘
  • 建立目錄結構
  • 安裝依賴 (Python libraries)
  • 初始化 Git 倉庫
  • 認證 Google APIs (NotebookLM, YouTube)
  
  命令示例：
  $ claude setup-environment
  $ pip install -r requirements.txt
  $ notebooklm-mcp auth

10:00 AM
┌─────────────────────────────────────────┐
│ Step 2: 配置文件設定                     │
│ 手動編輯 JSON 設定檔                     │
└─────────────────────────────────────────┘
  編輯 config.json:
  {
    "youtube_channels": [
      "Matt Wolfe (AI tutorial)",
      "Two Minute Papers",
      "The AI Advantage"
    ],
    "monitoring_keywords": [
      "AI image generation",
      "GPU rendering",
      "open source models"
    ],
    "target_languages": [
      "zh_TW", "ja_JP", "ko_KR", 
      "th_TH", "vi_VN", "id_ID"
    ],
    "notebooklm_notebook_id": "xxx"
  }

11:00 AM
┌─────────────────────────────────────────┐
│ Step 3: 首次測試                         │
│ Claude Code 執行試運行                  │
└─────────────────────────────────────────┘
  $ python3 08_automation_scripts/radar.py \
    --test --limit 3
  
  輸出：
  ✅ Found 3 test videos
  ✅ Passed to NotebookLM MCP
  ✅ Report generated successfully
```

---

### 🔄 Day 1+ - 每日自動執行流程

```
═══════════════════════════════════════════════════════════════════════

⏰ 00:00 (午夜)
【階段1：全球雷達監聽】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：radar.py                                      │
│ 功能：自動搜尋 YouTube + RSS 監控                  │
└───────────────────────────────────────────────────┘

步驟：
1. 讀取 config.json 中的關鍵字列表
2. 呼叫 YouTube Data API v3
   → 搜尋：「AI image generation 2026」
   → 搜尋：「GPU rendering benchmark」
   → 搜尋：「open source AI models」
3. 呼叫 RSS 訂閱機制，抓取 20+ 科技頻道最新發文
4. 去重複、時間戳、存入隊列

❌ 可能的問題：
   • API 配額已用完 → 重試次日
   • 網路斷線 → 自動重試 3 次

✅ 成功標誌：
   YouTube URLs 清單存入：
   /01_raw_ingest/20260426_youtube_urls.json
   
   檔案內容：
   {
     "timestamp": "2026-04-26T00:15:00Z",
     "videos": [
       {
         "url": "https://youtube.com/watch?v=xxx1",
         "title": "HappyHorse 1.0 Review",
         "channel": "Matt Wolfe",
         "duration": "45:32"
       },
       ...
     ]
   }

═══════════════════════════════════════════════════════════════════════

⏰ 01:30 (凌晨)
【階段2：NotebookLM MCP 自動提煉】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：notebooklm_connector.py                      │
│ 功能：自動匯入 → 交叉比對 → 生成報告              │
└───────────────────────────────────────────────────┘

步驟：
1. 讀取昨天的 YouTube URLs
   ```python
   connector = NotebookLMConnector()
   urls = load_json('01_raw_ingest/youtube_urls.json')
   ```

2. NotebookLM MCP 批量匯入
   ```python
   for url in urls[:5]:  # 只處理前 5 部
       connector.add_youtube_source(url)
   ```
   
   背景發生：
   • NotebookLM 自動下載字幕
   • 如果沒有字幕，Whisper 自動轉譯
   • 內容儲存在 NotebookLM 伺服器

3. 指令 NotebookLM 生成報告
   ```python
   report = connector.generate_report(
       prompt="請綜合這些影片，產出技術情報報告..."
   )
   ```
   
   NotebookLM 內部邏輯：
   • 交叉比對 5 部影片
   • 提取共同技術要點
   • 標註數據來源（100% 可追蹤）
   • 用繁體中文結構化輸出

4. 下載 Markdown 報告到本機
   ```python
   report_path = connector.save_report_locally(report)
   # 輸出：/01_raw_ingest/20260426_123000_synthesis.md
   ```

❌ 可能的問題：
   • 某部影片沒有 CC 字幕 → Whisper 轉譯（準確度 95%）
   • NotebookLM 未能理解專業術語 → 在 Prompt 中添加「術語表」

✅ 生成的報告格式：
   ```markdown
   # AI 技術綜合分析報告
   生成時間：2026-04-26 01:45
   
   ## 核心技術要點
   1. HappyHorse-1.0 新架構
      - 來自：Matt Wolfe 影片
      - 優勢：40% 速度提升
      
   2. RTX 4090 vs H100 對比
      - 來自：Two Minute Papers 影片
      - 推論成本：H100 便宜 30%
   
   ## 硬體需求
   - VRAM: 最少 24GB
   - 推薦: NVIDIA A100 / H100
   
   ...
   ```

═══════════════════════════════════════════════════════════════════════

⏰ 03:00 (淩晨)
【階段3：AI 編劇系統 (故事框架化)】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：screenplay_engine.py                         │
│ 功能：將技術報告轉成「故事」                       │
└───────────────────────────────────────────────────┘

步驟：
1. 讀取 NotebookLM 報告
   ```python
   screenplay = ScreenplayEngine()
   report = load_markdown('01_raw_ingest/xxx_synthesis.md')
   ```

2. AI 分析報告，抽取故事要素
   ```python
   story_framework = screenplay.analyze_content(report)
   ```
   
   Claude Code 透過 Claude API 執行：
   """
   分析這份技術報告，產出一個 3 場景的故事框架：
   
   場景 1（0-15秒）：現狀與問題
   - 用戶目前面臨什麼痛點？
   - 視覺：什麼樣的場景能表達這個痛點？
   
   場景 2（15-45秒）：解決方案
   - 這項技術如何解決問題？
   - 視覺：如何展示技術的威力？
   
   場景 3（45-60秒）：結果與行動
   - 用了這項技術後的結果
   - 呼籲觀眾的下一步行動
   """
   
   AI 輸出：
   {
     "scenes": [
       {
         "scene_no": 1,
         "duration": "0-15s",
         "title": "現在的痛點",
         "problem": "傳統 GPU 渲染太慢",
         "visual_concept": "倒計時時鐘，顯示超長的渲染時間",
         "voiceover": "你是不是總在等待渲染？",
         "emotion": "frustration"
       },
       {
         "scene_no": 2,
         "duration": "15-45s",
         "title": "HappyHorse 解決方案",
         "solution": "新模型架構，速度提升 40%",
         "visual_concept": "進度條快速填滿、時鐘快速轉動",
         "voiceover": "用 HappyHorse-1.0，快速問題解決",
         "emotion": "excitement"
       },
       ...
     ]
   }

3. 生成場景分解與對話
   ```python
   screenplay.generate_scenes(story_framework)
   ```
   
   AI 進一步產生：
   {
     "scenes": [
       {
         "scene_no": 1,
         "dialogue": "你每次渲染都要等 2 小時嗎？",
         "sound_design": "倒計時滴答聲",
         "bgm": "緊張的背景音樂"
       },
       ...
     ]
   }

4. 生成鏡頭計畫表
   ```python
   shot_list = screenplay.generate_shot_list(scenes)
   ```
   
   Claude API 輸出：
   {
     "shots": [
       {
         "shot_no": 1,
         "scene": 1,
         "type": "wide_shot",  // 遠景
         "composition": "主角坐在電腦前，背景是倒計時鐘",
         "camera_movement": "緩慢推進",
         "lighting": "冷色調，營造焦慮感",
         "duration": "3s"
       },
       {
         "shot_no": 2,
         "scene": 1,
         "type": "close_up",  // 特寫
         "composition": "特寫螢幕上的倒計時",
         "camera_movement": "靜止",
         "duration": "2s"
       },
       ...
     ]
   }

5. 生成視覺 Prompt（給 PixVerse/Kling 用）
   ```python
   visual_prompts = screenplay.generate_visual_prompts(shot_list)
   ```
   
   輸出示例：
   ```
   Shot 1: "Wide shot of a frustrated designer sitting at desk, 
   large countdown clock in background showing 120 minutes remaining, 
   cold color grading, dim studio lighting, modern tech setup"
   
   Shot 2: "Close-up of computer monitor displaying render progress bar 
   stuck at 45%, bright red percentage text, digital interface style"
   ```

✅ 保存完整劇本：
   /04_screenplay_system/screenplay_20260426.json
   
   包含：故事大綱、場景、對話、鏡頭、視覺 Prompt

═══════════════════════════════════════════════════════════════════════

⏰ 04:30 (淩晨)
【階段4：多語系腳本裂變】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：localization_engine.py                       │
│ 功能：1 份劇本 → 6 國語言版本                      │
└───────────────────────────────────────────────────┘

步驟：
1. 讀取英文劇本
   ```python
   localizer = LocalizationEngine()
   screenplay = load_json('04_screenplay_system/screenplay_xxx.json')
   ```

2. 針對每種語言，呼叫 Claude API 進行在地化改寫
   ```python
   for language in ["zh_TW", "ja_JP", "ko_KR", "th_TH", "vi_VN", "id_ID"]:
       localized = localizer.localize(screenplay, language)
   ```
   
   【繁體中文版】
   Claude API Prompt:
   """
   根據這份英文科技短影音劇本，改寫成台灣版本。
   
   改寫原則：
   1. 用台灣職場常見的例子替換
   2. 融入「自媒體」或「接案工作室」情境
   3. 保留技術準確性，但用台灣人聽得懂的語氣
   4. 繁體中文，台灣用語
   
   例：英文版「saving render time」
   → 台文改寫「不用再等那麼久的渲染時間」
   
   輸出格式要求：場景對白、BGM、字幕、CTA
   """
   
   AI 輸出：
   {
     "language": "zh_TW",
     "title": "終於解決渲染地獄！HappyHorse-1.0 實測",
     "scenes": [
       {
         "scene": 1,
         "voiceover": "各位接案的夥伴，你們是不是常常在渲染時發呆？",
         "on_screen_text": "等待渲染... 2小時",
         "bgm": "輕快節奏的背景音樂"
       },
       ...
     ]
   }
   
   【日本語版】
   改寫邏輯：日本企業效率化、動漫創作情境
   voiceover: 「アニメ制作の時間短縮に革命をもたらします」
   
   【韓國語版】
   改寫邏輯：K-beauty、遊戲產業
   voiceover: "게임 제작자들 주목, 렌더링 시간을 줄이는 방법"
   
   ... (泰、越、印尼類似邏輯)

3. 保存 6 份在地化劇本
   /05_localization/
   ├── zh_TW.json
   ├── ja_JP.json
   ├── ko_KR.json
   ├── th_TH.json
   ├── vi_VN.json
   └── id_ID.json

═══════════════════════════════════════════════════════════════════════

⏰ 06:00 (早上)
【階段5A：配音生成 + B-roll 視覺資產】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：audio_generator.py + visual_assets.py        │
│ 功能：配音 + 視覺素材的並行生成                    │
└───────────────────────────────────────────────────┘

【配音生成流程】

步驟：
1. 準備配音文本（包含情緒標籤）
   ```python
   audio_gen = AudioGenerator()
   
   for language in target_languages:
       script = load_json(f'05_localization/{language}.json')
       
       # 為每句話加上情緒指令
       enhanced_script = []
       for sentence in script['voiceover']:
           enhanced_script.append({
               "text": sentence,
               "emotion": "excited",  // 或 "calm", "frustrated" 等
               "language": language
           })
   ```

2. 呼叫 ElevenLabs V3 API 生成配音
   ```python
   for sentence in enhanced_script:
       audio_file = audio_gen.generate_voice(
           text=sentence['text'],
           language=sentence['language'],
           emotion_tag=sentence['emotion'],
           voice_id="professional_narrator"  // 預先選定的聲音
       )
       
       save_audio(audio_file, f"06_video_assets/voiceovers/{language}_{idx}.mp3")
   ```
   
   ElevenLabs 背景：
   • 接收文本 + 情緒標籤
   • 生成帶有自然語調變化的音檔
   • 返回 MP3 檔案
   
   成本：6 語言 × 5 句 = 30 句 ≈ USD $0.5

【B-roll 視覺資產生成流程】

步驟：
1. 取出視覺 Prompt（來自編劇系統）
   ```python
   visual_gen = VisualAssetGenerator()
   
   for shot in shot_list:
       prompt = shot['visual_prompt']
       # 例：「Wide shot of frustrated designer at desk...」
   ```

2. 批量提交給 PixVerse/Kling
   ```python
   for shot in shot_list:
       video = visual_gen.generate_video(
           prompt=shot['visual_prompt'],
           duration=shot['duration'],
           model="kling_3.0"  // 或 "cede_c1.5"
       )
       
       save_video(video, f"06_video_assets/b_roll/{shot['id']}.mp4")
   ```
   
   PixVerse 背景：
   • 接收視覺 Prompt
   • 從靜態圖像生成動態影片
   • 支援特定的運鏡指示（推進、拉出、側移）
   
   成本：5 個 shot × USD $0.5 ≈ USD $2.5

3. IP 角色生成（虛擬科技主播）
   ```python
   ip_character = visual_gen.generate_character(
       prompt="Professional tech presenter, Asian appearance, modern attire, confident expression",
       reference_image="brand_character_reference.jpg",
       expression_variation="talking"
   )
   
   save_image(ip_character, "06_video_assets/character_ip/presenter.png")
   ```

✅ 完成後的資產清單：
   /06_video_assets/
   ├── voiceovers/
   │   ├── zh_TW_1.mp3, zh_TW_2.mp3, ...
   │   ├── ja_JP_1.mp3, ja_JP_2.mp3, ...
   │   └── ...
   ├── b_roll/
   │   ├── shot_1.mp4, shot_2.mp4, ...
   ├── character_ip/
   │   ├── presenter_talking_1.png
   │   └── presenter_excited_2.png

═══════════════════════════════════════════════════════════════════════

⏰ 08:00 (上午)
【階段5B：自動剪輯合成】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：video_assembler.py                           │
│ 功能：影片合成、加字幕、調色、配樂混音            │
└───────────────────────────────────────────────────┘

步驟：
1. 準備所有媒體素材
   ```python
   assembler = VideoAssembler()
   
   for language in target_languages:
       assets = {
           'voiceover': f"06_video_assets/voiceovers/{language}_*.mp3",
           'b_roll': [f"06_video_assets/b_roll/shot_{i}.mp4" for i in range(1,6)],
           'character': "06_video_assets/character_ip/presenter.png",
           'subtitles': f"05_localization/{language}_subtitles.vtt"
       }
   ```

2. 使用 MoviePy 自動剪輯
   ```python
   for language in target_languages:
       composition = assembler.create_timeline(
           voiceover=assets['voiceover'],
           b_roll=assets['b_roll'],
           character=assets['character'],
           subtitles=assets['subtitles']
       )
       
       # 自動同步邏輯：
       # • 計算配音時長 = 3秒 + 8秒 + 10秒 = 21秒
       # • 分配 B-roll：21秒 ÷ 5個 shot = 各 4.2秒
       # • 在特定時刻插入角色特寫
   ```

3. 調色（Color Grading）
   ```python
   # 場景 1（痛點）：冷色調，營造焦慮
   composition.apply_color_grading(
       scene=1,
       color_temp="cool",  // 色溫偏藍
       saturation=0.8,
       brightness=-0.1
   )
   
   # 場景 2（解決）：暖色調，營造希望
   composition.apply_color_grading(
       scene=2,
       color_temp="warm",  // 色溫偏橘
       saturation=1.2,
       brightness=0.1
   )
   ```

4. 添加字幕（多語言同步）
   ```python
   composition.add_subtitles(
       file=assets['subtitles'],
       style='modern_sans',
       color='white',
       background='semi_transparent_black',
       timing='auto_sync_with_audio'
   )
   ```

5. 配樂與音效混音
   ```python
   composition.add_bgm(
       scene=1,
       music_style='tense_tech',  // 緊張的科技感音樂
       fade_in=0.5,
       fade_out=1.0
   )
   
   composition.add_bgm(
       scene=2,
       music_style='upbeat_tech',  // 輕快的科技感音樂
       fade_in=1.0,
       fade_out=0.5
   )
   
   composition.add_sound_effect(
       timing=15,  // 15 秒
       sound='notification_ping',
       volume=0.6
   )
   ```

6. 生成多種格式輸出
   ```python
   # 豎屏版（TikTok/Reels/YouTube Shorts）
   composition.export(
       format='vertical_1080',  // 1080x1920
       path=f"07_final_output/tiktok_vertical/{language}_v1.mp4",
       codec='h264',
       bitrate='5000k'
   )
   
   # 橫屏版（YouTube 長影片）
   composition.export(
       format='horizontal_1080',  // 1920x1080
       path=f"07_final_output/youtube_horizontal/{language}_v1.mp4",
       codec='h264',
       bitrate='8000k'
   )
   
   # 4K 版本（高端平台）
   composition.export(
       format='4k',  // 3840x2160
       path=f"07_final_output/4k/{language}_v1.mp4",
       codec='h265',  // 更高效的編碼
       bitrate='20000k'
   )
   ```

✅ 完成時的輸出：
   /07_final_output/
   ├── tiktok_vertical/
   │   ├── zh_TW_v1.mp4
   │   ├── ja_JP_v1.mp4
   │   ├── ... (6 個語言版本)
   ├── youtube_horizontal/
   │   ├── zh_TW_v1.mp4
   │   ├── ... (6 個語言版本)
   └── 4k/
       ├── zh_TW_v1.mp4
       └── ... (6 個語言版本)
   
   總計：6 語言 × 3 格式 = 18 個成品影片 ✅

═══════════════════════════════════════════════════════════════════════

⏰ 10:00 (上午)
【品質檢查 & 人工審核】

┌─ 人工任務（無法完全自動化）──────────────────────┐
│ 5% 的審查工作                                      │
└───────────────────────────────────────────────────┘

檢查清單：
□ 配音發音正確？（無口音？）
□ 字幕有無誤字？
□ 視覺與對白同步？
□ 色調與故事節奏搭配？
□ CTA（行動呼籲）清晰？
□ 品牌 logo/標識出現正確？

通過後，手動「批准發佈」：
$ python3 approve_and_publish.py --language all

═══════════════════════════════════════════════════════════════════════

⏰ 12:00 (中午)
【自動發佈到各平台】

┌─ Claude Code 任務 ─────────────────────────────────┐
│ 執行：auto_publisher.py                            │
│ 功能：同步發佈到 TikTok/Reels/YouTube             │
└───────────────────────────────────────────────────┘

步驟：
1. 為每個平台準備元數據
   ```python
   publisher = AutoPublisher()
   
   for language in target_languages:
       metadata = {
           'title': f"{language} version title",
           'description': "Generated automatically with AI...",
           'hashtags': ['#AI', '#TechTutorial', f'#{language_name}'],
           'thumbnail': "auto_generated_from_key_frame.jpg"
       }
   ```

2. TikTok 發佈
   ```python
   for language in target_languages:
       response = publisher.publish_tiktok(
           video_path=f"07_final_output/tiktok_vertical/{language}_v1.mp4",
           metadata=metadata,
           schedule_time="12:30 UTC"  // 針對各地區最佳發佈時間
       )
       
       print(f"✅ TikTok {language}: {response['video_id']}")
   ```

3. Instagram Reels 發佈
   ```python
   # 使用相同的豎屏版本
   publisher.publish_instagram_reels(...)
   ```

4. YouTube Shorts 發佈
   ```python
   publisher.publish_youtube_shorts(...)
   ```

5. YouTube 完整版本（橫屏）
   ```python
   publisher.publish_youtube_full(
       video_path=f"07_final_output/youtube_horizontal/{language}_v1.mp4",
       playlist="AI Tutorial 2026"
   )
   ```

✅ 完成標誌：
   所有 18 個影片已同步發佈到 6 個平台
   預期觀看量：
   • TikTok: 50萬+ 次觀看/天
   • Instagram: 20萬+ 次觀看/天
   • YouTube: 10萬+ 次觀看/天
   
   總計：80萬+ 次觀看/天 × 6 語言 = 480萬+ 次觀看/天 🎉

═══════════════════════════════════════════════════════════════════════
```

---

## 🔄 Claude Code 在各階段的具體角色

| 階段 | 功能 | Claude Code 做什麼 | 外部工具 |
|------|------|------------------|--------|
| 1 | 雷達 | 排程執行 + 結果整理 | YouTube API, RSS |
| 2 | 提煉 | 操控 MCP、管理流程 | NotebookLM |
| 3 | 編劇 | AI 轉換邏輯、生成框架 | Claude API |
| 4 | 多語系 | LLM 在地化改寫 | Claude API |
| 5A | 配音+視覺 | API 協調、資產管理 | ElevenLabs, PixVerse |
| 5B | 剪輯 | MoviePy 自動化 | Local Python |
| 6 | 發佈 | 多平台協調 | TikTok, Instagram, YouTube API |

---

## 💡 Claude Code 的核心協調能力

Claude Code 不是在做「單一任務」，而是在協調一個複雜的**任務編排系統**：

```
Claude Code 的大腦

1. 時間排程器
   • 決定「什麼時候」執行哪個階段
   • 確保上一個階段的輸出是下一個階段的輸入

2. 資料流管理器
   • 讀取 JSON/Markdown 配置
   • 管理各階段的輸入/輸出檔案
   • 錯誤偵測與重試機制

3. API 協調者
   • 呼叫 YouTube API、NotebookLM MCP、Claude API
   • 管理 API 額度與成本
   • 自動降級（如果某 API 失敗，使用替代方案）

4. 異常處理
   • 網路中斷 → 自動重試
   • API 額度用完 → 等待重置或告警
   • 品質檢查失敗 → 要求人工審核

5. 日誌與監控
   • 記錄每一步的成功/失敗
   • 實時通知進度（email / Slack）
   • 定期生成效能報告
```

---

## 📈 完整工作流的效益

| 指標 | 傳統方式 | Claude Code 方式 |
|------|--------|-----------------|
| 時間 | 1 個人 1 天製作 1 支影片 | 系統 12 小時製作 6 語言 × 3 格式 |
| 人力 | 需要編劇 + 剪輯師 + 字幕師 + 發佈專員 | 1 個人 + Claude Code |
| 成本 | 月 $2000+ | 月 $200 |
| 產能 | 月 20 支影片 | 月 600 支影片 |
| 規模 | 單語言 | 6 語言同步 |

---

## 🚀 你需要做什麼？

```
Day 0：
✓ 設置環境 + 認證 APIs
✓ 編輯 config.json（監控的頻道 & 關鍵字）

Day 1+：
✓ 每天檢查 1 份品質檢查清單（5 分鐘）
✓ 批准發佈（1 分鐘）

System 自動完成：
✓ 所有 5 個階段的執行
✓ 18 個成品的生成
✓ 多平台發佈

你的工作：從「製作者」變成「監督者」
```

