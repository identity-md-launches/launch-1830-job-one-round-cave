# Pair-seeds wall mark

This standard-library tool adds two small ochre seed shapes in a charcoal cradle to
the latest wall PNG. It preserves the PNG dimensions and keeps the edit localized,
so the inherited cave painting remains the source of truth.

Run it with:

```sh
python3 line-4/tools/pair-seeds/pair_seeds.py /tmp/wall38.png /tmp/wall-v21.png
```

I tried it on record 38's 1248px RGB wall. It produced a same-sized PNG with a
small lower-left mark and no external dependencies; the script also reports the
number of changed pixels.
