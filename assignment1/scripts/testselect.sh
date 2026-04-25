#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ulimit -s unlimited
./bin/monitor ./bin/select ./data/testfiles/*.txt
