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
  isAlive: boolean;
  heartbeatInterval?: NodeJS.Timeout;
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

const HEARTBEAT_INTERVAL = 30000; // 30 seconds
const HEARTBEAT_TIMEOUT = 60000; // 60 seconds

function startHeartbeat(deviceId: string) {
  const device = devices.get(deviceId);
  if (!device) return;

  device.heartbeatInterval = setInterval(() => {
    if (device.ws && device.ws.readyState === WebSocket.OPEN) {
      if (!device.isAlive) {
        device.ws.terminate();
        return;
      }
      device.isAlive = false;
      device.ws.ping();
    }
  }, HEARTBEAT_INTERVAL);
}

function stopHeartbeat(deviceId: string) {
  const device = devices.get(deviceId);
  if (device?.heartbeatInterval) {
    clearInterval(device.heartbeatInterval);
    device.heartbeatInterval = undefined;
  }
}

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

  let device = devices.get(deviceId);
  if (!device) {
    device = {
      id: deviceId,
      type,
      name: `${type}-${deviceId.slice(0, 8)}`,
      lastSeen: Date.now(),
      isAlive: true
    };
    devices.set(deviceId, device);
  } else {
    device.isAlive = true;
  }

  device.ws = ws;
  device.lastSeen = Date.now();
  startHeartbeat(deviceId);

  console.log(`${type} device connected: ${deviceId}`);

  ws.on('pong', () => {
    device!.isAlive = true;
    device!.lastSeen = Date.now();
  });

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      const { type: msgType, sessionId, content } = message;

      device!.lastSeen = Date.now();

      if (msgType === 'command' && sessionId) {
        const session = sessions.get(sessionId);
        if (session) {
          const targetId = type === 'mobile' ? session.desktopId : session.mobileId;
          const target = targetId ? devices.get(targetId) : null;

          if (target?.ws && target.ws.readyState === WebSocket.OPEN) {
            target.ws.send(JSON.stringify({
              type: 'command',
              from: deviceId,
              content,
              timestamp: Date.now()
            }));
          } else if (target) {
            ws.send(JSON.stringify({
              type: 'error',
              message: 'Target device is not connected'
            }));
          }
        }
      }
    } catch (e) {
      console.error('Error processing message:', e);
    }
  });

  ws.on('error', (error) => {
    console.error(`WebSocket error for ${deviceId}:`, error);
  });

  ws.on('close', () => {
    stopHeartbeat(deviceId);
    if (device) {
      device.ws = undefined;
      device.isAlive = false;
      console.log(`Device disconnected: ${deviceId}`);
    }
  });

  ws.send(JSON.stringify({
    type: 'connected',
    deviceId,
    timestamp: Date.now(),
    message: 'Successfully connected to Dispatch server'
  }));
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Dispatch server running on port ${PORT}`);
});
