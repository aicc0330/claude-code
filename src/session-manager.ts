import fs from 'fs';
import path from 'path';

interface SessionState {
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

const SESSION_DIR = '/home/user/claude-code/logs/sessions';

function ensureSessionDir() {
  if (!fs.existsSync(SESSION_DIR)) {
    fs.mkdirSync(SESSION_DIR, { recursive: true });
  }
}

export function saveSession(session: SessionState) {
  ensureSessionDir();
  const filePath = path.join(SESSION_DIR, `${session.sessionId}.json`);
  fs.writeFileSync(filePath, JSON.stringify(session, null, 2));
}

export function loadSession(sessionId: string): SessionState | null {
  const filePath = path.join(SESSION_DIR, `${sessionId}.json`);
  if (fs.existsSync(filePath)) {
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data) as SessionState;
  }
  return null;
}

export function getAllSessions(): SessionState[] {
  ensureSessionDir();
  const files = fs.readdirSync(SESSION_DIR).filter(f => f.endsWith('.json'));
  return files.map(f => {
    const data = fs.readFileSync(path.join(SESSION_DIR, f), 'utf-8');
    return JSON.parse(data) as SessionState;
  });
}

export function deleteSession(sessionId: string) {
  const filePath = path.join(SESSION_DIR, `${sessionId}.json`);
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
}

export function queueMessage(sessionId: string, message: { from: string; content: unknown; timestamp: number }) {
  const session = loadSession(sessionId);
  if (session) {
    session.messageQueue.push(message);
    session.lastActivity = Date.now();
    saveSession(session);
  }
}

export function flushQueue(sessionId: string): Array<{ from: string; content: unknown; timestamp: number }> {
  const session = loadSession(sessionId);
  if (session) {
    const queue = session.messageQueue;
    session.messageQueue = [];
    saveSession(session);
    return queue;
  }
  return [];
}
