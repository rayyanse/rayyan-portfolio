// Input checks and rate limiting for /api/chat.
// Files under api/_lib are not deployed as their own functions.

export const MAX_MESSAGES = 8;
export const MAX_CHARS = 1000;
const ALLOWED_ROLES = new Set(['user', 'assistant']);

// Keeps only the last MAX_MESSAGES turns, rejects anything that isn't a plain
// user/assistant text message. The browser must never be able to send a
// "system" message, or it could rewrite the bot's instructions.
export function validateMessages(input) {
  if (!Array.isArray(input) || input.length === 0) {
    return { ok: false, error: 'messages must be a non-empty array' };
  }
  const recent = input.slice(-MAX_MESSAGES);
  for (const m of recent) {
    if (!m || typeof m !== 'object') return { ok: false, error: 'invalid message' };
    if (!ALLOWED_ROLES.has(m.role)) return { ok: false, error: 'invalid role' };
    if (typeof m.content !== 'string' || m.content.trim() === '') {
      return { ok: false, error: 'invalid content' };
    }
    if (m.content.length > MAX_CHARS) return { ok: false, error: 'message too long' };
  }
  if (recent[recent.length - 1].role !== 'user') {
    return { ok: false, error: 'last message must be from the user' };
  }
  return { ok: true, messages: recent.map(({ role, content }) => ({ role, content })) };
}

// Fixed-window limiter, kept in memory. Vercel reuses function instances, so
// this stops one visitor hammering a warm instance, but each instance has its
// own counts and a cold start resets them. It is a speed bump, not a hard cap.
export function createRateLimiter({ limit, windowMs, now = Date.now }) {
  const hits = new Map();
  return function isLimited(key) {
    const t = now();
    const entry = hits.get(key);
    if (!entry || t - entry.start >= windowMs) {
      hits.set(key, { start: t, count: 1 });
      if (hits.size > 5000) {
        for (const [k, v] of hits) if (t - v.start >= windowMs) hits.delete(k);
      }
      return false;
    }
    entry.count += 1;
    return entry.count > limit;
  };
}
