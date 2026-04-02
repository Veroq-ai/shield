"""
Zero-config middleware — auto-shield every LLM response.

Install: pip install veroq openai
"""

import openai
from veroq.middleware import openai_shield

# Wrap the OpenAI client — every response is now verified
client = openai_shield(openai.OpenAI())

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is Tesla's current market cap?"}],
)

# The response works exactly like normal
print(response.choices[0].message.content)

# But now has verification attached
if hasattr(response, "veroq_shield"):
    s = response.veroq_shield
    print(f"\nShield: trust={s.trust_score:.0%} claims={s.claims_extracted} corrections={s.claims_contradicted}")
