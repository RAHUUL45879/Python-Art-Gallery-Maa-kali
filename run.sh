#!/usr/bin/env bash
# Run from UCRT64 Git Bash (or compatible Bash), inside this project.
set -euo pipefail
cd "$(dirname "$0")"
WINDOWS_PY="/c/Development/VirtualEnvironments/mitratics-kali-puja-python/Scripts/python.exe"
if [[ -n "${PYTHON_EXECUTABLE:-}" ]]; then
  PY="$PYTHON_EXECUTABLE"
elif [[ -f "$WINDOWS_PY" ]]; then
  PY="$WINDOWS_PY"
else
  PY=python
fi
case "${1:-help}" in
  test)    "$PY" -m unittest discover -s tests -v ;;
  preview) "$PY" render_radiant_31s.py --preview ;;
  full)    "$PY" render_radiant_31s.py ;;
  still)   "$PY" render_radiant_31s.py --still "${2:-355}" ;;
  *)       echo "Usage: bash run.sh {test|preview|full|still [frame]}" ;;
esac
