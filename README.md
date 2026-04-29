# Claude Dispatch - Cross-Device Session Control

Enable real-time communication and command execution between your iPhone and Claude Code desktop application.

## Features

- **Device Registration**: Register desktop and mobile devices with unique IDs
- **Session Management**: Create secure pairing sessions with verification codes
- **WebSocket Communication**: Real-time bidirectional messaging between devices
- **Automatic Command Routing**: Messages are automatically routed to the correct device

## Installation

```bash
npm install
```

## Setup

### 1. Start the Dispatch Server

```bash
npm run dev
```

The server will start on `http://localhost:3000`

### 2. Desktop Client Integration

```typescript
import DesktopDispatchClient from './src/desktop-client';

const desktop = new DesktopDispatchClient('ws://localhost:3000');
await desktop.register('My Computer');
await desktop.connect();

const session = await desktop.createSession();
console.log('Pairing Code:', session.pairingCode);
```

### 3. Mobile Client Integration

On your iPhone (via the Claude Code app or web interface):

```typescript
import MobileDispatchClient from './src/mobile-client';

const mobile = new MobileDispatchClient('ws://localhost:3000');
await mobile.register('iPhone');
await mobile.connect();
await mobile.pairWithDesktop(sessionId, pairingCode);
```

## Usage Example

```bash
npm run dev  # Terminal 1: Start server
npm run build
node dist/example.js  # Terminal 2: Run demo
```

## How It Works

1. **Desktop Registers**: Creates a session with a pairing code
2. **Mobile Connects**: Enters the pairing code to join the session
3. **Bidirectional Communication**: Commands flow between devices via WebSocket
4. **Automatic Routing**: Messages are routed based on device type and session

## Architecture

- **Server**: Express + WebSocket for message relay
- **Desktop Client**: Connects as 'desktop' type device
- **Mobile Client**: Connects as 'mobile' type device
- **Session**: Links desktop and mobile for secure communication

## Connection Stability Features

✓ **Heartbeat Monitoring**: Server sends periodic ping/pong to detect dead connections
✓ **Automatic Reconnection**: Exponential backoff reconnection strategy (3s, 4.5s, 6.75s...)
✓ **Connection State Tracking**: Monitors last seen time and connection status
✓ **Error Recovery**: Graceful handling of network failures and timeouts
✓ **Message Timestamps**: Includes timestamps for message ordering
✓ **Connection Status Feedback**: Device status visible through heartbeat mechanism

## How to Ensure Continuous Connection

1. **Server-side Monitoring**: Server sends ping every 30 seconds, terminates stale connections after 60 seconds
2. **Client-side Recovery**: Automatic reconnection with exponential backoff (max 10 attempts)
3. **Network Resilience**: Both desktop and mobile support graceful disconnection/reconnection
4. **Real-time Status**: Connection status is continuously monitored and reported