"""
Wrap any OpenAI call with Shield — automatic verification.

Install: pip install veroq openai
"""

import openai
from veroq import shield

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "What was Apple's revenue in Q4 2024?"}],
)

llm_output = response.choices[0].message.content
print(f"LLM said: {llm_output}\n")

# One line to verify
result = shield(llm_output, source="gpt-5.4")

print(f"Trust: {result.trust_score:.0%}")
if not result.is_trusted:
    print("Issues found:")
    for c in result.corrections:
        print(f"  - {c['claim'][:80]}...")
        print(f"    Fix: {c['correction'][:80]}...")
else:
    print("All claims verified.")
