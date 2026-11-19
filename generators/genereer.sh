#!/usr/bin/env bash
# Maakt de platen uit de declaratieve bestanden in fcd/.
# Het declaratieve bestand levert de plaat, niet andersom.
#
# Nodig: Python 3 met pyyaml en pillow, het lettertype Inter (otf)
# en de Fluent UI-iconen (npm install @fluentui/svg-icons).
#   FCD_FONTS  map met Inter-Regular.otf en Inter-Bold.otf
#   FCD_ICONS  map met de iconen (…/@fluentui/svg-icons/icons/)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p public/platen

python3 generators/fcd_plaat.py fcd/sk-demo.fcd.yaml public/platen/productplaat-sk-demo.svg
python3 generators/fcd_procesplaat.py fcd/fcd-demo.fcd.yaml public/platen/procesplaat-fcd-demo.svg
