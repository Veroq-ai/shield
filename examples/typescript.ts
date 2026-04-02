/**
 * Shield in TypeScript — same API, same result.
 *
 * Install: npm install @veroq/sdk
 * API key: export VEROQ_API_KEY=your_key_here
 */

import { shield, CachedShield } from "@veroq/sdk";

async function main() {
  // Basic verification
  const result = await shield(
    "NVIDIA reported $22 billion in Q4 2024 revenue, beating analyst expectations of $20.4 billion."
  );

  console.log(`Trust: ${(result.trustScore * 100).toFixed(0)}%`);
  console.log(`Trusted: ${result.isTrusted}`);
  console.log(`Claims: ${result.claimsExtracted}`);
  console.log(`Contradicted: ${result.claimsContradicted}`);

  if (result.corrections.length > 0) {
    console.log("\nCorrections:");
    for (const c of result.corrections) {
      console.log(`  Wrong: ${c.claim}`);
      console.log(`  Fixed: ${c.correction}`);
    }
  }

  // Cached for high volume
  const cached = new CachedShield({ maxCache: 1000 });
  const r1 = await cached.shield("NVIDIA reported $22B in Q4 revenue"); // API call
  const r2 = await cached.shield("NVIDIA reported $22B in Q4 revenue"); // instant
  console.log(`\nCache stats:`, cached.stats());

  // Block untrusted
  try {
    await shield("Some potentially wrong claim about financial data", {
      blockIfUntrusted: true,
    });
  } catch (e) {
    console.log(`\nBlocked: ${e}`);
  }
}

main();
