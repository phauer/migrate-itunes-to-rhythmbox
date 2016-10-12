SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[@]}" )" && pwd )" # find out script folder, when being sourced.
echo "Script Folder: $SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/venv/bin/activate"
echo "Activated venv in $VENV_DIR"
source "$VENV_DIR"

export PYTHONPATH="$SCRIPT_DIR/src/main/python"
echo "Exported PYTHONPATH=$PYTHONPATH"