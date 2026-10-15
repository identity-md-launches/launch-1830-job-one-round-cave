"""Focused regression checks, no network or non-workspace inputs."""
from decimal import Decimal, localcontext
import hashlib
import io
import json
from contextlib import redirect_stdout
import unittest
import check


class Feasibility(unittest.TestCase):
    def run_contract(self, text):
        return check.inspect(text.encode())

    def test_exact_gap(self):
        r = self.run_contract('{"type":"integer","minimum":9007199254740992.1,"maximum":9007199254740992.9}')
        self.assertTrue(r['provenImpossible'])
        self.assertEqual(r['findings'][0]['rule'], 'integer_gap')

    def test_negative_gap(self):
        self.assertTrue(self.run_contract('{"type":"integer","minimum":-0.9,"maximum":-0.1}')['provenImpossible'])

    def test_integer_exists(self):
        self.assertFalse(self.run_contract('{"type":"integer","minimum":-0.9,"maximum":0.1}')['provenImpossible'])

    def test_decimal_enum_is_not_integer(self):
        self.assertTrue(self.run_contract('{"type":"integer","enum":[1.0,true]}')['provenImpossible'])

    def test_enum_all_rules(self):
        self.assertTrue(check.analyze({'type':'string','minLength':3,'pattern':'^x','enum':['ab','long']})['provenImpossible'])

    def test_surviving_enum(self):
        self.assertFalse(check.analyze({'type':'string','minLength':3,'enum':['ab','long']})['provenImpossible'])

    def test_required_propagation_and_pointer(self):
        child = {'type':'integer','enum':[False]}
        c = {'type':'object','required':['a/~'],'properties':{'a/~':child}}
        r = check.analyze(c)
        self.assertTrue(r['provenImpossible'])
        self.assertEqual(r['findings'][0]['contractPath'],'/properties/a~1~0')

    def test_optional_not_root_empty(self):
        r = check.analyze({'type':'object','properties':{'x':{'type':'null','enum':[3]}}})
        self.assertFalse(r['provenImpossible'])
        self.assertEqual(len(r['findings']),1)

    def test_prefix_required(self):
        c = {'type':'array','minItems':1,'prefixItems':[{'type':'null','enum':[3]}]}
        self.assertTrue(check.analyze(c)['provenImpossible'])
        c['minItems']=0
        self.assertFalse(check.analyze(c)['provenImpossible'])

    def test_tail_required(self):
        c = {'type':'array','minItems':2,'prefixItems':[{'type':'null'}], 'items':{'type':'boolean','enum':[3]}}
        self.assertTrue(check.analyze(c)['provenImpossible'])
        c['minItems']=1
        self.assertFalse(check.analyze(c)['provenImpossible'])

    def test_nested_enum(self):
        c = {'type':'array','uniqueItems':True,'enum':[[1,Decimal('1.0')]]}
        self.assertTrue(check.analyze(c)['provenImpossible'])

    def test_unhandled_is_not_acceptance(self):
        r = check.analyze({'type':'string','minLength':2,'maxLength':2,'pattern':'^abc$'})
        self.assertEqual(r['status'],'not_proven_impossible')
        self.assertFalse(r['provenImpossible'])

    def test_invalid_contract(self):
        with self.assertRaises(ValueError):
            check.analyze({'type':'number','minimum':2,'maximum':1})

    def test_duplicate_json(self):
        with self.assertRaises(ValueError):
            self.run_contract('{"type":"null","type":"object"}')

    def test_pin_before_decode(self):
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            check.inspect(b'not json','0'*64)
        raw=b'{"type":"null"}'
        self.assertEqual(check.inspect(raw,hashlib.sha256(raw).hexdigest())['source']['bytes'],len(raw))

    def test_low_precision_context(self):
        with localcontext() as ctx:
            ctx.prec=2
            self.test_exact_gap()

    def test_cli(self):
        with redirect_stdout(io.StringIO()) as out:
            code=check.main(['line-2/tools/contract-feasibility/impossible.contract.json'])
        self.assertEqual(code,1)
        self.assertTrue(json.loads(out.getvalue())['complete'])

    def test_disallowed_path(self):
        with redirect_stdout(io.StringIO()) as out:
            code=check.main(['../not-opened'])
        self.assertEqual(code,2)
        self.assertFalse(json.loads(out.getvalue())['complete'])


if __name__=='__main__':
    unittest.main()
