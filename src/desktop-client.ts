import { WebSocket } from 'ws';
import { v4 as uuidv4 } from 'uuid';
import fetch from 'node-fetch';

class DesktopDispatchClient {
  private deviceId: string;
  private serverUrl: string;
  private ws?: WebSocket;
  private sessionId?: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectDelay = 3000;
  private isConnecting = false;
  private lastMessageTime = 0;
  private messageCheckInterval?: NodeJS.Timeout;

  constructor(serverUrl: string = 'ws://localhost:3000') {
    this.deviceId = uuidv4();
    this.serverUrl = serverUrl;
    this.lastMessageTime = Date.now();
  }

  async register(name: string = 'Claude Code Desktop') {
    try {
      const response = await fetch(`${this.serverUrl.replace('ws', 'http')}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'desktop', name })
      });

      const data = await response.json() as { deviceId: string };
      this.deviceId = data.deviceId;
      console.log('Desktop registered:', data);
      return this.deviceId;
    } catch (error) {
      console.error('Failed to register desktop:', error);
      throw error;
    }
  }

  async createSession() {
    try {
      const response = await fetch(`${this.serverUrl.replace('ws', 'http')}/api/sessions/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ desktopId: this.deviceId })
      });

      const data = await response.json() as { sessionId: string; pairingCode: string };
      this.sessionId = data.sessionId;
      console.log('Session created with pairing code:', data.pairingCode);
      return data;
    } catch (error) {
      console.error('Failed to create session:', error);
      throw error;
    }
  }

  async connect(): Promise<void> {
    if (this.isConnecting) return;
    this.isConnecting = true;

    return new Promise<void>((resolve, reject) => {
      const attemptConnection = () => {
        try {
          const wsUrl = `${this.serverUrl}?deviceId=${this.deviceId}`;
          this.ws = new WebSocket(wsUrl);

          const timeout = setTimeout(() => {
            this.ws?.terminate();
            reject(new Error('Connection timeout'));
          }, 10000);

          this.ws.on('open', () => {
            clearTimeout(timeout);
            console.log('✓ Desktop connected to Dispatch server');
            this.reconnectAttempts = 0;
            this.isConnecting = false;
            this.lastMessageTime = Date.now();
            this.startConnectionMonitor();
            resolve();
          });

          this.ws.on('message', (data) => {
            try {
              this.lastMessageTime = Date.now();
              const message = JSON.parse(data.toString());
              this.handleMessage(message);
            } catch (e) {
              console.error('Error parsing message:', e);
            }
          });

          this.ws.on('error', (error) => {
            clearTimeout(timeout);
            console.error('WebSocket error:', error);
          });

          this.ws.on('close', () => {
            clearTimeout(timeout);
            console.log('✗ Desktop disconnected from Dispatch server');
            this.isConnecting = false;
            this.stopConnectionMonitor();
            this.attemptReconnect();
          });
        } catch (error) {
          this.isConnecting = false;
          reject(error);
        }
      };

      attemptConnection();
    });
  }

  private startConnectionMonitor() {
    this.stopConnectionMonitor();
    this.messageCheckInterval = setInterval(() => {
      const timeSinceLastMessage = Date.now() - this.lastMessageTime;
      if (timeSinceLastMessage > 120000) {
        console.warn('No messages received for 2 minutes, reconnecting...');
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.close();
        }
      }
    }, 30000);
  }

  private stopConnectionMonitor() {
    if (this.messageCheckInterval) {
      clearInterval(this.messageCheckInterval);
      this.messageCheckInterval = undefined;
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);
    console.log(`Reconnecting in ${Math.round(delay / 1000)}s (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    setTimeout(() => {
      this.connect().catch(console.error);
    }, delay);
  }

  private handleMessage(message: Record<string, unknown>) {
    const { type, from, fromDeviceType, fromName, content, timestamp } = message;

    if (type === 'connected') {
      console.log('🖥️ Connected to Dispatch server:', content);
    } else if (type === 'command') {
      const deviceLabel = fromDeviceType === 'mobile' ? '📱 Mobile' : '🖥️ Desktop';
      console.log(`${deviceLabel} (${fromName}) sent:`, content, `[${new Date(timestamp as number).toLocaleTimeString()}]`);
      this.executeCommand(content as Record<string, unknown>);
    } else if (type === 'error') {
      console.error('⚠️ Error:', message);
    }
  }

  private executeCommand(command: Record<string, unknown>) {
    const { action, args } = command;
    console.log(`Executing action: ${action}`, args);
  }

  send(message: Record<string, unknown>) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
}

export default DesktopDispatchClient;
