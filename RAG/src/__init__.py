"""RAG system over the vLLM codebase (invoked as `python -m src`)."""

import os
from pathlib import Path

# On 42 machines the home quota is tiny, so redirect the HuggingFace model
# cache (~1.4 GB for Qwen) to goinfre. This runs before `transformers` is
# imported anywhere, and is a no-op when ~/goinfre is absent (other machines).
_GOINFRE = Path.home() / "goinfre"
if _GOINFRE.is_dir():
    os.environ.setdefault("HF_HOME", str(_GOINFRE / "hf-cache"))
