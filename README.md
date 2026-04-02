<p align="center">
  <img src="https://veroq.ai/veroq-logo.png" alt="VeroQ Shield" width="80" />
</p>

<h1 align="center">Shield</h1>

<p align="center">
  <strong>Stop shipping hallucinations. One function call.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/veroq"><img src="https://img.shields.io/pypi/v/veroq?label=PyPI&color=blue" alt="PyPI" /></a>
  <a href="https://www.npmjs.com/package/@veroq/sdk"><img src="https://img.shields.io/npm/v/@veroq/sdk?label=npm&color=blue" alt="npm" /></a>
  <a href="https://veroq.ai"><img src="https://img.shields.io/badge/docs-veroq.ai-brightgreen" alt="Docs" /></a>
  <a href="https://github.com/Veroq-api/shield/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License" /></a>
</p>

---

Wrap any LLM output in `shield()` and get back a trust score, corrections, and verification receipts. Works with OpenAI, Anthropic, LLaMA, Mistral, Gemini -- any model, any framework.

```python
from veroq import shield

result = shield("NVIDIA reported $22B in Q4 revenue, beating estimates by 12%.")

print(result.trust_score)     # 0.73
print(result.is_trusted)      # False
print(result.corrections)     # [{"claim": "...", "correction": "..."}]
print(result.verified_text)   # text with corrections inline
```

```typescript
import { shield } from "@veroq/sdk";

const result = await shield("NVIDIA reported $22B in Q4 revenue, beating estimates by 12%.");

console.log(result.trustScore);    // 0.73
console.log(result.isTrusted);     // false
console.log(result.corrections);   // [{claim, correction, confidence}]
```

## What Shield Does

1. **Extracts** verifiable claims from any LLM text
2. **Verifies** each claim against real-time evidence (web, financial data, public records)
3. **Returns** a trust score (0-1), corrections for anything wrong, and permanent verification receipts

Every verification produces a **receipt** -- a permanent, shareable proof that a claim was checked.

## Install

```bash
pip install veroq          # Python
npm install @veroq/sdk     # TypeScript / Node.js
```

Get your API key at [veroq.ai](https://veroq.ai):

```bash
export VEROQ_API_KEY=your_key_here
```

## Examples

### Wrap any LLM call

```python
from veroq import shield
import openai

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What was NVIDIA's Q4 2024 revenue?"}],
)

verified = shield(response.choices[0].message.content)

if not verified.is_trusted:
    print(f"Found {verified.claims_contradicted} incorrect claims")
    for c in verified.corrections:
        print(f"  Wrong: {c['claim']}")
        print(f"  Fixed: {c['correction']}")
```

### Block untrusted responses

```python
from veroq import shield

# Raises VeroqError if any claim is contradicted
result = shield(llm_output, block_if_untrusted=True)
```

### Zero-config middleware

```python
from veroq.middleware import openai_shield

# Every OpenAI response is automatically verified
client = openai_shield(openai.OpenAI())
response = client.chat.completions.create(model="gpt-4o", messages=[...])
# response now has .veroq_shield attached
```

### High-volume caching

```python
from veroq import CachedShield

cached = CachedShield(max_cache=1000, ttl_seconds=3600)
result = cached("NVIDIA reported $22B in Q4 revenue")   # API call
result = cached("NVIDIA reported $22B in Q4 revenue")   # instant, 0 credits
print(cached.stats())  # {'hits': 1, 'misses': 1, 'hit_rate': 0.5, 'size': 1}
```

### CI/CD -- verify AI outputs before deploy

```yaml
# .github/workflows/shield.yml
- uses: veroq/shield-action@v1
  with:
    api-key: ${{ secrets.VEROQ_API_KEY }}
    prompts: tests/prompts.json
    threshold: 0.7
```

### TypeScript

```typescript
import { shield, CachedShield } from "@veroq/sdk";

// Basic
const result = await shield("NVIDIA's Q4 revenue exceeded $22B");

// With options
const result = await shield(llmOutput, {
  source: "gpt-4o",
  agentId: "my-bot",
  blockIfUntrusted: true,
});

// Cached for high volume
const cached = new CachedShield({ maxCache: 1000 });
const r1 = await cached.shield("NVIDIA reported $22B");  // API call
const r2 = await cached.shield("NVIDIA reported $22B");  // instant
```

## ShieldResult

| Property | Type | Description |
|----------|------|-------------|
| `trust_score` / `trustScore` | `float` | Overall confidence (0-1) |
| `is_trusted` / `isTrusted` | `bool` | True if no claims contradicted |
| `corrections` | `list` | Corrections for contradicted claims |
| `verified_text` / `verifiedText` | `str` | Text with corrections inline |
| `claims` | `list` | All extracted claims with verdicts |
| `claims_extracted` / `claimsExtracted` | `int` | Number of claims found |
| `claims_contradicted` / `claimsContradicted` | `int` | Number of incorrect claims |
| `receipt_ids` / `receiptIds` | `list` | Permanent verification receipt IDs |
| `credits_used` / `creditsUsed` | `int` | API credits consumed |

## How It Works

```
Your LLM output
      |
      v
  [ Extract claims ]     "NVIDIA Q4 revenue was $22B"
      |                   "Estimates were $20.4B"
      v
  [ Verify each claim ]  web search + financial data + public records
      |
      v
  [ Return ShieldResult ]
      |
      +-- trust_score: 0.73
      +-- corrections: [{claim, correction}]
      +-- receipt_ids: ["vr_abc123"]  (permanent, shareable proof)
```

Shield uses VeroQ's verification engine under the hood: real-time web search, financial data providers, and cross-reference analysis. No fine-tuned models or vibes -- just evidence.

## Pricing

| Plan | Shield calls/day | Cost |
|------|-----------------|------|
| Free | 10 | $0 |
| Builder ($24/mo) | 100 | 5 credits + 2/claim |
| Startup ($79/mo) | 500 | 5 credits + 2/claim |
| Growth ($179/mo) | 2,000 | 5 credits + 2/claim |
| Scale ($399/mo) | 10,000 | 5 credits + 2/claim |

Cached results are free. [Full pricing at veroq.ai/pricing](https://veroq.ai/pricing).

## Part of VeroQ

Shield is the fastest way to start with [VeroQ](https://github.com/Veroq-api) -- the verified intelligence platform for AI agents. When you're ready for more:

- **[Verified Swarm](https://veroq.ai/docs)** -- 5-agent pipeline that auto-verifies every step
- **[Agent Memory](https://veroq.ai/docs)** -- persistent per-agent knowledge that gets smarter over time
- **[Agent Runtime](https://veroq.ai/docs)** -- vertical kits for finance, legal, research, compliance
- **[62 MCP Tools](https://github.com/Veroq-api/veroq-mcp)** -- full Model Context Protocol integration
- **[Verification Receipts](https://veroq.ai/docs)** -- permanent, shareable proof of every verification

## Links

- [Documentation](https://veroq.ai/docs)
- [API Reference](https://veroq.ai/docs/api)
- [Python SDK](https://github.com/Veroq-api/veroq-python)
- [TypeScript SDK](https://github.com/Veroq-api/veroq-sdk)
- [MCP Server](https://github.com/Veroq-api/veroq-mcp)
- [Get API Key](https://veroq.ai)

## License

MIT
