import express from 'express';
import { WebSocketServer, WebSocket } from 'ws';
import { createServer } from 'http';
import { v4 as uuidv4 } from 'uuid';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

interface Device {
  id: string;
  type: 'desktop' | 'mobile';
  name: string;
  lastSeen: number;
  ws?: WebSocket;
}

interface Session {
  id: string;
  desktopId: string;
  mobileId?: string;
  pairingCode: string;
  createdAt: number;
  isActive: boolean;
}

const devices = new Map<string, Device>();
const sessions = new Map<string, Session>();

app.use(express.json());

app.post('/api/register', (req, res) => {
  const { type, name } = req.body;
  const deviceId = uuidv4();

  devices.set(deviceId, {
    id: deviceId,
    type,
    name,
    lastSeen: Date.now()
  });

  res.json({ deviceId, message: `Device ${name} registered as ${type}` });
});

app.post('/api/sessions/create', (req, res) => {
  const { desktopId } = req.body;
  const sessionId = uuidv4();
  const pairingCode = Math.random().toString(36).substring(2, 8).toUpperCase();

  sessions.set(sessionId, {
    id: sessionId,
    desktopId,
    pairingCode,
    createdAt: Date.now(),
    isActive: true
  });

  res.json({ sessionId, pairingCode });
});

app.post('/api/sessions/pair', (req, res) => {
  const { sessionId, pairingCode, mobileId } = req.body;
  const session = sessions.get(sessionId);

  if (!session || session.pairingCode !== pairingCode) {
    return res.status(400).json({ error: 'Invalid pairing code' });
  }

  session.mobileId = mobileId;
  const desktop = devices.get(session.desktopId);
  const mobile = devices.get(mobileId);

  res.json({
    message: 'Pairing successful',
    desktop: desktop?.name,
    mobile: mobile?.name
  });
});

wss.on('connection', (ws, req) => {
  const url = new URL(req.url || '', `http://${req.headers.host}`);
  const deviceId = url.searchParams.get('deviceId');
  const type = url.searchParams.get('type') as 'desktop' | 'mobile';

  if (!deviceId) {
    ws.close(1000, 'Missing deviceId');
    return;
  }

  const device = devices.get(deviceId);
  if (device) {
    device.ws = ws;
    device.lastSeen = Date.now();
  }

  console.log(`${type} device connected: ${deviceId}`);

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      const { type: msgType, sessionId, content } = message;

      if (msgType === 'command' && sessionId) {
        const session = sessions.get(sessionId);
        if (session) {
          const targetId = type === 'mobile' ? session.desktopId : session.mobileId;
          const target = targetId ? devices.get(targetId) : null;

          if (target?.ws && target.ws.readyState === WebSocket.OPEN) {
            target.ws.send(JSON.stringify({
              type: 'command',
              from: deviceId,
              content
            }));
          }
        }
      }
    } catch (e) {
      console.error('Error processing message:', e);
    }
  });

  ws.on('close', () => {
    if (device) {
      device.ws = undefined;
      console.log(`Device disconnected: ${deviceId}`);
    }
  });

  ws.send(JSON.stringify({
    type: 'connected',
    deviceId,
    message: 'Successfully connected to Dispatch server'
  }));
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Dispatch server running on port ${PORT}`);
});
