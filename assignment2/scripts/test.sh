#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ulimit -s unlimited

python3 ./src/clustering_divide_conquer.py ./datasets/a280.csv
python3 ./src/2app.py ./datasets/a280.csv
# python3 ./src/christo3.py ./datasets/a280.csv
# python3 ./src/christo5.py ./datasets/a280.csv

python3 ./src/clustering_divide_conquer.py ./datasets/xql662.csv
python3 ./src/2app.py ./datasets/xql662.csv
# python3 ./src/christo3.py ./datasets/xql662.csv
# python3 ./src/christo5.py ./datasets/xql662.csv

python3 ./src/clustering_divide_conquer.py ./datasets/kz9976.csv
python3 ./src/2app.py ./datasets/kz9976.csv
# python3 ./src/christo3.py ./datasets/kz9976.csv
# python3 ./src/christo5.py ./datasets/kz9976.csv

python3 ./src/2app.py ./datasets/mona-lisa100K.csv
python3 ./src/clustering_divide_conquer.py ./datasets/mona-lisa100K.csv
# python3 ./src/christo3.py ./datasets/mona-lisa100K.csv
# python3 ./src/christo5.py ./datasets/mona-lisa100K.csv
