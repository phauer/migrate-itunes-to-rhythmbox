#!/usr/bin/env bash
source venv/bin/activate
echo "Activated venv"
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
export PYTHONPATH="$SCRIPT_DIR/src/main/python"
echo "Exported PYTHONPATH=$PYTHONPATH"
