# NotebookLM 與本機系統的完整整合指南
## 雲端智能過濾器 ↔ 本地知識大腦

---

## 核心問題

**為什麼需要整合？**

NotebookLM 是雲端工具（強大但封閉），本機系統是本地工具（靈活但需自動化）。
兩者結合才能達到：
- ✅ 高質量的內容篩選（NotebookLM）
- ✅ 持續生長的知識記憶（本機大腦）
- ✅ 完全自動化的流程（Claude Code）

---

## 第一層：NotebookLM 的角色定位

### 1.1 NotebookLM 是「前置過濾器」

```
目的：對原始 YouTube 內容進行智能篩選和初步分析

功能：
✓ 批量匯入播放清單（50 部影片一次）
✓ 自動下載字幕（支援多語言）
✓ 交叉比對多部影片的見解
✓ 評估來源可靠性
✓ 生成高質量的綜合報告

限制：
✗ 每個筆記本只能 50 個來源
✗ 沒有開放 API（需透過 MCP 繞過）
✗ 無法直接連接本機系統
✗ 知識會被新上傳的內容覆蓋

因此：不是存儲系統，而是「分析系統」
```

### 1.2 NotebookLM 的筆記本結構（具體配置）

#### 筆記本 1：AI 影像生成與開源模型
```
筆記本名稱：AI_IMAGE_GENERATION_v2026
目標來源數：40-45 個（保留 5-10 的空間用於新增）

預設系統角色設定：
"""
你是一位專業的 AI 視覺技術研究員。

核心職責：
1. 分析上傳的 YouTube 教學與評測影片
2. 提取技術規格、最佳實踐、市場趨勢
3. 進行影片間的交叉比對
4. 評估來源可靠性

數據標準：
- 優先採信有基準測試 (benchmark) 支持的內容
- 標記『官方文件支持』vs『第三方推測』
- 標註所有數據的來源影片與發佈日期

輸出格式：
- 用繁體中文
- 結構化 Markdown
- 每項信息後面都要有『來自：XX 影片』的標註
"""

主要監控的頻道：
- Matt Wolfe (The AI Advantage)
- Two Minute Papers
- Fireworks.ai
- OpenAI 官方頻道
- 本地 YouTuber（如台灣科技新鮮事）

定期維護：
- 每月第一週：移除超過 90 天的舊影片（騰出空間）
- 每週末：新增該週最值得的 3-5 部影片
- 每月末：生成綜合月報
```

#### 筆記本 2：硬體算力與 GPU 評測
```
筆記本名稱：HARDWARE_GPU_ANALYSIS_v2026
系統角色設定：企業級算力採購顧問

主要內容：
- GPU 性能基準測試
- 市場報價與成本分析
- 企業採購建議
- 硬體冷卻與電力成本

目標輸出：
- 成本效益對比表格
- 購買建議清單
- ROI 計算示意
```

#### 筆記本 3：影視製作與 AI
```
筆記本名稱：VIDEO_PRODUCTION_AI_v2026
系統角色設定：電影製片技術顧問

主要內容：
- AI 輔助拍攝與後製
- 特效與動畫製作
- 音聲設計與配音
- 色彩分級與視覺效果

目標輸出：
- 製作流程指南
- 軟硬體採購清單
- 成本預算表
```

---

## 第二層：資訊在兩個系統間的流轉

### 2.1 完整的資訊流程圖

```
【YouTube - 歐美科技頻道】
    ↓
【IFTTT 自動監控】
    • 當 Matt Wolfe 發布新影片
    • 當標題包含「AI」或「model」
    • 自動記錄到 Google Sheets
    ↓
【Google Sheets - 待審清單】
    ┌─ 自動更新，但需人工檢查
    │  • 標題是否相關？
    │  • 是否已經有類似內容？
    │  • 優先度是多少？
    ↓
【人工篩選】（週末進行，5-10 分鐘）
    ┌─ 從清單中挑選 5-10 部最有價值的影片
    │  複製 URL → 貼入 NotebookLM
    ↓
【YouTube to NotebookLM 擴充功能】
    ┌─ 使用者点击：將 URL 匯入指定筆記本
    │  系統自動：
    │  • 下載影片英文字幕
    │  • 如無字幕，用 Whisper 轉譯
    │  • 儲存在 NotebookLM 雲端
    │  • 生成初步摘要
    ↓
【NotebookLM 內的自動分析】（等待 24 小時）
    ┌─ 系統自動：
    │  • 與同筆記本內的其他影片交叉比對
    │  • 評估可靠性（官方 vs 第三方）
    │  • 提取核心要點
    ↓
【NotebookLM 報告生成】
    ┌─ 使用者提問：
    │  「請綜合這些影片，產出技術情報摘要」
    │  系統輸出：高質量的 Markdown 報告
    │  （包含：核心技術、市場趨勢、硬體需求）
    ↓
【人工複製】（5 分鐘）
    ┌─ 在 NotebookLM 中複製完整的 Markdown 報告
    │  • 全選所有內容
    │  • 複製到剪貼板
    ↓
【貼入本機系統】
    ┌─ 貼入 ~/ai_content_hub/01_raw_ingest/notebooklm_exports/
    │  檔名格式：YYYYMMDD_main_topic.md
    │  例如：20260427_ai_image_gen.md
    ↓
【Claude Code 觸發 - 滾動式記憶更新】
    ┌─ 自動執行 brain_router.py
    │  • 讀取 Markdown 報告
    │  • 分類知識點
    │  • 融合進 02_knowledge_base 中的對應主題
    │  • 保持源追蹤（標註來自哪份報告）
    │  • 更新 index.md
    │  • Git 自動 commit
    ↓
【本地知識庫持續成長】
    ┌─ ~/studio_ai_brain/02_Concepts/
    │  例：AI_IMAGE_GENERATION.md
    │  內容變得越來越厚實
    │  • 第一週：5 個知識點
    │  • 第二週：8 個知識點（新增 + 融合）
    │  • 第三週：12 個知識點
    │  • ...持續成長
    ↓
【Claude Code 進行多語系裂變】
    ┌─ 自動執行 localization_engine.py
    │  • 讀取本地知識庫
    │  • 轉換成故事框架
    │  • 產出 6 語言版本的短影音腳本
    │  • 附加視覺 Prompt 與情緒標籤
    ↓
【生成配音 + B-roll + 自動剪輯】
    ┌─ 自動執行
    │  • ElevenLabs 配音
    │  • PixVerse 視覺資產
    │  • MoviePy 自動剪輯
    ↓
【18 個成品影片】
    ┌─ 6 語言 × 3 格式（竪屏、橫屏、4K）
    ↓
【多平台同步發佈】
    ┌─ TikTok / Instagram Reels / YouTube Shorts
    ↓
【💰 變現】
```

---

## 第三層：實現整合的具體步驟

### 3.1 NotebookLM 端的操作

#### Step 1：建立分類筆記本

在 [notebooklm.google.com](https://notebooklm.google.com) 上：

```
1. 點擊「Create notebook」
2. 命名：「AI_IMAGE_GENERATION_v2026」
3. 點擊齒輪圖示 → 「Customize」
4. 設定「System role」：[見上面筆記本配置]
5. 保存

重複此流程建立其他主題的筆記本
```

#### Step 2：安裝「YouTube to NotebookLM」擴充功能

```
1. 前往 Chrome Web Store
2. 搜尋「YouTube to NotebookLM」
3. 點擊「Add to Chrome」安裝
4. 在 YouTube 影片頁面，右上角會出現擴充功能圖示
5. 點擊 → 選擇目標 NotebookLM 筆記本 → 匯入
```

#### Step 3：設定 IFTTT 自動監控

在 [ifttt.com](https://ifttt.com) 上建立規則：

```
IFTTT 規則 1：
IF: YouTube
  Trigger: New video from channel「Matt Wolfe」
THEN: Google Sheets
  Action: Add row to spreadsheet「YouTube_monitoring」
  
Row format:
  Column 1: {{PostedAt}} (日期)
  Column 2: {{Title}} (影片標題)
  Column 3: {{Url}} (影片連結)
  Column 4: {{ChannelTitle}} (頻道名)
  Column 5: [空白，用於人工標記相關性]

IFTTT 規則 2-N：
重複為其他關鍵 YouTuber（Two Minute Papers, OpenAI, ...）
```

#### Step 4：每週末人工篩選與匯入

```
時間：週日上午 10:00
流程：
1. 打開 Google Sheets（IFTTT 自動更新的清單）
2. 掃過標題，挑選 5-10 部最有價值的
3. 對於每部影片：
   a. 複製 URL
   b. 打開 YouTube 網頁
   c. 點擊擴充功能圖示
   d. 選擇「AI_IMAGE_GENERATION_v2026」筆記本
   e. 匯入

時間成本：約 5-10 分鐘（操作很簡單）
```

#### Step 5：在 NotebookLM 中生成報告

```
在 NotebookLM 筆記本的對話框中提問：

「請分析最近新增的 5 部影片。
綜合它們的內容，生成一份技術情報報告，包含：

### 1. 核心技術突破
- 列出 3-5 項最重要的新技術
- 每項標註『來自哪部影片』
- 標記『官方確認』或『評測發現』

### 2. 硬體需求 & 成本
- GPU 型號與規格
- 市場報價
- 預估成本

### 3. 實際操作步驟
- 如果有教程，列出步驟
- 工具清單
- 常見問題

### 4. 市場趨勢 & 預期
- 這項技術對亞洲市場的意義
- 預期採用時間表

---
請用繁體中文，結構化 Markdown 格式輸出。」

NotebookLM 會在 1-2 分鐘內生成報告。
```

---

### 3.2 本機端的自動化操作

#### Claude Code 的「橋樑」腳本

```python
# bridge_notebooklm_to_local.py
# 目的：將 NotebookLM 報告自動複製進本機系統

import os
import json
from datetime import datetime

def monitor_clipboard():
    """監控剪貼板是否有新的 Markdown 內容"""
    
    # 使用者手動複製 NotebookLM 報告後
    # 執行此腳本：python bridge_notebooklm_to_local.py
    
    # 讀取剪貼板
    clipboard_content = get_clipboard_content()
    
    # 判斷是否為 NotebookLM 報告（檢查特徵）
    if is_notebooklm_report(clipboard_content):
        # 提取主題（從報告的 H1 標題）
        topic = extract_topic(clipboard_content)
        
        # 儲存到 01_raw_ingest
        filename = f"{datetime.now().strftime('%Y%m%d')}_{topic.lower()}.md"
        filepath = f"01_raw_ingest/notebooklm_exports/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clipboard_content)
        
        print(f"✅ 報告已保存：{filepath}")
        
        # 自動觸發下一步
        trigger_brain_update(filepath)
```

#### 完整的自動化流程腳本

```python
# daily_automation.py
# 目的：每天自動執行完整的流程

import schedule
import time
from datetime import datetime

def schedule_daily_tasks():
    """設定每日自動化任務"""
    
    # 00:00 - YouTube 監聽
    schedule.every().day.at("00:00").do(run_radar)
    
    # 01:30 - NotebookLM MCP 匯入（人工輸入後）
    # 需要人工複製 NotebookLM 報告
    schedule.every().day.at("02:00").do(check_raw_ingest)
    
    # 03:00 - 觸發滾動式記憶更新
    schedule.every().day.at("03:00").do(run_brain_router)
    
    # 04:00 - 編劇系統 + 多語系裂變
    schedule.every().day.at("04:00").do(run_screenplay_and_localization)
    
    # 06:00 - 配音 + B-roll 生成
    schedule.every().day.at("06:00").do(run_audio_and_video_gen)
    
    # 08:00 - 自動剪輯與發佈
    schedule.every().day.at("08:00").do(run_video_assembly_and_publish)
    
    # 持續執行
    while True:
        schedule.run_pending()
        time.sleep(60)

def check_raw_ingest():
    """檢查 01_raw_ingest 是否有新的 NotebookLM 報告"""
    
    ingest_path = "01_raw_ingest/notebooklm_exports/"
    processed_log = "01_raw_ingest/processed_flag/processed.log"
    
    # 讀取已處理的報告清單
    processed = load_processed_list(processed_log)
    
    # 掃描新的報告檔案
    for filename in os.listdir(ingest_path):
        if filename.endswith('.md') and filename not in processed:
            print(f"🆕 發現新的 NotebookLM 報告：{filename}")
            
            # 標記為已處理
            mark_as_processed(filename, processed_log)
```

---

## 第四層：核心整合邏輯

### 4.1 「滾動式記憶更新」的詳細實現

```python
# brain_router.py - 最核心的整合邏輯

def rolling_memory_update(notebooklm_report_path):
    """
    讀取 NotebookLM 報告，將知識融合進本地大腦
    
    邏輯：不是「覆蓋」，而是「融合」與「補充」
    """
    
    # 讀取 NotebookLM 報告
    report = load_markdown(notebooklm_report_path)
    
    # 解析報告中的各個知識點
    knowledge_sections = parse_report(report)
    
    # 對於每個知識點
    for section_title, section_content in knowledge_sections.items():
        
        # 判斷本地大腦中是否已存在相關主題
        concept_file = find_matching_concept(section_title)
        
        if concept_file:
            # 【情況 1】主題已存在
            print(f"📖 主題已存在：{concept_file}")
            
            existing_content = load_markdown(concept_file)
            
            # 判斷新信息是「重複」、「補充」還是「矛盾」
            relationship = analyze_relationship(existing_content, section_content)
            
            if relationship == "duplicate":
                # 如果是重複，只更新時間戳，不寫入新內容
                print(f"   → 重複內容，略過")
                
            elif relationship == "supplement":
                # 如果是補充，附加到檔案末尾
                print(f"   → 補充內容，融合進檔案")
                
                new_entry = f"""
## 更新 [{datetime.now().strftime('%Y-%m-%d')}]
來自報告：{get_report_name(notebooklm_report_path)}

{section_content}
"""
                append_to_file(concept_file, new_entry)
                
            elif relationship == "contradiction":
                # 如果有矛盾，標記為需要人工審查
                print(f"   ⚠️ 檢測到矛盾內容，標記為 [REVIEW_NEEDED]")
                
                mark_for_review(concept_file, "contradiction")
        else:
            # 【情況 2】新主題，建立新檔案
            print(f"✨ 新主題：{section_title}")
            
            new_concept = f"""# {section_title}

## 首次提及日期
{datetime.now().strftime('%Y-%m-%d')}

## 來源
{get_report_name(notebooklm_report_path)}

## 核心內容
{section_content}

## 相關主題
[待補充]

## 時間線
- {datetime.now().strftime('%Y-%m-%d')}: 首次提及
"""
            save_new_concept(concept_file, new_concept)
    
    # 更新 index.md
    update_knowledge_index()
    
    # Git 自動 commit
    git_commit(f"知識庫更新：融合 {get_report_name(notebooklm_report_path)}")
```

### 4.2 源追蹤的實現

```python
# 每項知識點都要包含「來自何處」的追蹤信息

def add_source_tracking(content, source_info):
    """為內容附加源追蹤"""
    
    tracked_content = f"""{content}

---
### 源追蹤
- **首次提及**：{source_info['first_date']}
- **來自報告**：{source_info['report_name']}
- **影片來源**：{source_info['youtube_videos']}  
  • {source_info['videos'][0]['title']} (Matt Wolfe, {source_info['videos'][0]['date']})
  • {source_info['videos'][1]['title']} (Two Minute Papers, {source_info['videos'][1]['date']})
- **官方確認**：[是/否]
- **最後更新**：{source_info['last_update']}
"""
    
    return tracked_content
```

---

## 第五層：人工操作的「間隙點」

### 5.1 需要人工介入的地方

```
✓ 自動化：YouTube 監控 (IFTTT)
✗ 人工：週末篩選與匯入（5-10 分鐘）
✓ 自動化：NotebookLM 分析與報告生成
✗ 人工：複製報告到本機（1 分鐘）
✓ 自動化：本地大腦更新 + 多語系裂變
✓ 自動化：配音 + 視覺化 + 發佈

總人工成本：約 10-15 分鐘/周
```

### 5.2 簡化人工操作的方法

```python
# 方法 1：監控剪貼板自動保存
# 使用者複製 NotebookLM 報告 → 執行腳本 → 自動貼入本機

# 方法 2：Chrome 擴充功能直接存儲
# 在 NotebookLM 中加入按鈕 → 直接發送報告到本機

# 方法 3：API 整合（未來）
# 一旦 Google 開放 NotebookLM API，這一步將完全自動化
```

---

## 六、 整合的優勢總結

| 層面 | 單獨使用 NotebookLM | 單獨使用本機系統 | 整合使用 |
|------|-----------------|-----------------|---------|
| **內容質量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **記憶延續性** | ❌ (被新內容覆蓋) | ✅ | ✅ |
| **自動化程度** | 低 | 高 | 極高 |
| **成本** | 低 | 低 | 低 |
| **靈活性** | 低 | 高 | 極高 |
| **規模擴展** | 困難 (50 源上限) | 容易 | 容易 |

**結論**：整合使用是最優選擇，結合兩個系統的優勢。

---

## 七、 故障排除

### 7.1 NotebookLM 報告未生成

```
症狀：超過 24 小時還沒有報告
原因：
  • 字幕品質太差，NotebookLM 無法理解
  • 內容太雜亂，系統無法提煉

解決：
  1. 檢查字幕是否正確（YouTube CC 字幕品質）
  2. 重新提問，提示更明確
  3. 如果還是失敗，手動刪除該來源，選擇其他影片
```

### 7.2 本地大腦更新失敗

```
症狀：brain_router.py 執行出錯
原因：
  • NotebookLM 報告格式異常
  • Markdown 解析出錯
  • Git 提交失敗

解決：
  1. 檢查報告檔案的格式
  2. 查看 logs/errors.log
  3. 手動修正格式或重新複製報告
  4. 重新執行 brain_router.py
```

### 7.3 多語系腳本品質下降

```
症狀：某個語言版本的腳本明顯生硬
原因：
  • 本地知識點不足
  • Claude API 上下文不夠清晰
  • 該語言的文化背景設定不足

解決：
  1. 為該語言的提示詞添加更多文化背景
  2. 增加該主題的知識點數量
  3. 人工檢查並修正腳本
  4. 建立該語言的「常用表達」字典
```

---

## 八、 未來的完全自動化（API 開放後）

```
目前：
YouTube → IFTTT → Google Sheets → 人工篩選 → YouTube to NotebookLM

未來（假設 Google 開放 API）：
YouTube → IFTTT → Google Sheets → 自動篩選（Claude） → NotebookLM API → 自動下載報告 → 本機大腦

完成度：100% 自動化
人工成本：0 分鐘/週
```

