# Assignment 2: Traveling Salesman Problem

This project compares Traveling Salesman Problem approaches on benchmark-style coordinate datasets. The implementations include MST-based 2-approximation, Christofides, Held-Karp, and a K-means plus Held-Karp divide-and-conquer solver.

## Key Files

- `src/2app.py`: MST-based 2-approximation solver.
- `src/christo3.py`: Christofides solver.
- `src/held_karp.py`: Held-Karp exact solver and shared helper functions.
- `src/clustering_divide_conquer.py`: K-means plus Held-Karp divide-and-conquer solver.
- `src/kmeans_heldkarp.py`: Compatibility entry point for the clustering solver.
- `scripts/test.sh`: Batch runner for the main datasets.

## Directory Layout

- `datasets/`: Input CSV datasets.
- `datasets/original/`: Original TSP source files.
- `opt/`: Reference tours or optimal-tour files.
- `result/`: Experiment output CSV files.
- `result/legacy_root_runs/`: Earlier run outputs kept for comparison.
- `notebooks/`: Jupyter notebooks used during experimentation.
- `archive/ipynb_checkpoints/`: Notebook checkpoint archive.

## Run

```bash
cd assignment2
python3 ./src/2app.py ./datasets/a280.csv
python3 ./src/christo3.py ./datasets/a280.csv
python3 ./src/held_karp.py ./datasets/a280.csv
python3 ./src/clustering_divide_conquer.py ./datasets/a280.csv
```

Batch execution:

```bash
cd assignment2
./scripts/test.sh
```

By default, generated CSV outputs are saved under `result/`. Use `-o` to choose a different output file.

## Report

The submitted report is available at [../reports/CSE331___Assignment_2.pdf](../reports/CSE331___Assignment_2.pdf).
