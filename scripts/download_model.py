"""Download model files from Hugging Face to a local models directory.

Usage examples (PowerShell):
  # Download specific file(s)
  python .\scripts\download_model.py --repo-id meta-llama/Llama-2-7b-chat-hf --filenames pytorch_model.bin

  # Download the full repo snapshot (may be large and require git-lfs)
  python .\scripts\download_model.py --repo-id meta-llama/Llama-2-7b-chat-hf --all

Notes:
  - You must accept the model license on Hugging Face before downloading gated weights.
  - Authenticate with `huggingface-cli login` or set HF_TOKEN in your environment.
  - This script does not perform model conversions (PyTorch -> ggml). See README for conversion steps.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import List


def ensure_hf_hub():
    try:
        import huggingface_hub as hf
        return hf
    except Exception as e:
        print("The 'huggingface_hub' package is required. Install with: pip install huggingface_hub")
        raise


def download_files(repo_id: str, filenames: List[str], out_dir: str):
    hf = ensure_hf_hub()
    from huggingface_hub import hf_hub_download

    os.makedirs(out_dir, exist_ok=True)
    for name in filenames:
        try:
            print(f"Downloading {name} from {repo_id}...")
            path = hf_hub_download(repo_id=repo_id, filename=name, cache_dir=out_dir)
            print(f"Saved to: {path}")
        except Exception as e:
            print(f"Failed to download {name}: {e}")


def download_snapshot(repo_id: str, out_dir: str):
    hf = ensure_hf_hub()
    from huggingface_hub import snapshot_download

    print(f"Downloading full repo snapshot for {repo_id} into {out_dir} (this may be large)...")
    try:
        path = snapshot_download(repo_id=repo_id, cache_dir=out_dir, local_dir=out_dir, local_dir_use_symlinks=False)
        print(f"Snapshot downloaded to: {path}")
    except Exception as e:
        print(f"Failed to download snapshot: {e}")


def parse_args(argv: List[str] | None = None):
    p = argparse.ArgumentParser(description="Download model files from Hugging Face")
    p.add_argument("--repo-id", required=True, help="Hugging Face repo id (e.g., meta-llama/Llama-2-7b-chat-hf)")
    p.add_argument("--out-dir", default="models", help="Output directory to save files")
    p.add_argument("--filenames", nargs="*", help="Specific filenames to download from the repo (default: none)")
    p.add_argument("--all", action="store_true", help="Download entire repo snapshot (may be large)")
    return p.parse_args(argv)


def main(argv: List[str] | None = None):
    args = parse_args(argv)
    repo = args.repo_id
    out = os.path.abspath(args.out_dir)

    # Quick sanity message about license
    print("Make sure you have accepted the model's license on Hugging Face before downloading gated weights.")

    if args.all:
        download_snapshot(repo, out)
        return

    if args.filenames:
        download_files(repo, args.filenames, out)
        return

    print("No filenames specified and --all not set. Nothing to do. Use --filenames or --all.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(2)
