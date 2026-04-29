import fs from 'fs';
import path from 'path';

interface SessionMemory {
  sessionId: string;
  desktopId: string;
  mobileId?: string;
  pairingCode: string;
  createdAt: number;
  lastActivity: number;
  isActive: boolean;
  messageQueue: Array<{
    from: string;
    content: unknown;
    timestamp: number;
  }>;
}

const MEMORY_DIR = '/home/user/claude-code/logs/sessions';

function ensureMemoryDir() {
  if (!fs.existsSync(MEMORY_DIR)) {
    fs.mkdirSync(MEMORY_DIR, { recursive: true });
  }
}

export function saveMemory(session: SessionMemory) {
  ensureMemoryDir();
  const filePath = path.join(MEMORY_DIR, `${session.sessionId}.json`);
  fs.writeFileSync(filePath, JSON.stringify(session, null, 2));
}

export function loadMemory(sessionId: string): SessionMemory | null {
  const filePath = path.join(MEMORY_DIR, `${sessionId}.json`);
  if (fs.existsSync(filePath)) {
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data) as SessionMemory;
  }
  return null;
}

export function getAllMemories(): SessionMemory[] {
  ensureMemoryDir();
  const files = fs.readdirSync(MEMORY_DIR).filter(f => f.endsWith('.json'));
  return files.map(f => {
    const data = fs.readFileSync(path.join(MEMORY_DIR, f), 'utf-8');
    return JSON.parse(data) as SessionMemory;
  });
}

export function deleteMemory(sessionId: string) {
  const filePath = path.join(MEMORY_DIR, `${sessionId}.json`);
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
}

export function queueMessage(sessionId: string, message: { from: string; content: unknown; timestamp: number }) {
  const session = loadMemory(sessionId);
  if (session) {
    session.messageQueue.push(message);
    session.lastActivity = Date.now();
    saveMemory(session);
  }
}

export function flushQueue(sessionId: string): Array<{ from: string; content: unknown; timestamp: number }> {
  const session = loadMemory(sessionId);
  if (session) {
    const queue = session.messageQueue;
    session.messageQueue = [];
    saveMemory(session);
    return queue;
  }
  return [];
}
