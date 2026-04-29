import { WebSocket } from 'ws';
import { v4 as uuidv4 } from 'uuid';
import fetch from 'node-fetch';

class MobileDispatchClient {
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

  async register(name: string = 'iPhone') {
    try {
      const response = await fetch(`${this.serverUrl.replace('ws', 'http')}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'mobile', name })
      });

      const data = await response.json() as { deviceId: string };
      this.deviceId = data.deviceId;
      console.log('Mobile registered:', data);
      return this.deviceId;
    } catch (error) {
      console.error('Failed to register mobile:', error);
      throw error;
    }
  }

  async pairWithDesktop(sessionId: string, pairingCode: string) {
    try {
      const response = await fetch(`${this.serverUrl.replace('ws', 'http')}/api/sessions/pair`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          pairingCode,
          mobileId: this.deviceId
        })
      });

      if (!response.ok) {
        throw new Error('Pairing failed');
      }

      this.sessionId = sessionId;
      const data = await response.json();
      console.log('Pairing successful:', data);
      return data;
    } catch (error) {
      console.error('Failed to pair:', error);
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
            console.log('✓ Mobile connected to Dispatch server');
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
            console.log('✗ Mobile disconnected from Dispatch server');
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
      console.log('📱 Connected to Dispatch server:', content);
    } else if (type === 'command') {
      const deviceLabel = fromDeviceType === 'desktop' ? '🖥️ Desktop' : '📱 Mobile';
      console.log(`${deviceLabel} (${fromName}) sent:`, content, `[${new Date(timestamp as number).toLocaleTimeString()}]`);
    } else if (type === 'error') {
      console.error('⚠️ Error:', message);
    }
  }

  sendCommand(content: Record<string, unknown>) {
    if (!this.sessionId) {
      console.error('No active session');
      return;
    }

    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'command',
        sessionId: this.sessionId,
        content
      }));
    }
  }
}

export default MobileDispatchClient;
