"""
bench.py — benchmark claim extraction precision/recall.

Usage: python bench.py labeled_dir

Expect labeled_dir to contain pairs of files:
- deckname.claims.json (ground truth)
- deckname.extracted.json (extractor output)

This script matches claims by normalized text and reports precision/recall.
"""

import json
import sys
import os
import re
from src import env_loader

# Load .env automatically if it exists
env_loader.load_env()


def normalize(s):
    return re.sub(r"\W+"," ", s.lower()).strip()


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate(gt, ext):
    gt_norm = [normalize(x['claim']) for x in gt]
    ext_norm = [normalize(x['claim']) for x in ext]
    gt_set = set(gt_norm)
    ext_set = set(ext_norm)
    tp = len(gt_set & ext_set)
    fp = len(ext_set - gt_set)
    fn = len(gt_set - ext_set)
    precision = tp / (tp+fp) if (tp+fp)>0 else 0.0
    recall = tp / (tp+fn) if (tp+fn)>0 else 0.0
    return precision, recall, tp, fp, fn


def main():
    if len(sys.argv) < 2:
        print('Usage: python bench.py labeled_dir')
        sys.exit(1)
    d = sys.argv[1]
    files = os.listdir(d)
    pairs = {}
    for f in files:
        if f.endswith('.claims.json'):
            base = f[:-len('.claims.json')]
            gt = os.path.join(d, f)
            ext = os.path.join(d, base + '.extracted.json')
            if os.path.exists(ext):
                gt_list = load(gt)
                ext_list = load(ext)
                p,r,tp,fp,fn = evaluate(gt_list, ext_list)
                print(f'{base}: precision={p:.2f} recall={r:.2f} TP={tp} FP={fp} FN={fn}')


if __name__ == '__main__':
    main()
