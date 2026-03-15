# FRED Economic Compiler + Feature Generator

A professional Python project that:

1. Reads your `config.yaml`.
2. Loads your FRED API key from `keys/*.txt`.
3. Downloads economic series grouped by frequency (weekly/monthly/quarterly).
4. Cleans and transforms each series.
5. Merges each frequency group into its own master dataset.
6. Generates features and stores all outputs to disk.

## Project Structure

```text
.
├── config.yaml
├── keys/
│   ├── .gitkeep
│   └── README.md
├── output/
│   ├── raw/
│   ├── processed/
│   ├── masters/
│   └── features/
├── pyproject.toml
├── README.md
└── src/
    └── fred_compiler/
        ├── __init__.py
        ├── config.py
        ├── fred_client.py
        ├── io_utils.py
        ├── key_manager.py
        ├── main.py
        └── processing.py
```

## Setup

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Add your FRED API key

Create `keys/fred_api_key.txt` and paste your key in that file (only the key string, no extra text).

### 3) Configure series and frequencies

Edit `config.yaml`:

- `frequencies.weekly`: weekly series IDs.
- `frequencies.monthly`: monthly series IDs.
- `frequencies.quarterly`: quarterly series IDs.
- `feature_windows`: rolling windows used in feature generation.

## Run

```bash
fred-compiler --config config.yaml
```

Alternative:

```bash
python -m fred_compiler.main --config config.yaml
```

## Output Files

After running:

- Raw series: `output/raw/<frequency>/<series_id>.csv`
- Cleaned series: `output/processed/<frequency>/<series_id>.csv`
- Merged masters: `output/masters/master_<frequency>.csv`
- Feature sets: `output/features/features_<frequency>.csv`

## Data Processing Logic

- **Cleaning**
  - Removes duplicate timestamps.
  - Sorts by date.
  - Replaces infinite values with null.
- **Transforming**
  - Time interpolation.
  - Forward/backward fill to close gaps.
- **Merging**
  - Outer join across all series in each frequency bucket.
- **Feature generation**
  - Percent change per series.
  - Rolling mean and rolling standard deviation for each configured window.

## Notes

- Keep API keys in `keys/*.txt` and never commit real credentials.
- The project is intentionally modular so you can add more transforms/features quickly.
