// Gemini free-tier client for /api/chat, with a fallback model.

const ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models';

// Tried in order. The fallback only runs when the first model is rate limited
// or down, not when the request itself is bad.
// thinkingLevel 'low': with thinking on by default, gemini-3.8-flash spent 288
// of 300 output tokens thinking and cut the reply off (tested 2026-11-13).
export const MODELS = [
  { id: 'gemini-3.8-flash', thinkingConfig: { thinkingLevel: 'low' } },
  { id: 'gemini-3.5-flash-lite' },
];

const MAX_OUTPUT_TOKENS = 400;
const RETRYABLE = new Set([429, 500, 502, 503, 504]);

// Chat messages use 'assistant'; Gemini calls that role 'model'.
export function toGeminiRequest(systemPrompt, messages, model) {
  const generationConfig = { maxOutputTokens: MAX_OUTPUT_TOKENS };
  if (model.thinkingConfig) generationConfig.thinkingConfig = model.thinkingConfig;
  return {
    systemInstruction: { parts: [{ text: systemPrompt }] },
    contents: messages.map(m => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }],
    })),
    generationConfig,
  };
}

// Returns the reply text, or null if Gemini sent nothing usable.
// A reply cut off at the token limit counts as nothing usable.
export function readReply(data) {
  const candidate = data?.candidates?.[0];
  if (!candidate || candidate.finishReason !== 'STOP') return null;
  const text = (candidate.content?.parts ?? []).map(p => p.text ?? '').join('').trim();
  return text || null;
}

// Returns { reply } or { error: { status, model, reason } }.
export async function generateReply({ apiKey, systemPrompt, messages, fetchImpl = fetch }) {
  let last = null;
  for (const model of MODELS) {
    const response = await fetchImpl(`${ENDPOINT}/${model.id}:generateContent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': apiKey },
      body: JSON.stringify(toGeminiRequest(systemPrompt, messages, model)),
    });
    const data = await response.json().catch(() => ({}));
    if (response.ok) {
      const reply = readReply(data);
      if (reply) return { reply };
      last = { status: response.status, model: model.id, reason: data?.candidates?.[0]?.finishReason ?? 'EMPTY' };
      continue;
    }
    last = { status: response.status, model: model.id, reason: data?.error?.status ?? null };
    if (!RETRYABLE.has(response.status)) break;
  }
  return { error: last };
}
