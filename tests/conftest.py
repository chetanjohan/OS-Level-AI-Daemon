import os
import sys

# Ensure repository root is on sys.path so tests can import project modules
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
