import { test } from 'node:test';
import assert from 'node:assert/strict';
import { toGeminiRequest, readReply, generateReply, MODELS } from '../api/_lib/gemini.mjs';

const msgs = [
  { role: 'user', content: 'hi' },
  { role: 'assistant', content: 'hello' },
  { role: 'user', content: 'price?' },
];
const ok = text => ({ candidates: [{ finishReason: 'STOP', content: { parts: [{ text }] } }] });
const respond = (status, body) => ({ ok: status >= 200 && status < 300, status, json: async () => body });

test('maps assistant to model and puts the system prompt in systemInstruction', () => {
  const body = toGeminiRequest('SYS', msgs, MODELS[0]);
  assert.deepEqual(body.contents.map(c => c.role), ['user', 'model', 'user']);
  assert.equal(body.systemInstruction.parts[0].text, 'SYS');
  assert.ok(!body.contents.some(c => c.parts[0].text === 'SYS'));
});

test('sends thinkingConfig only for models that set one', () => {
  assert.deepEqual(toGeminiRequest('S', msgs, MODELS[0]).generationConfig.thinkingConfig, { thinkingLevel: 'low' });
  assert.equal(toGeminiRequest('S', msgs, MODELS[1]).generationConfig.thinkingConfig, undefined);
});

test('readReply rejects cut-off, blocked and empty replies', () => {
  assert.equal(readReply(ok('Hi there')), 'Hi there');
  assert.equal(readReply({ candidates: [{ finishReason: 'MAX_TOKENS', content: { parts: [{ text: 'Costs depend on' }] } }] }), null);
  assert.equal(readReply({ candidates: [{ finishReason: 'SAFETY' }] }), null);
  assert.equal(readReply(ok('   ')), null);
  assert.equal(readReply({}), null);
});

test('uses the first model when it answers', async () => {
  const calls = [];
  const r = await generateReply({ apiKey: 'k', systemPrompt: 'S', messages: msgs,
    fetchImpl: async (url, init) => { calls.push({ url, key: init.headers['x-goog-api-key'] }); return respond(200, ok('first')); } });
  assert.deepEqual(r, { reply: 'first' });
  assert.equal(calls.length, 1);
  assert.match(calls[0].url, /gemini-3\.8-flash:generateContent$/);
  assert.equal(calls[0].key, 'k');
});

test('falls back to the second model on a rate limit', async () => {
  const urls = [];
  const r = await generateReply({ apiKey: 'k', systemPrompt: 'S', messages: msgs,
    fetchImpl: async url => { urls.push(url); return urls.length === 1 ? respond(429, { error: { status: 'RESOURCE_EXHAUSTED' } }) : respond(200, ok('second')); } });
  assert.deepEqual(r, { reply: 'second' });
  assert.match(urls[1], /gemini-3\.5-flash-lite/);
});

test('falls back when the first reply is cut off', async () => {
  let n = 0;
  const r = await generateReply({ apiKey: 'k', systemPrompt: 'S', messages: msgs,
    fetchImpl: async () => (++n === 1 ? respond(200, { candidates: [{ finishReason: 'MAX_TOKENS', content: { parts: [{ text: 'cut' }] } }] }) : respond(200, ok('whole'))) });
  assert.deepEqual(r, { reply: 'whole' });
});

test('does not retry a bad key, and reports status without content', async () => {
  let n = 0;
  const r = await generateReply({ apiKey: 'bad', systemPrompt: 'S', messages: msgs,
    fetchImpl: async () => { n++; return respond(400, { error: { status: 'INVALID_ARGUMENT', message: 'API key not valid' } }); } });
  assert.equal(n, 1);
  assert.deepEqual(r, { error: { status: 400, model: 'gemini-3.8-flash', reason: 'INVALID_ARGUMENT' } });
});

test('reports the last error when every model fails', async () => {
  const r = await generateReply({ apiKey: 'k', systemPrompt: 'S', messages: msgs,
    fetchImpl: async () => respond(503, { error: { status: 'UNAVAILABLE' } }) });
  assert.deepEqual(r, { error: { status: 503, model: 'gemini-3.5-flash-lite', reason: 'UNAVAILABLE' } });
});

test('a non-JSON error body does not crash it', async () => {
  const r = await generateReply({ apiKey: 'k', systemPrompt: 'S', messages: msgs,
    fetchImpl: async () => ({ ok: false, status: 502, json: async () => { throw new SyntaxError('bad'); } }) });
  assert.equal(r.error.status, 502);
});
