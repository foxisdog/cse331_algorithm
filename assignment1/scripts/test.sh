#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ulimit -s unlimited
./bin/monitor ./bin/heap ./data/testfiles/*.txt
./bin/monitor ./bin/merge ./data/testfiles/*.txt
./bin/monitor ./bin/tim ./data/testfiles/*.txt
./bin/monitor ./bin/quick ./data/testfiles/*.txt
./bin/monitor ./bin/tournament ./data/testfiles/*.txt
./bin/monitor ./bin/intro ./data/testfiles/*.txt
./bin/monitor ./bin/comb ./data/testfiles/*.txt
./bin/monitor ./bin/library ./data/testfiles/*.txt
./bin/monitor ./bin/shaker ./data/testfiles/*.txt
./bin/monitor ./bin/insert ./data/testfiles/*.txt
./bin/monitor ./bin/select ./data/testfiles/*.txt
./bin/monitor ./bin/bubble ./data/testfiles/*.txt
