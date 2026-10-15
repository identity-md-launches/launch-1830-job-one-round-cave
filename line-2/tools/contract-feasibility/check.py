#!/usr/bin/env python3
"""Prove selected JSON contract branches impossible, without claiming full SAT."""
import argparse
from decimal import ROUND_CEILING, ROUND_FLOOR
import hashlib
import json
import re
import sys
import engine


def analyze(contract):
    engine.prepare(contract)
    findings = []

    def walk(c, path):
        reasons = []
        t = c['type']
        if 'enum' in c:
            # The complete validator decides which finite choices survive every rule.
            surviving = [i for i, v in enumerate(c['enum']) if not engine.validate(v, c)]
            if not surviving:
                reasons.append(('enum_empty', 'no enum member satisfies this node'))
        if t == 'integer' and 'minimum' in c and 'maximum' in c:
            lo, hi = c['minimum'], c['maximum']
            low = lo if type(lo) is int else lo.to_integral_value(rounding=ROUND_CEILING)
            high = hi if type(hi) is int else hi.to_integral_value(rounding=ROUND_FLOOR)
            if low > high:
                reasons.append(('integer_gap', 'bounds contain no integer literal'))
        if t == 'object':
            for key, child in c.get('properties', {}).items():
                child_path = engine.pointer(engine.pointer(path, 'properties'), key)
                empty = walk(child, child_path)
                if empty and key in c.get('required', []):
                    reasons.append(('required_empty', 'required property is impossible: ' + key))
        if t == 'array':
            minimum = c.get('minItems', 0)
            prefixes = c.get('prefixItems', [])
            for i, child in enumerate(prefixes):
                empty = walk(child, engine.pointer(engine.pointer(path, 'prefixItems'), i))
                if empty and i < minimum:
                    reasons.append(('prefix_empty', 'required array position is impossible: ' + str(i)))
            if 'items' in c:
                empty = walk(c['items'], engine.pointer(path, 'items'))
                if empty and minimum > len(prefixes):
                    reasons.append(('items_empty', 'minimum length requires an impossible tail item'))
        for rule, message in reasons:
            findings.append({'contractPath': path, 'rule': rule, 'message': message})
        return bool(reasons)

    impossible = walk(contract, '')
    return {'complete': True, 'provenImpossible': impossible,
            'status': 'impossible' if impossible else 'not_proven_impossible',
            'findings': findings,
            'scope': 'finite enums, integer gaps, required properties and required array positions; not a satisfiability proof'}


def inspect(raw, pin=None):
    digest = hashlib.sha256(raw).hexdigest()
    if pin is not None:
        if not re.fullmatch('[0-9a-f]{64}', pin):
            raise ValueError('expected SHA-256 must be 64 lowercase hex digits')
        if digest != pin:
            raise ValueError('contract SHA-256 mismatch')
    result = analyze(engine.decode(raw))
    result['source'] = {'sha256': digest, 'bytes': len(raw)}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract')
    parser.add_argument('--contract-sha256')
    args = parser.parse_args(argv)
    try:
        result = inspect(engine.read_bytes(args.contract), args.contract_sha256)
        output = json.dumps(result, ensure_ascii=True, indent=2)
        if len(output.encode()) > engine.MAX_BYTES:
            raise ValueError('complete output exceeds byte limit')
        print(output)
        return 1 if result['provenImpossible'] else 0
    except (ValueError, OSError, RecursionError) as exc:
        print(json.dumps({'complete': False, 'status': 'input_error', 'error': str(exc)[:1000]}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
