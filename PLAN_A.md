# 計畫 A：本地對話系統架構

## 概述

計畫 A 是一個完全本地化的對話系統，消除了對遠端 API 的依賴。所有對話歷史、系統狀態和會話資料都存儲在本地檔案系統中，通過本地 CLI 進行處理。

## 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                     Web 瀏覽器介面                             │
│                 (localhost:3001)                            │
│           ✓ 對話管理 ✓ 訊息發送 ✓ 會話控制                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP REST API
                       ↓
┌──────────────────────────────────────────────────────────────┐
│                 本地 API 伺服器                                │
│              (local-api-server.ts)                           │
│  - 對話管理    - 訊息路由    - 狀態同步                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   ┌────────┐   ┌─────────┐   ┌──────────┐
   │ 本地   │   │ 系統    │   │ 對話     │
   │ CLI    │   │ 狀態    │   │ 歷史     │
   │ 調用   │   │ 儲存    │   │ 儲存     │
   └────────┘   └─────────┘   └──────────┘
        │              │              │
        └──────────────┼──────────────┘
                       ↓
        /home/user/claude-code/local-data/
        ├── conversations/     (對話歷史)
        ├── system-state/      (系統狀態)
        └── cache/             (暫存資料)
```

## 核心元件

### 1. local-data-manager.ts
**功能**：本地資料持久化層
```typescript
// 對話管理
createConversation(title)      // 建立新對話
loadConversation(id)           // 讀取對話
saveConversation(conversation) // 保存對話
addMessage(id, role, content)  // 新增訊息

// 系統狀態
loadSystemState()              // 讀取系統狀態
saveSystemState(state)         // 保存系統狀態
updateDeviceState(deviceId)    // 更新設備狀態
updateSessionState(sessionId)  // 更新會話狀態
recordVideoMetadata(videoId)   // 記錄視頻元數據
```

### 2. local-api-server.ts
**功能**：REST API 伺服器，處理所有網頁請求
```
GET  /api/conversations              - 獲取所有對話列表
POST /api/conversations              - 建立新對話
GET  /api/conversations/:id          - 獲取特定對話
POST /api/conversations/:id/messages - 發送訊息

GET  /api/system-state               - 獲取系統狀態
PATCH /api/system-state/devices/:id  - 更新設備狀態
PATCH /api/system-state/sessions/:id - 更新會話狀態
POST /api/system-state/videos        - 記錄視頻元數據
```

### 3. Web 用戶介面
**功能**：現代化的對話介面，無需終端
- 對話列表管理
- 即時訊息發送和接收
- 自動滾動和加載狀態指示
- 完全本地運行，無需遠端資源

## 資料流程

### 發送訊息流程

1. **用戶輸入** → Web 介面
2. **API 請求** → REST API 到 local-api-server
3. **訊息儲存** → 本地 JSON 檔案
4. **CLI 調用** → 呼叫本地 `/opt/node22/bin/claude`
5. **回應生成** → CLI 處理訊息
6. **回應儲存** → 本地 JSON 檔案
7. **UI 更新** → Web 介面顯示回應

### 資料儲存結構

```
local-data/
├── conversations/
│   ├── uuid1.json           # 對話 1
│   ├── uuid2.json           # 對話 2
│   └── uuid3.json           # ...
├── system-state/
│   └── system.json          # 全域系統狀態
└── cache/
    └── [暫存檔案]
```

#### 對話檔案格式
```json
{
  "id": "uuid-string",
  "title": "對話標題",
  "messages": [
    {
      "id": "msg-uuid",
      "role": "user",
      "content": "用戶訊息",
      "timestamp": 1234567890
    },
    {
      "id": "msg-uuid",
      "role": "assistant",
      "content": "AI 回應",
      "timestamp": 1234567891
    }
  ],
  "createdAt": 1234567890,
  "updatedAt": 1234567891,
  "isActive": true
}
```

## 使用方法

### 啟動計畫 A

```bash
# 方法 1：使用啟動指令稿
bash /home/user/claude-code/start-plan-a.sh

# 方法 2：手動啟動
cd /home/user/claude-code
npm run build
npm run local-api

# 方法 3：使用 ts-node（開發模式）
cd /home/user/claude-code
npx ts-node src/local-api-server.ts
```

### 訪問介面

打開網頁瀏覽器，訪問：
```
http://localhost:3001
```

### 停止系統

按 `Ctrl+C` 停止 API 伺服器

## 優勢

✓ **無 API 依賴**：完全本地運行，無需遠端伺服器
✓ **隱私保護**：所有資料存儲在本地，不上傳任何資訊
✓ **離線操作**：無網際網路也能使用
✓ **持久儲存**：對話歷史永久保存在本地
✓ **快速響應**：無網路延遲
✓ **完全控制**：可完全自訂和擴展
✓ **與 Dispatch 整合**：可與設備同步系統整合

## 技術棧

| 組件 | 技術 |
|------|------|
| 後端 | Node.js + Express + TypeScript |
| 前端 | Vanilla JavaScript + HTML/CSS |
| 儲存 | 本地檔案系統 (JSON) |
| CLI  | Claude Code CLI (/opt/node22/bin/claude) |

## 檔案清單

```
/home/user/claude-code/
├── local-data-manager.ts        # 核心資料管理層
├── src/
│   └── local-api-server.ts      # REST API 伺服器
├── public/
│   └── index.html               # Web 用戶介面
├── start-plan-a.sh              # 啟動指令稿
├── local-data/
│   ├── conversations/           # 對話歷史
│   ├── system-state/            # 系統狀態
│   └── cache/                   # 暫存資料
└── PLAN_A.md                    # 本文件
```

## 未來擴展

1. **進階搜尋**：搜尋過去的對話內容
2. **匯出功能**：匯出對話為 PDF/Markdown
3. **多使用者**：支援多個使用者帳戶
4. **設定同步**：與 Dispatch 系統同步設定
5. **自動備份**：自動備份到本地儲存裝置
6. **版本控制**：追蹤對話的版本歷史

## 故障排除

### API 伺服器無法啟動
- 檢查埠 3001 是否被佔用：`lsof -i :3001`
- 檢查 Node.js 是否已安裝：`node --version`
- 檢查 TypeScript 依賴：`npm install`

### 無法連線到 CLI
- 確認 claude CLI 可用：`which claude`
- 檢查檔案權限：`ls -la /opt/node22/bin/claude`

### 資料無法保存
- 檢查目錄權限：`ls -la /home/user/claude-code/local-data/`
- 確保目錄可寫：`touch /home/user/claude-code/local-data/test.txt`

## 安全考量

- 所有資料存儲在本地，無需考慮遠端伺服器安全
- 建議定期備份 `/home/user/claude-code/local-data/` 目錄
- 對話歷史以明文形式存儲，請保護好磁碟存取權限

---

**計畫 A 完全就緒。所有資訊已存儲在 CLI 本地。**
