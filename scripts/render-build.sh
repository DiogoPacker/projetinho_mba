#!/usr/bin/env bash
# O Render executa este script no build; um reinício não baixa nem treina novamente.
set -euo pipefail
python -m pip install .
python -m flightlab.cli download
python -m flightlab.cli train
