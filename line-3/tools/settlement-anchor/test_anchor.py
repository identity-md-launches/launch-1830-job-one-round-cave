import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("anchor", HERE / "anchor.py")
anchor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anchor)


def demo():
    return json.loads((HERE / "demo-anchor.json").read_text())


class AnchorTests(unittest.TestCase):
    def test_demo_anchors(self):
        result = anchor.anchor(demo())
        self.assertTrue(result["anchored"])
        self.assertEqual(result["transactionIndex"], 181)

    def test_block_mismatch_is_not_anchored(self):
        bundle = demo()
        bundle["position"]["block"]["hash"] = "0x" + "ab" * 32
        result = anchor.anchor(bundle)
        self.assertEqual(result["state"], "block_anchor_mismatch")

    def test_wrong_transaction_refuses(self):
        bundle = demo()
        bundle["position"]["transactionHash"] = "0x" + "ab" * 32
        with self.assertRaises(anchor.AnchorError):
            anchor.anchor(bundle)

    def test_finality_is_required(self):
        bundle = demo()
        bundle["settlement"]["finalized"] = False
        self.assertEqual(anchor.anchor(bundle)["state"], "finality_policy_failed")

    def test_confirmation_math_is_bound(self):
        bundle = demo()
        bundle["settlement"]["confirmations"] = 12
        self.assertEqual(anchor.anchor(bundle)["state"], "confirmation_policy_failed")

    def test_reverted_verdict_does_not_pass(self):
        bundle = demo()
        bundle["settlement"]["settled"] = False
        self.assertEqual(anchor.anchor(bundle)["state"], "settlement_not_accepted")

    def test_duplicate_keys_refused(self):
        with self.assertRaises(anchor.AnchorError):
            anchor.strict_json(b'{"policy":{},"policy":{},"settlement":{},"position":{}}')


if __name__ == "__main__":
    unittest.main()
