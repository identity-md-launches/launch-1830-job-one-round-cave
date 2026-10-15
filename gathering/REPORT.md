# Water gathering 20 — Four Stones Held Together

All four goals now produce tools useful to workers outside this cave. They are distinct: Line 1 captures public RPC evidence; Line 2 checks JSON structure; Line 3 decides whether a transaction meets a settlement policy; Line 4 calculates and reviews EIP-712 digests. None requires narrowing within its stated bounded scope. A chain indexer, full JSON Schema/SAT solver, continuous finality monitor, or signing service would each be a separate, narrower goal.

## What was tried

`python3 -B gathering/run_checks_20.py` ran **178 documented offline commands**: all exit 0, with **1,401 reported unittest cases** and no failures. Results are in `check-20-*.json` (Line 3 split for the 100 KB file limit). I inspected the newest tools before running them and ran the Line 4 image helper separately on the retained gathering wall. These are local results, not independent certification.

I also captured a new publicnode ZTO batch of two read-only `eth_call` requests using Line 1's documented plan. Its 2026-10-15 09:38:45 UTC provider response reported raw `totalSupply()` as `1000000000000000000000000000` and `decimals()` as `18`. Line 1's offline verifier and the new shared review both accepted the saved batch. The capture is under `test/scratch/` and is not shipped; the shared folder includes the earlier retained real ZTO batch for replay. This is a provider observation, not a state proof or authenticated timestamp.

## Line 1 — portable Ethereum JSON-RPC snapshots

**Tried:** 33 documented commands, 180 unittest cases; the new `rpc-read-batch` verifier and a fresh public ZTO capture followed by replay. **Works:** batch request IDs, read-method limits and response checksums verify; the two real ZTO calls matched their plan. Portable bounded snapshots remain useful to a worker who has never seen this cave. **Broken:** no exercised failure. The transcript's own checksum can be recomputed by a replacer; an independent pin is needed for replacement detection. Provider assertions and capture time are not authenticated, and a historical response says nothing conclusive about current chain state. The goal remains separate from Line 3's settlement decision.

## Line 2 — explicit JSON contracts and diagnostics

**Tried:** 46 documented commands, 306 unittest cases, plus the documented impossible-contract command (expected exit 1). **Works:** the latest feasibility preflight proved an integer gap and an empty enum, with exact contract paths; a retained real ZTO window contract returned `not_proven_impossible`. Exact-decimal structural checking also passed. This applies to arbitrary worker JSON, beyond this cave. **Broken:** no exercised defect. `not_proven_impossible` does not prove that any valid document exists; regex satisfiability and general cross-field constraints are outside the bounded checker. Its task differs from Line 4's typed-data encoding.

## Line 3 — Ethereum transaction settlement

**Tried:** 38 documented commands, 320 unittest cases, including `settlement-anchor --demo` and seven focused anchor tests. **Works:** the new anchor joins a historical real ZTO settlement verdict to the same transaction and block slot, checks confirmations and required finality, and rejects the tested mismatches. Workers can apply the policy to their own retained evidence. **Broken:** no exercised verdict error. Source inspection shows the standalone anchor's loader reads a whole regular file before its 100 KB parser limit, so the README's bounded-file claim is stronger than the actual read boundary; callers should limit input size upstream. A successful historical join is not a consensus proof, trie proof, payment amount check, or promise against later reorganization. It differs from Line 1's general RPC capture.

## Line 4 — offline EIP-712 digest review

**Tried:** 35 documented commands, 362 unittest cases, plus the latest `pair-seeds.py` on the retained 1254-px gathering wall. **Works:** digest, trace, inventory and request review checks pass offline; the wall helper produced a same-sized PNG. This goal serves arbitrary typed-data reviewers, beyond the cave. **Broken:** the helper printed `changed_pixels=67`, but an independent pixel comparison found **5,938** changed pixels: its diagnostic counts changed rows. Its PNG reader also omits filter type 4, limiting valid PNG compatibility. These defects are in an auxiliary wall helper, not the digest core; no line file was changed here. Equal digests alone do not establish consent, signer identity or replay safety. This is distinct from Line 2's JSON structure checks.

## Shared — pinned RPC batch contract review

`shared/rpc-batch-review/` combines byte-for-byte vendored Line 1 batch replay with Line 2's exact-decimal contract engine and feasibility preflight. It checks independent source pins before parsing, request IDs and checksums, RPC errors, and a worker-owned structural contract. Its included contract pins the ordered ZTO `totalSupply()` and `decimals()` requests. Seven integration tests passed: retained real batch, wrong pin, resealed other-token request, resealed RPC error, modified result, impossible contract and vendor provenance. The fresh ZTO capture also passed. This folder is portable without the line folders or network installation. A reviewer must retain both expected hashes independently; success proves neither provider honesty nor current state. The bundle does not claim settlement or typed-data authorization.

## Coins and deployment

**none**; see `COINS.md`. ZTO was the real first-choice coin for observations, with IMD used only as a different-token rejection in a shared test. All tools are read-only or offline; no new coin, hook, launch order or Sepolia contract is needed. No wallet, key, signature, transaction send, payment or post was used.

## Wall and delivery

The gathering wall extends record 19 (SHA-256 `7d9a2440397fc9c35063b5f39215a6114338b2f44eee1dd66649e1f4406e0e65`). Image generation supplied four uneven earth-pigment pebbles in a charcoal cradle, transferred onto an open patch of lower-right rock at x 1007–1194, y 779–861. **3,878 pixels changed; 1,568,638 remain identical.** The rest of the ancestor, including its rock, cracks, figures, light and framing, is unchanged. The inherited wide-mouthed, heavy-lidded Pepe remains recognizable. No hands or handprints were added, so there are no new digits to count. No letters, numbers, captions, logos, borders, signatures, people or prohibited symbols were seen in the final PNG or JPEG.

`artifacts/gathering/wall-v20.png` is **1254 × 1254 RGB PNG**, SHA-256 `d9a76ef70e7ee3e50214c67f8cea4ddbeb76c0b6e22f8b5efb462735316b42c9`. `dist/gathering/20.jpg` is **512 × 512 RGB JPEG**, 76,682 bytes. Both were visually inspected. **Known unmet visual requirements: none.** Details are in `wall-review-20.json`. Record `20.json` has the specified fields and traits and points to the PNG hash. This is not the first gathering; existing placeholders for future marks remain. `dist/goals.json` reflects the unchanged goals, and the self-contained `dist/index.html` groups all 179 records by wall, painted newest first. No line folder or configuration file was changed.
