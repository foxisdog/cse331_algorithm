# Assignment 1: Sorting Algorithms

This project implements and compares sorting algorithms on random, sorted, descending, and partially sorted inputs. It includes basic sorting methods, hybrid approaches, and a Timsort implementation.

## Key Files

- `Makefile`: Builds the sorting executables and the runtime monitor.
- `src/`: C++ implementations and shared sorting utilities.
- `scripts/`: Test runners and helper Python scripts.
- `data/testfiles/`: Main input datasets.
- `data/testfilesfast/`: Additional partially sorted input datasets.
- `results/raw/`: Raw experiment CSV files.
- `results/processed/`: Processed experiment CSV files.
- `docs/`: Notes, pseudocode, and report drafts.

## Build

```bash
cd assignment1
make
```

Executables are written to `bin/`.

## Run

```bash
cd assignment1
./scripts/test.sh
```

Additional scripts are available for focused runs:

- `scripts/testfast.sh`
- `scripts/testbubble.sh`
- `scripts/testinsert.sh`
- `scripts/testlibrary.sh`
- `scripts/testselect.sh`
- `scripts/testshaker.sh`

## Report

The submitted report is available at [../reports/CSE331___Assignment_1.pdf](../reports/CSE331___Assignment_1.pdf).
