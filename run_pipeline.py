"""
run_pipeline.py — simple driver for the pipeline stages with --step support

Usage:
  python run_pipeline.py            # run full pipeline
  python run_pipeline.py --step 1   # run only stage 1 (extract)
  python run_pipeline.py --step 2   # run only verify
  python run_pipeline.py --step 3   # run only memo+bench
"""
import argparse
import os
from src import extractor, verify, memo, env_loader

# Load .env automatically if it exists
env_loader.load_env()

# Prefer model_extractor when configured (MODEL_API_URL + GEMINI_API_KEY); fallback to heuristic extractor
try:
    from src import model_extractor
except Exception:
    model_extractor = None


def stage1():
    inputs = []
    inp_dir = os.path.join('demo','inputs')
    if os.path.isdir(inp_dir):
        for f in os.listdir(inp_dir):
            if f.lower().endswith('.pdf'):
                inputs.append(os.path.join(inp_dir, f))
    if not inputs:
        print('No PDFs in demo/inputs; run extractor on local PDFs or place sample PDFs in demo/inputs')
        return
    claims = None
    # Try model extractor first
    if model_extractor is not None:
        try:
            claims = model_extractor.extract_with_model(inputs)
            if claims is None:
                print('Model extractor not used or failed; falling back to heuristic extractor')
        except Exception as e:
            print(f'Model extractor error: {e}; falling back to heuristic extractor')
            claims = None
    if claims is None:
        claims = extractor.extract(inputs)
    out_path = os.path.join('demo','outputs','claims.json')
    extractor.write_claims(claims, out_path)
    # Print claims table to console
    try:
        from src import utils
        print('\nClaims extracted:')
        utils.print_claims_table(claims)
    except Exception:
        pass
    print(f'Wrote {out_path} ({len(claims)} claims)')


def stage2():
    inp = os.path.join('demo','outputs','claims.json')
    out_checked = os.path.join('demo','outputs','claims_checked.json')
    out_questions = os.path.join('demo','outputs','questions.md')
    verify.verify(inp, out_checked, out_questions)
    print(f'Wrote {out_checked} and {out_questions}')


def stage3():
    checked = os.path.join('demo','outputs','claims_checked.json')
    memo_out = os.path.join('demo','outputs','memo.md')
    memo.memo_from_checked(checked, memo_out)
    print(f'Wrote {memo_out}')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--step', type=int, choices=[1,2,3], help='run single stage')
    args = p.parse_args()
    if args.step == 1:
        stage1()
    elif args.step == 2:
        stage2()
    elif args.step == 3:
        stage3()
    else:
        stage1(); stage2(); stage3()
