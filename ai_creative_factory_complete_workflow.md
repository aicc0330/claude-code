# 全球 AI 創意內容工廠：完整工作流設計
## 整合編劇系統 + 短影音製造 + 跨國變現

---

## 📋 核心架構概覽

```
歐美 AI 情報源
    ↓
[階段1] 全球雷達 (YT Search + RSS 監控)
    ↓
[階段2] NotebookLM MCP 提煉 (免費無幻覺總結)
    ↓
[階段3] AI 編劇系統 (故事框架化)
    ├─ 故事大綱生成
    ├─ 場景分解 & 對話編寫
    ├─ 鏡頭計畫表
    └─ 視覺提示詞輸出
    ↓
[階段4] 多語系裂變 (全亞洲語言)
    ├─ 繁體中文腳本
    ├─ 日文腳本
    ├─ 韓文腳本
    ├─ 泰文腳本
    ├─ 越南文腳本
    └─ 印尼文腳本
    ↓
[階段5] 影視化生成
    ├─ B-roll AI 影片生成 (PixVerse/Kling)
    ├─ 多語系配音 (ElevenLabs V3)
    ├─ 虛擬 IP 主播生成
    └─ 自動剪輯合成
    ↓
全亞洲短影音發佈 (TikTok/Reels/YouTube Shorts)
    ↓
💰 多國變現與流量變現
```

---

## 🎬 五層完整工作流

### 層級一：全球資訊監聽 (Global Radar)
**目標**：自動捕獲歐美最新 AI 科技情報

**執行步驟**：
- 設定監聽關鍵字：AI 影像生成、開源模型、GPU 硬體、影視技術
- YT Search Skill 每日搜尋前 3-5 部最新英文影片
- RSS 訂閱機制監控 20+ 科技頻道
- 自動構建待處理隊列

**輸出**：YouTube URL 清單 + 影片元數據

---

### 層級二：生肉提煉與總結 (Content Extraction & Summarization)
**目標**：從原始素材提取核心技術知識點，且完全免費

**執行步驟**：
1. NotebookLM MCP 自動將 YouTube URL 匯入筆記本
2. NotebookLM 交叉比對 5 部影片內容
3. 自動生成結構化報告（包含技術要點、硬體需求、操作步驟）
4. 報告自動下載回本機 `01_raw_ingest/` 目錄

**成本**：0（完全免費）
**品質**：無幻覺（仅基於源資料）

**輸出**：Markdown 技術報告

---

### 層級三：AI 編劇與故事框架化 (Screenplay System)
**目標**：將生硬的技術報告轉化為「有靈魂的故事」

#### 步驟 3.1：故事概念轉換
- **輸入**：技術報告（如「HappyHorse-1.0 新功能」）
- **轉換邏輯**：
  - 痛點提取：用戶現在的問題是什麼？
  - 情感連結：故事的情緒弧線是什麼？
  - 解決方案：如何用這項技術解決？
- **輸出**：故事大綱（3 場景結構）

#### 步驟 3.2：場景分解 & 角色對話
- 場景一：現狀/問題 (0-15秒)
- 場景二：技術介紹 (15-45秒)
- 場景三：結果/CTA (45-60秒)
- 自動生成主播台詞與旁白

#### 步驟 3.3：鏡頭計畫表
- 景別設定（遠景、中景、特寫）
- 運鏡方向（推進、拉出、側移）
- 光線與氛圍描述
- 視覺轉場方式

#### 步驟 3.4：視覺提示詞生成 (Prompt Engineering)
- B-roll 場景描述（給 PixVerse/Kling 用）
- 角色表情與肢體語言
- 產品展示方式

**輸出**：完整劇本 + 鏡頭計畫表 + 視覺 Prompt 清單

---

### 層級四：多語系腳本裂變 (Multilingual Localization)
**目標**：一份故事，六國語言版本

**語言清單**：
1. 繁體中文（台灣市場）
2. 日本語（日本市場）
3. 韓國語（韓國市場）
4. ไทย（泰國市場）
5. Tiếng Việt（越南市場）
6. Bahasa Indonesia（印尼市場）

**在地化邏輯**（不只翻譯，而是改寫）：
- 繁中版：台灣職場/自媒體情境
- 日文版：日本企業效率化、動漫創作情境
- 韓文版：K-beauty、遊戲產業情境
- 泰文版：泰國電商、短影音文化
- 越南文版：越南新創、年輕族群情境
- 印尼文版：印尼數位經濟、社群平台文化

**輸出**：6 份在地化腳本（每份含台詞 + 視覺指示）

---

### 層級五：影視化生成與自動剪輯 (Video Generation & Assembly)
**目標**：從腳本到成片，完全自動化

#### 5.1：AI 視覺資產生成
- **B-roll 生成**：用視覺 Prompt 丟進 PixVerse/Kling，批次生成科技感空景
- **IP 角色生成**：使用固定的「虛擬科技主播」Prompt 確保品牌一致性
- **產品展示**：上傳真實產品圖作為參考，確保生成準確

#### 5.2：多語系配音生成
- 呼叫 ElevenLabs V3 API
- 每個台詞自動加入情緒標籤：[excited]、[explanatory]、[urgent]
- 同步生成繁中、日、韓、泰、越、印尼六國語言音檔

#### 5.3：自動剪輯與合成
- **工具**：Python moviepy 庫
- **邏輯**：
  - 圖像序列 + 音檔 自動對軌
  - 自動計算切換點（根據台詞節奏）
  - 自動加入字幕（多語言同步）
  - 調色邏輯（冷色→暖色，對應故事節奏）
  - 配樂與音效自動混音

#### 5.4：多平台格式輸出
- 1080p 豎屏版（TikTok/Reels/YouTube Shorts）
- 1080p 橫屏版（YouTube 長影片）
- 4K 版本（高端平台）

**輸出**：6 個語言版本 × 3 種格式 = 18 個成品影片

---

## 💾 Ubuntu 本機目錄結構

```
~/ai_creative_factory/
├── 01_radar/                 # 情報監聽
│   ├── youtube_channels.json
│   ├── rss_feeds.txt
│   └── daily_captures.log
│
├── 02_raw_ingest/           # 原始資料暫存
│   ├── notebooklm_reports/
│   │   └── 20260426_ai_image_gen_summary.md
│   └── transcripts/
│
├── 03_knowledge_base/       # 持續生長的記憶
│   ├── concepts/
│   │   ├── HappyHorse_1.0.md
│   │   ├── GPU_算力趨勢.md
│   │   └── 影視逆向工程.md
│   └── viral_hooks.md        # 爆款開場白資料庫
│
├── 04_screenplay_system/    # 編劇系統核心
│   ├── story_framework/
│   │   ├── outline.json
│   │   └── scenes.json
│   ├── characters.json
│   ├── screenplay.md
│   └── shot_list.md
│
├── 05_localization/         # 多語系腳本
│   ├── zh_TW.md            # 繁中
│   ├── ja_JP.md            # 日文
│   ├── ko_KR.md            # 韓文
│   ├── th_TH.md            # 泰文
│   ├── vi_VN.md            # 越文
│   └── id_ID.md            # 印尼文
│
├── 06_video_assets/        # 影視資產
│   ├── b_roll_prompts/
│   ├── generated_videos/
│   ├── character_ip/
│   └── voiceovers/
│       ├── zh_TW_audio.mp3
│       ├── ja_JP_audio.mp3
│       └── ...
│
├── 07_final_output/        # 成品
│   ├── tiktok_vertical/
│   │   ├── zh_TW_v1.mp4
│   │   ├── ja_JP_v1.mp4
│   │   └── ...
│   ├── youtube_shorts/
│   └── instagram_reels/
│
└── 08_automation_scripts/  # Python 自動化腳本
    ├── radar.py
    ├── notebooklm_connector.py
    ├── screenplay_engine.py
    ├── localization_engine.py
    ├── video_generator.py
    ├── scheduler.py
    └── requirements.txt
```

---

## 🔄 完整執行時間線

| 時間 | 任務 | 自動化程度 |
|------|------|---------|
| 00:00 | 每日 YT 監聽 + 捕獲 5 部影片 | 100% 自動 |
| 02:00 | NotebookLM MCP 提煉生肉 | 100% 自動 |
| 04:00 | AI 編劇系統產出劇本 | 100% 自動 |
| 06:00 | 多語系腳本裂變 | 100% 自動 |
| 08:00 | 配音 + B-roll 生成 | 100% 自動 |
| 10:00 | 剪輯合成 + 品質檢查 | 95% 自動（留 5% 人工檢視） |
| 12:00 | 18 個語言版本成品就緒 | ✅ 完成 |

---

## 🎯 關鍵績效指標 (KPIs)

- **產能**：每天 6 語言 × 1 影片 = 6 個頻道同時發佈
- **成本**：月度 API 成本 < USD $200（ElevenLabs + PixVerse）
- **時效**：歐美發佈新影片 → 亞洲多國發佈 ≤ 12 小時
- **品質**：零幻覺（NotebookLM 數據來源把控）+ 高視覺張力（影視級生成）
- **變現**：預期 6 個月內月均流量 500萬+ 次觀看

---

## ⚠️ 避坑指南

1. **防止資訊污染**：在 NotebookLM 層級設定「僅採信有官方文件支持的內容」過濾
2. **品牌一致性**：虛擬主播 IP 和視覺風格必須完全鎖定，不允許隨機變化
3. **成本控制**：定期監控 API 呼叫量，設定每月預算上限
4. **法律合規**：確保所有轉譯內容都有正確的來源標註（尊重原創作者）

