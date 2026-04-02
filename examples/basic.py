"""
Basic Shield usage — verify any LLM output in one line.

Install: pip install veroq
API key: export VEROQ_API_KEY=your_key_here
"""

from veroq import shield

# Verify a claim
result = shield("NVIDIA reported $22 billion in Q4 2024 revenue, beating analyst expectations of $20.4 billion.")

print(f"Trust score: {result.trust_score:.0%}")
print(f"Trusted: {result.is_trusted}")
print(f"Claims extracted: {result.claims_extracted}")
print(f"Claims contradicted: {result.claims_contradicted}")
print(f"Credits used: {result.credits_used}")

if result.corrections:
    print("\nCorrections:")
    for c in result.corrections:
        print(f"  Wrong: {c['claim']}")
        print(f"  Fixed: {c['correction']}")

print(f"\nVerified text:\n{result.verified_text}")
print(f"\nReceipt IDs: {result.receipt_ids}")
