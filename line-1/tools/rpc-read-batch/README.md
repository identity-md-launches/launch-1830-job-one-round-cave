# RPC read batch

This standard-library Python tool sends a bounded batch of public Ethereum
JSON-RPC reads to Ethereum Publicnode or dRPC, correlates responses by request
ID, and saves a portable record. The offline verifier checks the request and
response batches and their checksums without making a network request. It only
accepts the read methods already allowed by Line 1's bounded snapshot tool;
redirects, environment proxy discovery, credentials, and other endpoints are
refused.

Run from the repository root to check the included public ZTO capture offline:

```sh
python3 -B line-1/tools/rpc-read-batch/read_batch.py verify line-1/tools/rpc-read-batch/live-zto-batch.json
```

I captured two real public `eth_call` reads of ZTO `totalSupply()` and
`decimals()` in one batch on 2026-10-15 UTC. Both responses correlated to their
request IDs and the saved batch passed offline verification. Publicnode
reported raw supply `1000000000000000000000000000` and 18 decimals. The
transcript retains its RPC endpoint, UTC capture time, both request/response
arrays and checksums. It is a provider response, not a state proof or
authenticated timestamp; keep the printed transcript SHA-256 separately if
you need to detect replacement of the whole record.

To capture the included request plan into a new visible workspace file:

```sh
python3 -B line-1/tools/rpc-read-batch/read_batch.py capture --plan line-1/tools/rpc-read-batch/zto-plan.json --output test/scratch/zto-batch.json
```

Capture is a public read only. The tool never reads a wallet or secret, signs,
sends a transaction, or needs a separate coin. For inherited safe file access
and read parameter checks, keep `safe-snapshot-files/safe_files.py` and
`bounded-rpc-snapshot/snapshot.py` beside the Line 1 tools. It has no external
Python dependencies.
