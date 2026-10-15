# Settlement anchor

`settlement-anchor` joins three retained facts before a worker relies on a
settlement: the requested policy, a successful settlement verdict, and the
transaction's recorded `(block number, block hash, transaction index)` slot.
It refuses a transaction mismatch, block-anchor mismatch, reverted verdict,
bad confirmation arithmetic, insufficient confirmations, or missing required
finality. It uses only Python's standard library and never opens a wallet,
signs, sends, or posts.

From the repository root, run the bundled example:

```sh
python3 -B line-3/tools/settlement-anchor/anchor.py --demo
```

The command exits 0 with `anchored: true`. A worker-owned bundle can be checked
with `--bundle path/to/bundle.json`; paths are bounded to regular files inside
the workspace. The bundle is a join boundary, not a replacement for the
settlement verifier or independent hash custody.

What happened when tried: the demo passed, and seven focused tests passed. The
demo replays a retained real ZTO transaction and its historical settlement
position offline; it is not a fresh chain observation. It does not prove
consensus, receipt inclusion by a cryptographic trie proof, payment amount or
authorization, and a later reorganization remains possible.
