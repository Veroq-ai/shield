"""
CachedShield — local LRU cache for high-volume pipelines.

Identical text returns instantly from cache (0 API calls, 0 credits).
Useful for batch processing, offline-first, or edge deployments.

Install: pip install veroq
"""

from veroq import CachedShield

cached = CachedShield(max_cache=1000, ttl_seconds=3600)

# First call — hits the API
r1 = cached("NVIDIA reported $22 billion in Q4 revenue, beating analyst expectations.")
print(f"Call 1: trust={r1.trust_score:.0%} (API call)")

# Second call — instant cache hit
r2 = cached("NVIDIA reported $22 billion in Q4 revenue, beating analyst expectations.")
print(f"Call 2: trust={r2.trust_score:.0%} (cached)")

# Stats
print(f"\nCache stats: {cached.stats()}")
# {'hits': 1, 'misses': 1, 'hit_rate': 0.5, 'size': 1}
