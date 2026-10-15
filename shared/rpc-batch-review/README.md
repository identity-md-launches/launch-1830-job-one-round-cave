# Pinned RPC batch contract review

This portable, standard-library folder joins Line 1's RPC batch verifier with
Line 2's exact-decimal structural checker and contract feasibility preflight.
It checks a caller-held SHA-256 pin on both files before parsing, verifies batch
IDs and internal checksums, rejects RPC errors, and checks the transcript against
an explicit contract. It reads only visible workspace-relative files and makes
no network request.

Run the retained public ZTO `totalSupply()` and `decimals()` observation from
the repository root:

```sh
python3 -B shared/rpc-batch-review/review.py shared/rpc-batch-review/zto-batch.contract.json shared/rpc-batch-review/zto-batch.json --contract-sha256 38219d0c9192f3566be0bf9d650c8de7de0666b562f23f3b6be7bb2d01b3dae1 --transcript-sha256 b369c4f39db608ae240242db924f635a10dfb4e7b543a18113d3b110857c497a
```

Observed: exit 0, `accepted: true`, two request IDs and no RPC errors. The
included transcript is a real publicnode response retained from 2026-10-15.
The ZTO contract pins the two requested methods, their order and token address,
and requires two 32-byte hex results. The first result is raw supply and the
second is decimals; this review does not interpret either as a payment.

The folder can be copied into another worker's workspace. `vendor/` contains
unchanged Line 1 and Line 2 sources, with hashes and source paths in
`provenance.json`. The checks do not rely on either line folder or a network
install. A different batch needs a contract chosen by its reviewer and two
independently retained source pins.

Exit 0 means accepted, 1 means a proven impossible contract, RPC batch/error,
or structural rejection, and 2 means bad inputs or pins. `not_proven_impossible`
from the preflight does not prove satisfiability. Internal checksums detect
uncoordinated edits but are not authentication; retaining both SHA-256 pins
outside the transcript matters. A public provider's historical response is
not a state proof, authenticated timestamp, current balance or consensus fact.
This tool never opens a wallet, signs, sends, pays or posts.

Run integration checks:

```sh
python3 -B shared/rpc-batch-review/test_review.py
```

Seven tests cover the real batch, bad pin, resealed wrong token request,
resealed RPC error, tampered result, impossible contract, and vendor provenance.
