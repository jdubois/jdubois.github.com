import { chromium } from 'playwright';
import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile, unlink } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const output = path.join(root, 'workshops/copilot-app/assets');
const base = process.env.WORKSHOP_URL || 'http://127.0.0.1:18765';
if (new URL(base).hostname !== '127.0.0.1') throw new Error('Capture only the loopback training app');
const stage = process.env.WORKSHOP_STAGE || 'start';
if (!['start', 'after-bugfix', 'after-feature', 'after-performance'].includes(stage)) throw new Error('Unknown fixture stage');
const references = JSON.parse(await readFile(path.join(output, 'references.json'), 'utf8'));
const reference = references.checkpoints[stage];
const viewport = { width: 1600, height: 1000 };
const channel = process.env.CAPTURE_CHANNEL || 'chromium';
const playwright = JSON.parse(await readFile(new URL('./node_modules/playwright/package.json', import.meta.url), 'utf8'));
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const javaRuntime = JSON.parse(process.env.WORKSHOP_JAVA_RUNTIME || 'null');
if (!javaRuntime || !['version', 'vendor', 'vm'].every(field =>
  typeof javaRuntime[field] === 'string' && javaRuntime[field].trim())) {
  throw new Error('Use capture-all.py to supply actual capture JVM metadata');
}
await mkdir(output, { recursive: true });

async function jsonRequest(method, route) {
  const response = await fetch(`${base}${route}`, { method });
  if (!response.ok) throw new Error(`${method} ${route}: HTTP ${response.status}`);
  return response.json();
}

async function mcp(name, args) {
  const response = await fetch(`${base}/bootui/api/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json, text/event-stream' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name, arguments: args } })
  });
  if (!response.ok) throw new Error(`MCP transport HTTP ${response.status}`);
  const raw = await response.text();
  const envelope = JSON.parse(raw);
  if (envelope.error || envelope.result?.isError) throw new Error(JSON.stringify(envelope));
  const data = envelope.result.structuredContent ||
    JSON.parse(envelope.result.content.find(item => item.type === 'text').text);
  return { tool: name, arguments: args, originalResponseBytes: Buffer.byteLength(raw), data };
}

const identity = await jsonRequest('GET', '/api/workshop');
if (identity.application !== 'shopping-cart' || identity.revision !== reference.commit) {
  throw new Error(`Wrong process/revision: ${JSON.stringify(identity)}`);
}
const browser = await chromium.launch({ channel });
try {
  const page = await browser.newPage({ viewport, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  await page.goto(base);
  await page.waitForFunction(() => document.querySelector('#status').textContent.startsWith('Ready.'));
  async function clickAndWait(button) {
    const response = page.waitForResponse(r => r.url() === `${base}/api/cart` && r.request().method() === 'GET');
    await button.click();
    await response;
    await page.waitForFunction(() =>
      document.querySelector('#status').textContent.startsWith('Server cart:') &&
      [...document.querySelectorAll('button')].every(button => !button.disabled));
  }
  await clickAndWait(page.getByRole('button', { name: 'Add Notebook to cart', exact: true }));
  await clickAndWait(page.getByRole('button', { name: 'Add Notebook to cart', exact: true }));
  const quantity = Number(await page.locator('#cart-count').textContent());
  if (quantity !== (stage === 'start' ? 1 : 2)) throw new Error(`Wrong repeated-add behavior: ${quantity}`);
  if (stage === 'after-feature') {
    await clickAndWait(page.getByRole('button', { name: 'Add Coffee mug to cart', exact: true }));
    await clickAndWait(page.getByRole('button', { name: 'Remove Notebook', exact: true }));
    if (await page.locator('#cart-count').textContent() !== '1' ||
        !await page.locator('#cart-lines').textContent().then(text => text.includes('Coffee mug') && !text.includes('Notebook'))) {
      throw new Error('Removal did not preserve the other item');
    }
  } else if (stage === 'after-performance') {
    await clickAndWait(page.getByRole('button', { name: 'Load sample cart', exact: true }));
  }
  const image = {
    start: 'cart-bug.png', 'after-bugfix': 'cart-fixed.png',
    'after-feature': 'cart-feature.png', 'after-performance': 'cart-performance.png'
  }[stage];
  await page.screenshot({ path: path.join(output, image) });

  await jsonRequest('POST', '/api/workshop/reset?items=8');
  const cart = await jsonRequest('GET', '/api/cart');
  const distinctProducts = new Set(cart.items.map(item => item.productId)).size;
  const totalCents = cart.items.reduce((total, item) => total + item.lineTotalCents, 0);
  if (cart.items.length !== 8 || distinctProducts !== 8 || cart.itemCount !== 8 ||
      cart.totalCents !== totalCents || totalCents !== 11500 ||
      cart.items.some(item => item.quantity !== 1 || item.lineTotalCents !== item.priceCents)) {
    throw new Error('Wrong query workload, quantities or total');
  }
  const activity = await mcp('get_live_activity', { query: '/api/cart', limit: 8 });
  const entry = activity.data.entries.find(item =>
    item.type === 'REQUEST' && item.method === 'GET' && item.path === '/api/cart');
  if (!entry) throw new Error('No matching cart GET request');
  const profile = await mcp('get_request_profile', { id: entry.id });
  const journal = profile.data.journal;
  const sqlEvents = journal.timeline.filter(item => item.source === 'sql');
  const expectedSql = stage === 'after-performance' ? 1 : 9;
  if (journal.requestId !== entry.id || journal.status !== 200 || sqlEvents.length !== expectedSql) {
    throw new Error(`Mismatched profile/query count: expected ${expectedSql}, got ${sqlEvents.length}`);
  }
  const currentIdentity = await jsonRequest('GET', '/api/workshop');
  if (JSON.stringify(identity) !== JSON.stringify(currentIdentity)) throw new Error('Runtime changed during capture');

  const evidencePath = path.join(output, 'mcp-evidence.json');
  const manifestPath = path.join(output, 'capture-manifest.json');
  let evidence = {
    label: 'Reference: real shop HTTP MCP capture; not Copilot App execution or Chronicle accounting',
    redaction: 'Only synthetic cart request evidence is published. Original response sizes are UTF-8 bytes, not tokens.',
    stages: {}
  };
  let manifest = {
    method: 'Playwright actual shop UI; BootUI accessed only through HTTP MCP, no dashboard screenshots',
    viewport, browser: browser.version(), browserChannel: channel, playwright: playwright.version,
    javaRuntime, stages: {}
  };
  if (stage !== 'start') {
    evidence = JSON.parse(await readFile(evidencePath, 'utf8'));
    manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
    if (JSON.stringify(manifest.javaRuntime) !== JSON.stringify(javaRuntime)) {
      throw new Error('Capture JVM changed between stages');
    }
  }
  evidence.stages[stage] = {
    identity, workload: { method: 'GET', path: '/api/cart', distinctProducts },
    cart: { items: cart.items, itemCount: cart.itemCount, totalCents: cart.totalCents },
    activity: {
      tool: activity.tool, arguments: activity.arguments,
      originalResponseBytes: activity.originalResponseBytes,
      matchedRequest: { id: entry.id, method: entry.method, path: entry.path, status: entry.status }
    },
    profile: {
      tool: profile.tool, arguments: profile.arguments, originalResponseBytes: profile.originalResponseBytes,
      requestId: journal.requestId, route: journal.route, status: journal.status, sqlEventCount: sqlEvents.length,
      timeline: journal.timeline.map(({ source, label, detail }) => ({ source, label, detail }))
    }
  };
  manifest.stages[stage] = {
    identity, sourceRepository: references.repository, sourceTag: reference.tag, sourceCommit: reference.commit,
    transport: 'HTTP JSON-RPC tools/call; terminal reference, not a native App call',
    images: { [image]: sha256(await readFile(path.join(output, image))) }
  };
  const evidenceText = JSON.stringify(evidence, null, 2) + '\n';
  manifest.mcpEvidenceSha256 = sha256(Buffer.from(evidenceText));
  await writeFile(evidencePath, evidenceText);
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  if (stage === 'start') {
    for (const obsolete of ['order-desk-rejected.png', 'order-desk-fixed.png', 'bootui-request.png',
      'bootui-fixed.png', 'incoming-partial-commit.png', 'incoming-good.png']) {
      try { await unlink(path.join(output, obsolete)); }
      catch (error) { if (error.code !== 'ENOENT') throw error; }
    }
  }
  console.log(`Captured ${stage}: quantity ${quantity}, ${sqlEvents.length} SELECTs, MCP request ${entry.id}`);
} finally {
  await browser.close();
}
