#!/usr/bin/env python3
"""Offline review of a pinned RPC batch against a worker-owned JSON contract."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
EXACT = runpy.run_path(str(VENDOR / "line-2/tools/exact-contract/check.py"))
sys.path.insert(0, str(VENDOR / "line-2/tools/contract-feasibility"))
try:
    FEASIBLE = runpy.run_path(str(VENDOR / "line-2/tools/contract-feasibility/check.py"))
finally:
    sys.path.pop(0)
BATCH = runpy.run_path(str(VENDOR / "line-1/tools/rpc-read-batch/read_batch.py"))
HEX = re.compile(r"[0-9a-f]{64}\Z")


def review(contract_raw, transcript_raw, contract_pin, transcript_pin):
    """Check source pins, feasibility, RPC integrity, and the structural policy."""
    for label, raw, pin in (("contract", contract_raw, contract_pin),
                            ("transcript", transcript_raw, transcript_pin)):
        if not HEX.fullmatch(pin) or hashlib.sha256(raw).hexdigest() != pin:
            raise ValueError(label + " SHA-256 pin mismatch")
    preflight = FEASIBLE["inspect"](contract_raw, contract_pin)
    if preflight["provenImpossible"]:
        return {"accepted": False, "state": "contract_proven_impossible",
                "preflight": preflight, "contractSha256": contract_pin,
                "transcriptSha256": transcript_pin}
    structural = EXACT["inspect"](contract_raw, transcript_raw)
    try:
        transcript = BATCH["verify_record"](EXACT["decode"](transcript_raw))
    except BATCH["BatchError"] as exc:
        return {"accepted": False, "state": "rpc_batch_invalid", "reason": str(exc)[:500],
                "contractValid": structural["valid"], "errors": structural["errors"],
                "contractSha256": contract_pin, "transcriptSha256": transcript_pin}
    errors = [r for r in transcript["responses"] if "error" in r]
    accepted = structural["valid"] and not errors
    return {"accepted": accepted,
            "state": "accepted" if accepted else ("rpc_error" if errors else "contract_violation"),
            "contractValid": structural["valid"], "errors": structural["errors"],
            "rpcErrorIds": [r["id"] for r in errors],
            "requestCount": len(transcript["request"]),
            "contractSha256": contract_pin, "transcriptSha256": transcript_pin,
            "embeddedTranscriptSha256": transcript["transcript_sha256"],
            "limitations": "Historical provider responses and caller-held pins; not a state proof, authenticated time, or current balance."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract")
    parser.add_argument("transcript")
    parser.add_argument("--contract-sha256", required=True)
    parser.add_argument("--transcript-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        contract = EXACT["read_bytes"](args.contract, 100_000)
        transcript = EXACT["read_bytes"](args.transcript, 100_000)
        result = review(contract, transcript, args.contract_sha256,
                        args.transcript_sha256)
        output = json.dumps(result, separators=(",", ":"), ensure_ascii=True)
        if len(output) > 100_000:
            raise ValueError("output exceeds byte limit")
        print(output)
        return 0 if result["accepted"] else 1
    except (ValueError, OSError, TypeError, OverflowError, RecursionError) as exc:
        print(json.dumps({"accepted": False, "state": "input_error",
                          "reason": str(exc)[:500]}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
