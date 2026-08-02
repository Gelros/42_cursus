#!/bin/sh
# Redirect uv + HuggingFace caches and the venv to goinfre so they don't
# fill the limited home quota on 42 machines.
#
# No login is hardcoded: $HOME and $USER expand to the current student, so
# this works for everyone (guilacol, jdupont, ...).
#
# Usage (SOURCE it, do NOT execute — so the exports stay in your shell):
#     source ./goinfre_setup.sh
# then run `make install`, `uv run python -m src index`, etc.

# Auto-detect goinfre across the common 42 layouts. Override by exporting
# GOINFRE=<path> before sourcing.
if [ -z "$GOINFRE" ]; then
    for candidate in "$HOME/goinfre" "/goinfre/$USER" "/sgoinfre/$USER"; do
        if [ -d "$candidate" ]; then
            GOINFRE="$candidate"
            break
        fi
    done
fi

if [ -z "$GOINFRE" ] || [ ! -d "$GOINFRE" ]; then
    echo "goinfre not found (tried \$HOME/goinfre, /goinfre/\$USER, /sgoinfre/\$USER)." >&2
    echo "Set it manually: GOINFRE=/your/path source ./goinfre_setup.sh" >&2
    return 1 2>/dev/null || exit 1
fi

mkdir -p "$GOINFRE/uv-cache" "$GOINFRE/hf-cache" "$GOINFRE/venv"

export UV_CACHE_DIR="$GOINFRE/uv-cache"          # uv wheel cache (torch, ...)
export HF_HOME="$GOINFRE/hf-cache"               # Qwen model cache
export UV_PROJECT_ENVIRONMENT="$GOINFRE/venv"    # the project's virtualenv

echo "Caches redirected to $GOINFRE"
echo "  UV_CACHE_DIR=$UV_CACHE_DIR"
echo "  HF_HOME=$HF_HOME"
echo "  UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT"
