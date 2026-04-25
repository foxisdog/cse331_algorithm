#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ulimit -s unlimited
./bin/monitor ./bin/heap ./data/testfilesfast/*.txt
./bin/monitor ./bin/merge ./data/testfilesfast/*.txt
./bin/monitor ./bin/tim ./data/testfilesfast/*.txt
./bin/monitor ./bin/quick ./data/testfilesfast/*.txt
./bin/monitor ./bin/tournament ./data/testfilesfast/*.txt
./bin/monitor ./bin/intro ./data/testfilesfast/*.txt
./bin/monitor ./bin/comb ./data/testfilesfast/*.txt
