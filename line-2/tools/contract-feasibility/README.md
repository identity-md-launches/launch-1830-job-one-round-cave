# Offline contract feasibility preflight

Find selected impossible branches in the line-2 structural contract language
before asking workers to produce a JSON deliverable. Python 3.10+, standard
library only; this folder runs independently with its included `engine.py`.

From the repository root, one command demonstrates the tool:

```sh
python3 -B line-2/tools/contract-feasibility/check.py line-2/tools/contract-feasibility/impossible.contract.json
```

Observed: exit **1**, `complete: true`, `provenImpossible: true`. An integer
amount between 0.1 and 0.9 cannot exist. Its required parent is therefore
impossible too. The optional memo enum has no string long enough; that branch
is reported independently. Diagnostic `contractPath` values are escaped JSON
Pointers into the contract, including `/properties/amount` and `/properties/memo`.
Root is the empty pointer. No candidate document is needed.

The retained real ZTO window manifest contract also works:

```sh
python3 -B line-2/tools/contract-feasibility/check.py line-2/tools/field-relations/window.contract.json
```

Observed: exit **0**, `status: "not_proven_impossible"`, no findings. This checks
only a retained contract, not the manifest, evidence, chain state or settlement.
No coin, network, installation or account is needed.

## Meaning and limits

The preflight first uses the exact-contract engine's contract preparation.
Malformed or unsupported contracts (including inverted bounds) return exit 2.
For well-formed contracts it proves emptiness in these cases:

- No finite enum member passes the node's full structural validator.
- Integer bounds contain no integer literal, using exact decimal ceil/floor.
- A required object property has a proven impossible contract.
- An array's minimum length requires an impossible prefix or tail item.

Optional properties and unused array positions may be impossible without
making the root impossible. They still produce findings. `prefixItems` replace
`items` at their positions, matching the inherited validator's semantics.
Enum validation includes nested fields, exact numbers, patterns and uniqueness.
Boolean values remain distinct from integers; decimal literals do not satisfy
integer type even when mathematically integral.

Exit **1** proves the root has no valid document under these semantics. Exit
**0** means only that these checks did not prove it impossible. It does **not**
prove satisfiability, approve a document or guarantee a future checker pass.
For example, incompatible string length and regex rules without an enum are
not solved. Unique-item capacity and general regex satisfiability are not
solved. Run the normal document validator as well. Require `complete: true`;
input/output failure is exit **2**, `complete: false`.

Inputs use the included engine's no-follow bounded reader: visible relative
workspace paths only, no symlinks, hidden or parent components, directories or
special files. One input capture, at most 1,000,000 bytes. Output has the same
byte cap, with no truncated success. `--contract-sha256 HEX` checks an independently
retained lowercase SHA-256 before parsing; byte count and digest accompany
results. Pins are not authentication. Hard links/mounts are not excluded.
No environment or external paths are read. The program only writes stdout.

Trusted regexes and enum comparisons are not a CPU sandbox. Recursion is
bounded by Python; numeric token/exponent limits match exact-contract. A large
finite enum may be costly. The copied engine is unchanged; its provenance hash
and actual outcomes are in `validation.json`.

## Check results

```sh
python3 -B line-2/tools/contract-feasibility/test_check.py
```

18 tests passed: exact neighboring large decimals, negative gaps, surviving
integers, enums with wrong literal types, all-rule enum filtering, required and
optional propagation, pointer escaping, array prefix/tail semantics, nested
uniqueness, conservative unknown results, invalid contracts, duplicate JSON,
pins before parsing, low decimal precision, CLI results and refused paths.
The inherited exact-contract suite also passed all 22 tests. Saved CLI results
are `impossible.result.json` and `window.result.json`. These are local checks,
not independent certification.
