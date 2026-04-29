import fs from 'fs';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

const DATA_DIR = '/home/user/claude-code/local-data';
const CONVERSATIONS_DIR = path.join(DATA_DIR, 'conversations');
const STATE_DIR = path.join(DATA_DIR, 'system-state');

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

interface ConversationRecord {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
  isActive: boolean;
}

interface SystemState {
  devices: Record<string, any>;
  sessions: Record<string, any>;
  videoMetadata: Record<string, any>;
  lastUpdated: number;
}

function ensureDirs() {
  [CONVERSATIONS_DIR, STATE_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

export function createConversation(title: string): ConversationRecord {
  ensureDirs();
  const id = uuidv4();
  const now = Date.now();
  const conversation: ConversationRecord = {
    id,
    title,
    messages: [],
    createdAt: now,
    updatedAt: now,
    isActive: true
  };

  saveConversation(conversation);
  return conversation;
}

export function saveConversation(conversation: ConversationRecord) {
  ensureDirs();
  const filePath = path.join(CONVERSATIONS_DIR, `${conversation.id}.json`);
  conversation.updatedAt = Date.now();
  fs.writeFileSync(filePath, JSON.stringify(conversation, null, 2));
}

export function loadConversation(conversationId: string): ConversationRecord | null {
  const filePath = path.join(CONVERSATIONS_DIR, `${conversationId}.json`);
  if (fs.existsSync(filePath)) {
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data) as ConversationRecord;
  }
  return null;
}

export function addMessage(conversationId: string, role: 'user' | 'assistant', content: string): Message {
  const conversation = loadConversation(conversationId);
  if (!conversation) {
    throw new Error(`Conversation ${conversationId} not found`);
  }

  const message: Message = {
    id: uuidv4(),
    role,
    content,
    timestamp: Date.now()
  };

  conversation.messages.push(message);
  saveConversation(conversation);
  return message;
}

export function getAllConversations(): ConversationRecord[] {
  ensureDirs();
  const files = fs.readdirSync(CONVERSATIONS_DIR).filter(f => f.endsWith('.json'));
  return files
    .map(f => {
      const data = fs.readFileSync(path.join(CONVERSATIONS_DIR, f), 'utf-8');
      return JSON.parse(data) as ConversationRecord;
    })
    .sort((a, b) => b.updatedAt - a.updatedAt);
}

export function saveSystemState(state: SystemState) {
  ensureDirs();
  const filePath = path.join(STATE_DIR, 'system.json');
  fs.writeFileSync(filePath, JSON.stringify(state, null, 2));
}

export function loadSystemState(): SystemState {
  ensureDirs();
  const filePath = path.join(STATE_DIR, 'system.json');
  if (fs.existsSync(filePath)) {
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data) as SystemState;
  }
  return {
    devices: {},
    sessions: {},
    videoMetadata: {},
    lastUpdated: Date.now()
  };
}

export function updateDeviceState(deviceId: string, deviceData: any) {
  const state = loadSystemState();
  state.devices[deviceId] = {
    ...state.devices[deviceId],
    ...deviceData,
    lastUpdated: Date.now()
  };
  state.lastUpdated = Date.now();
  saveSystemState(state);
}

export function updateSessionState(sessionId: string, sessionData: any) {
  const state = loadSystemState();
  state.sessions[sessionId] = {
    ...state.sessions[sessionId],
    ...sessionData,
    lastUpdated: Date.now()
  };
  state.lastUpdated = Date.now();
  saveSystemState(state);
}

export function recordVideoMetadata(videoId: string, metadata: any) {
  const state = loadSystemState();
  state.videoMetadata[videoId] = {
    ...metadata,
    recordedAt: Date.now()
  };
  state.lastUpdated = Date.now();
  saveSystemState(state);
}
