import DesktopDispatchClient from './desktop-client';
import MobileDispatchClient from './mobile-client';

async function main() {
  const serverUrl = 'ws://localhost:3000';

  console.log('=== Dispatch Example Demo ===\n');

  // Step 1: Initialize desktop client
  console.log('Step 1: Initializing desktop client...');
  const desktop = new DesktopDispatchClient(serverUrl);
  await desktop.register('My MacBook');
  await desktop.connect();

  // Step 2: Create a session
  console.log('\nStep 2: Creating session...');
  const session = await desktop.createSession();
  console.log(`Pairing Code: ${session.pairingCode}`);

  // Wait a moment for setup
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Step 3: Initialize mobile client
  console.log('\nStep 3: Initializing mobile client (iPhone)...');
  const mobile = new MobileDispatchClient(serverUrl);
  await mobile.register('iPhone 15');
  await mobile.connect();

  // Step 4: Pair mobile with desktop
  console.log('\nStep 4: Pairing mobile with desktop...');
  await mobile.pairWithDesktop(session.sessionId, session.pairingCode);

  // Wait for connection to establish
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Step 5: Send command from mobile to desktop
  console.log('\nStep 5: Sending command from mobile to desktop...');
  mobile.sendCommand({
    action: 'executeCode',
    args: { code: 'console.log("Hello from iPhone!")' }
  });

  // Keep connection alive for demo
  await new Promise(resolve => setTimeout(resolve, 2000));
  console.log('\n=== Demo Complete ===');
}

main().catch(console.error);
