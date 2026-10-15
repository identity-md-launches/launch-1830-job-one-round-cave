"""Offline integration checks using the retained real ZTO batch."""
import hashlib
import json
from pathlib import Path
import unittest

import review

HERE = Path(__file__).resolve().parent
CONTRACT = (HERE / "zto-batch.contract.json").read_bytes()
TRANSCRIPT = (HERE / "zto-batch.json").read_bytes()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def reseal(value):
    value["request_sha256"] = review.BATCH["digest"](value["request"])
    value["responses_sha256"] = review.BATCH["digest"](value["responses"])
    unsigned = {k: v for k, v in value.items() if k != "transcript_sha256"}
    value["transcript_sha256"] = review.BATCH["digest"](unsigned)
    return encoded(value)


class BatchReview(unittest.TestCase):
    def check(self, contract=CONTRACT, transcript=TRANSCRIPT):
        return review.review(contract, transcript, sha(contract), sha(transcript))

    def test_retained_zto_batch(self):
        result = self.check()
        self.assertTrue(result["accepted"])
        self.assertEqual(result["requestCount"], 2)

    def test_independent_pin_precedes_parsing(self):
        with self.assertRaisesRegex(ValueError, "transcript SHA-256 pin mismatch"):
            review.review(CONTRACT, b"not json", sha(CONTRACT), sha(TRANSCRIPT))

    def test_resealed_other_token_rejected_by_contract(self):
        value = json.loads(TRANSCRIPT)
        value["request"][0]["params"][0]["to"] = "0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7"
        result = self.check(transcript=reseal(value))
        self.assertEqual(result["state"], "contract_violation")
        self.assertTrue(any(e["path"] == "/request" for e in result["errors"]))

    def test_rpc_error_rejected_after_reseal(self):
        value = json.loads(TRANSCRIPT)
        value["responses"][1].pop("result")
        value["responses"][1]["error"] = {"code": -32000, "message": "provider error"}
        result = self.check(transcript=reseal(value))
        self.assertEqual(result["state"], "rpc_error")
        self.assertEqual(result["rpcErrorIds"], [2])

    def test_modified_result_without_checksum_refused(self):
        value = json.loads(TRANSCRIPT)
        value["responses"][0]["result"] = "0x" + "0" * 64
        result = self.check(transcript=encoded(value))
        self.assertEqual(result["state"], "rpc_batch_invalid")

    def test_impossible_contract_preflight(self):
        contract = b'{"type":"integer","minimum":0.1,"maximum":0.9}'
        result = self.check(contract=contract)
        self.assertEqual(result["state"], "contract_proven_impossible")
        self.assertFalse(result["accepted"])

    def test_vendor_sources_match(self):
        root = HERE.parents[1]
        for entry in json.loads((HERE / "provenance.json").read_text()):
            source = (root / entry["source"]).read_bytes()
            copied = (root / entry["copy"]).read_bytes()
            self.assertEqual(source, copied)
            self.assertEqual(sha(copied), entry["sha256"])


if __name__ == "__main__":
    unittest.main()
