"""
Block untrusted outputs — raises an exception if any claim is contradicted.

Use this in production pipelines where accuracy is non-negotiable.

Install: pip install veroq
"""

from veroq import shield
from veroq.exceptions import VeroqError

text = "Apple's Q4 2024 revenue was $500 billion, making it the largest quarter in history."

try:
    result = shield(text, block_if_untrusted=True)
    print(f"Trusted! Score: {result.trust_score:.0%}")
except VeroqError as e:
    print(f"Blocked: {e}")
    # Handle the error — log it, fall back, or alert
