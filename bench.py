"""
bench.py — benchmark claim extraction precision/recall.

Usage: python bench.py labeled_dir

Expect labeled_dir to contain pairs of files:
- deckname.claims.json (ground truth)
- deckname.extracted.json (extractor output)

This is a minimal stub; replace with your preferred evaluation code.
"""

import json
import sys
from collections import Counter


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    print('This is a stub. Implement evaluation comparing ground-truth to extracted claims.')


if __name__ == '__main__':
    main()
