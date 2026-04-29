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

  constructor(serverUrl: string = 'ws://localhost:3000') {
    this.deviceId = uuidv4();
    this.serverUrl = serverUrl;
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
          const wsUrl = `${this.serverUrl}?deviceId=${this.deviceId}&type=mobile`;
          this.ws = new WebSocket(wsUrl);

          const timeout = setTimeout(() => {
            this.ws?.terminate();
          }, 10000);

          this.ws.on('open', () => {
            clearTimeout(timeout);
            console.log('✓ Mobile connected to Dispatch server');
            this.reconnectAttempts = 0;
            this.isConnecting = false;
            resolve();
          });

          this.ws.on('message', (data) => {
            try {
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
    const { type, from, content } = message;

    if (type === 'connected') {
      console.log('Message:', content);
    } else if (type === 'command') {
      console.log(`Received response from ${from}:`, content);
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
