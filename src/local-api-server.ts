import express from 'express';
import { spawn } from 'child_process';
import path from 'path';
import {
  createConversation,
  loadConversation,
  saveConversation,
  addMessage,
  getAllConversations,
  loadSystemState,
  updateDeviceState,
  updateSessionState,
  recordVideoMetadata
} from './local-data-manager';

const app = express();
app.use(express.json());

// 提供靜態 HTML UI
app.use(express.static(path.join(__dirname, '../public')));

interface CLIMessage {
  role: 'user' | 'assistant';
  content: string;
}

async function invokeLocalCLI(conversationHistory: CLIMessage[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const claude = spawn('/opt/node22/bin/claude', []);
    let output = '';
    let errorOutput = '';

    claude.stdout.on('data', (data) => {
      output += data.toString();
    });

    claude.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    claude.on('close', (code) => {
      if (code === 0) {
        resolve(output.trim());
      } else {
        reject(new Error(`CLI exited with code ${code}: ${errorOutput}`));
      }
    });

    // 發送對話歷史給 CLI
    const prompt = conversationHistory
      .map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`)
      .join('\n\n');

    claude.stdin.write(prompt);
    claude.stdin.end();

    // 設置超時
    setTimeout(() => {
      claude.kill();
      reject(new Error('CLI execution timeout'));
    }, 30000);
  });
}

// 建立新對話
app.post('/api/conversations', (req, res) => {
  const { title } = req.body;
  const conversation = createConversation(title || 'New Conversation');
  res.json(conversation);
});

// 獲取所有對話
app.get('/api/conversations', (req, res) => {
  const conversations = getAllConversations();
  res.json(conversations);
});

// 獲取特定對話
app.get('/api/conversations/:id', (req, res) => {
  const conversation = loadConversation(req.params.id);
  if (!conversation) {
    return res.status(404).json({ error: 'Conversation not found' });
  }
  res.json(conversation);
});

// 發送訊息到對話
app.post('/api/conversations/:id/messages', async (req, res) => {
  const { content } = req.body;
  const conversation = loadConversation(req.params.id);

  if (!conversation) {
    return res.status(404).json({ error: 'Conversation not found' });
  }

  // 添加用戶訊息
  addMessage(req.params.id, 'user', content);

  try {
    // 準備對話歷史
    const history: CLIMessage[] = conversation.messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
    history.push({ role: 'user', content });

    // 調用本地 CLI
    const response = await invokeLocalCLI(history);

    // 添加助手回應
    addMessage(req.params.id, 'assistant', response);

    const updatedConversation = loadConversation(req.params.id);
    res.json(updatedConversation);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

// 獲取系統狀態
app.get('/api/system-state', (req, res) => {
  const state = loadSystemState();
  res.json(state);
});

// 更新設備狀態
app.patch('/api/system-state/devices/:deviceId', (req, res) => {
  const { deviceId } = req.params;
  updateDeviceState(deviceId, req.body);
  res.json({ success: true });
});

// 更新會話狀態
app.patch('/api/system-state/sessions/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  updateSessionState(sessionId, req.body);
  res.json({ success: true });
});

// 記錄視頻元數據
app.post('/api/system-state/videos', (req, res) => {
  const { videoId, ...metadata } = req.body;
  recordVideoMetadata(videoId, metadata);
  res.json({ success: true });
});

const PORT = parseInt(process.env.LOCAL_API_PORT || '3001', 10);
app.listen(PORT, '127.0.0.1', () => {
  console.log(`本地 API 服務器運行在 http://127.0.0.1:${PORT}`);
  console.log('所有資料存儲在: /home/user/claude-code/local-data/');
});
